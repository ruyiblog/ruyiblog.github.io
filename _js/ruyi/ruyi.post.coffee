ruyi.namespace 'ruyi.post', (exports) ->
  'use strict'

  on_post_init = ->
    post = $(@)
    content = post.find('section.js-post-content')

    # make links open new window
    $.each content.find('a'), ->
      $(@).attr
        target: '_blank'

    # add lity
    $.each content.find('a img'), ->
      $(@).attr
        'data-lity': ''
        'data-lity-target': $(@).parents('a').attr('href')

    # set up highlight
    $.each content.find('img'), ->
      alt = $(@).attr('alt')
      return unless alt and alt.startsWith('+')
      $(@).attr 'alt', alt.substring(1).trim()

      container = $(@).parents('.container')
      parent = $(@)
      while parent.parent()[0] != container[0]
        parent = parent.parent()

      newcontainer = null
      container.children().each ->
        unless newcontainer?
          return if @ != parent[0]
          highlight = $('<div/>').addClass('highlight').insertAfter container
          parent.remove().appendTo highlight
          newcontainer = $('<div/>').addClass('container').insertAfter highlight
          return
        $(@).remove().appendTo newcontainer

    # set up caption
    $.each content.find('img'), ->
      caption = $(@).attr('alt').trim()
      return unless caption

      container = $(@).parents('.container,.highlight')
      parent = $(@)
      while parent.parent()[0] != container[0]
        parent = parent.parent()

      if container.is('.highlight')
        $('<div/>').addClass('caption').html(caption).appendTo $('<div/>').addClass('container').insertAfter parent
      else
        $('<div/>').addClass('caption').html(caption).insertAfter parent
      parent.addClass('captioned')

  ruyi.init ->
    $('article.js-post').each on_post_init

