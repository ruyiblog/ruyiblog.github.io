RUYI_TARGET = ruyi.js
RUYI_SOURCES = \
	debug.js \
	jquery/jquery.js \
	jquery/jquery.livequery.js \
	jquery/jquery.imagesloaded.js \
	jquery/jquery.pjax.coffee.js \
	jquery/jquery.autotimestamp.coffee.js \
	lity.js \
	ruyi/ruyi.coffee.js \
	ruyi/ruyi.utils.coffee.js \
	ruyi/ruyi.language.coffee.js \
	ruyi/ruyi.cover.coffee.js \
	ruyi/ruyi.post.coffee.js \

.PHONY: all
all:  ../static/js/$(RUYI_TARGET)

../static/js/$(RUYI_TARGET): $(RUYI_TARGET)
	mkdir -p ../static/js
	cat $(RUYI_TARGET) | sed 's/\/\*!/\/**/g' | yui-compressor --type js > ../static/js/$(RUYI_TARGET)

$(RUYI_TARGET): $(RUYI_SOURCES)
	cat $(RUYI_SOURCES) > $(RUYI_TARGET)

%.coffee.js: %.coffee
	cat $< | coffee -c -s > $<.js

.PHONY: clean
clean:
	find . -iname \*.coffee.js -exec rm -f {} \;
	rm -f $(RUYI_TARGET)
	rm -f ../static/js/$(RUYI_TARGET)
