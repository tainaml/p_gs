var config = require('./');
var fontConfig = require('./fonts');

module.exports = {
  name: 'Ideia icons',
  src: config.sourceAssets + '/icons/*.svg',
  dest: fontConfig.dest,
  sassDest: config.sourceAssets + '/stylesheets/base/icons',
  template: './gulpfile.js/tasks/iconFont/template.sass',
  sassOutputName: '_icons.sass',
  fontPath: '../fonts',
  className: 'icon',
  options: {
    svg: true,
    timestamp: 0, // see https://github.com/fontello/svg2ttf/issues/33
    fontName: 'icons',
    appendUnicode: true,
    normalize: false
  }
};
