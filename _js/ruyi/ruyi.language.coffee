ruyi.namespace 'ruyi.language', (exports) ->
  'use strict'

  exports.set = (language) ->
    body = $(document.body)
    $('*[lang]', body).addClass('hide')
    $('*[lang="' + language + '"]', body).removeClass('hide')

  ruyi.init ->
    language = navigator.userLanguage or navigator.language or 'en'
    language = language.split('-')[0].toLowerCase()
    language = 'en' unless language in ['zh']
    ruyi.language.set language
