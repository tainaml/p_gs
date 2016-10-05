'use strict'

// Dependecies
const $ =  require('jquery')

var module = (element) => {
  const dropZone = $(element)
  let $input = dropZone.find('input') // TODO: Change this selector name
  let $altInput = dropZone.find('[data-trigger="file"]')
  let defaultImage = dropZone.data('original-image')

  if(defaultImage){
      fakeLoad('Imagem Padrão', defaultImage)
  }

  dropZone.on({
    dragover: cbDragOver,
    dragleave: cbDragLeave,
    drop: cbDrop
  })

  $input.on({
    change: cbChangeFile
  })

  $altInput.on({
    click: cbTriggerFile
  })

  function cbDragOver (event) {
    dropZone.addClass('hover')
    return false
  }

  function cbDragLeave (event) {
    dropZone.removeClass('hover')
    return false
  }

  function cbDrop (event) {
    let file = event.originalEvent.dataTransfer.files[0]

    event.stopPropagation()
    event.preventDefault()
    dropZone.removeClass('hover')

    readFile(file)
    $input.files = file
    $input.val('')
    return false
  }

  function cbChangeFile (event) {
    readFile(this.files[0])
    return false
  }

  function cbTriggerFile (event) {
    $input.trigger('click')
  }

}

var fakeLoad = function(name, src){
  var $image = $('<img/>')
      .load(function() {
          createPreview(name, getCanvasImage(this))
      })
      .attr('src', src);
}

var readFile = function (file) {
  var reader = new FileReader();

  reader.onload = function(e) {
      fakeLoad(file.name, e.target.result)
  }
  reader.readAsDataURL(file);
}

var getCanvasImage = function(image) {

  let imgWidth = image.width,
      imgHeight = image.height;

  let canvas = document.createElement('canvas');
  canvas.width = imgWidth;
  canvas.height = imgHeight;

  let ctx = canvas.getContext('2d');
  ctx.drawImage(image, 0, 0, imgWidth, imgHeight);

  return canvas.toDataURL('image/jpeg');
}

var createPreview = function(filename, newURL) {
  let fileName = filename.substr(0, filename.lastIndexOf('.')) //subtract file extension
  let filePath = newURL
  let image = `<img src="${filePath}" class="img-responsive" alt="${fileName}"/>`
  //append new image through jQuery Template
  $('[data-content="file"]').html(image).show()
  $('.custom-file-content').hide()
}

export default module