var config = require('./');

module.exports = {
  watch: ['../templates/**/*.html'],
  src: ['../templates/**/*.html', '!**/{layouts,shared,macros}/**'],
  dest: config.templatesDir,
  // nunjucks: [config.sourceDirectory + '/html/'],
  htmlmin: {
    collapseWhitespace: true
  }
};
