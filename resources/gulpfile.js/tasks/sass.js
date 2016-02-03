var gulp         = require('gulp');
var browserSync  = require('browser-sync');
var sass         = require('gulp-sass');
var minifyCss    = require('gulp-minify-css');
var handleErrors = require('../libraries/handleErrors');
var config       = require('../config/sass');
var autoprefixer = require('gulp-autoprefixer');
// var minify = require('gulp-clean-css');

gulp.task('sass', function () {
  return gulp.src(config.src)
    .pipe(sass(config.settings))
    .pipe(minifyCss())
    .on('error', handleErrors)
    .pipe(autoprefixer(config.autoprefixer))
    .pipe(gulp.dest(config.dest))
    .pipe(browserSync.reload({stream:true}));
});