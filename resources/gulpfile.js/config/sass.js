var config = require('./');

module.exports = {
  autoprefixer: { browsers: [
    'ie >= 9',
    'ie_mob >= 10',
    'ff >= 30',
    'chrome >= 34',
    'safari >= 6',
    'opera >= 23',
    'ios >= 6',
    'android >= 4.4',
    'bb >= 10'
    ] },
  src: config.sourceAssets + "/stylesheets/**/*.{sass,scss}",
  dest: config.publicAssets + '/stylesheets',
  settings: {
    // indentedSyntax: true, // Enable .sass syntax!
    imagePath: 'images' // Used by the image-url helper
  }
};
