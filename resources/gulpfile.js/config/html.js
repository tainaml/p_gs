var config = require('./');

module.exports = {
  watch: ['../../../rede_gsti/templates/**/*.html'],
  src: ['../../../rede_gsti/templates/**/*.html', '!**/{layouts,shared,macros}/**'],
  dest: config.templatesDir,
  htmlmin: {
    collapseWhitespace: true
  }
};
