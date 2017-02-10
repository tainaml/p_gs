var gulp      = require('gulp');
var watch     = require('gulp-watch');
var browserSync  = require('browser-sync');
var html      = require('../config/html');
var sass      = require('../config/sass');
// var iconFont  = require('../config/iconFont');
// var svgSprite = require('../config/svg-sprite');
// var images    = require('../config/images');
// var fonts     = require('../config/fonts');

gulp.task('watch', ['browserSync'], function() {
  // watch(images.src, function() { gulp.start('images'); });
  watch(sass.src, function() { gulp.start('sass'); });
  // watch(iconFont.src, function() { gulp.start('iconFont'); });
  // watch(svgSprite.src, function() { gulp.start('svg-sprite'); });
  // watch(fonts.src, function() { gulp.start('fonts'); });
  watch(html.dest, function() {
    browserSync.reload({
      stream: true
    });
  });
});
