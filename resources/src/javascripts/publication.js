'use strict';

const asyncModules = document.querySelectorAll( '[data-async]' )

asyncModules.forEach((element, index) => {
  const name = element.getAttribute( 'data-async' )

  require.ensure([], function () {
    module = require(`${name}`)
    module( element )
  })
})
