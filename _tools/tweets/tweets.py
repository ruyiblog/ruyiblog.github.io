import pycurl
import simplejson as json
import urllib
import oauth2
import logging
import threading
import sys
import time
import os
import yaml

 
class Tweets(threading.Thread):
 
    def __init__(self, url, consumer, token, parameters, callback):
        super(Tweets, self).__init__()
 
        self.url = url
        self.consumer = consumer
        self.token = token
        self.parameters = parameters
        self.callback = callback
        self.buffer = ''
 
    def run(self):
        oauth = oauth2.Request.from_consumer_and_token(
            self.consumer,
            token=self.token,
            http_method='POST',
            http_url=self.url,
            parameters=self.parameters
        )
        oauth.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
 
        # process headers
        headers = oauth.to_header()
        headers = ['%s: %s' % (header, value) for header, value in headers.iteritems()]
        headers = [header.encode('utf-8') for header in headers]
 
        # run the request
        request = pycurl.Curl()
        request.setopt(pycurl.URL, self.url)
        request.setopt(pycurl.POST, 1)
        request.setopt(pycurl.HTTPHEADER, headers)
        request.setopt(pycurl.POSTFIELDS, urllib.urlencode(self.parameters))
        request.setopt(pycurl.WRITEFUNCTION, self.on_received)
        request.perform()

        logging.warn('tweets: request terminated')
 
    def on_received(self, data):
        self.buffer += data
        if not data.endswith('\r\n'):
            return
 
        data = self.buffer.strip()
        self.buffer = ''
        if not data:
            return
 
        logging.debug('tweets: received: %s' % data)
        try:
            data = json.loads(data)
        except Exception, error:
            logging.error('tweets: %s: error processing: %s' % (error, data))
            return

        self.callback(data)

def update(root, modifier, message):

    os.system('cd \"%s\" && git pull' % root)

    data = []
    path = os.path.join(root, '_data', 'tweets.yml')
    with open(path, 'rb') as f:
        data = yaml.load(f) or []

    if not modifier(data):
        return

    with open(path, 'wb') as f:
        yaml.dump(data, f, default_flow_style=False)

    os.system('cd \"%s\" && git commit -a -m \"%s\" && git pull && git push' % (root, message))

def kill():
    logging.warning('tweets: quiting ...')
    sys.exit(0)
 
def setup(debug=True):
    # set up logging
    import logging.handlers
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
 
    if not debug:
        logger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        logger.addHandler(handler)
 
    import signal
    signal.signal(signal.SIGTERM, lambda signum, frame: kill())

def main(args):
    setup(args.debug)

    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    consumer = oauth2.Consumer(*args.consumer.split(':'))
    token = oauth2.Token(*args.access.split(':'))
 
    parameters = {}
    if args.follow:
        parameters['follow'] = args.follow
    if args.track:
        parameters['track'] = args.track

    root = os.path.realpath(args.root)

    def callback(data):
        if 'delete' in data and 'status' in data['delete']:
            id = data['delete']['status']['id_str']
            logging.info('tweets: delete: %s' % id)

            def modifier(data):
                for element in data:
                    if element['id'] == id:
                        data.remove(element)
                        return True
                return False

            update(root, modifier, 'tweets: deleting tweet %s' % id)
            return

        if 'text' in data and 'user' in data:
            id = data['id_str']
            text = data['text']

            if data['in_reply_to_screen_name']:
                return

            if data['user']['id_str'] != args.follow:
                return

            logging.info('tweets: new: %s: %s' % (id, text))

            def modifier(data):
                data.insert(0, {
                    'id': id,
                    'text': text,
                    'timestamp': int(time.time()),
                })
                return True

            update(root, modifier, 'tweets: new tweet %s' % id)
            return

        logging.info('tweets: strange: %s' % unicode(data))
 
    try:
	while True:
            tweets = Tweets(url, consumer, token, parameters, callback)
            tweets.setDaemon(True)
            tweets.start()
            while tweets.isAlive():
                tweets.join(10)
    except KeyboardInterrupt:
        kill()
 
def parse_args():
    import argparse
 
    class Parser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)
 
    parser = argparse.ArgumentParser(description='Stream tweets.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output in logging.')
    parser.add_argument('-c', '--consumer', metavar='TOKEN:SECRET', help='Consumer token and secret.', default=':')
    parser.add_argument('-a', '--access', metavar='TOKEN:SECRET', help='Access token and secret.', default=':')
    parser.add_argument('-f', '--follow', metavar='ID', help='A comma separated list of user IDs, indicating the users to return statuses for in the stream.', default='')
    parser.add_argument('-t', '--track', metavar='KEYWORDS', help='Keywords to track. Phrases of keywords are specified by a comma-separated list. ', default='')
    parser.add_argument('-r', '--root', metavar='ROOT', help='Root path of repository.', default='../..')
    return parser.parse_args()
 
if __name__ == '__main__':
    main(parse_args())
