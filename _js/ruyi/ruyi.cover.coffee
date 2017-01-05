ruyi.namespace 'ruyi.cover', (exports) ->
  'use strict'

  on_cover_init = ->
    cover = $(@)
    background = cover.find('> div:first')
    image = background.find('> img')
    initial = background.height()
    debug.debug 'ruyi.cover.background.initial', initial

    background.imagesLoaded ->
      top = $(window).scrollTop()

      image.removeClass('collapsed')
      return if $(window).width() < 768

      diff = background.height() - initial
      debug.debug 'ruyi.cover.background.diff', diff
      return unless diff > 0

      $('html,body').scrollTop top + diff

  ruyi.init ->
    $('.js-cover').each on_cover_init

