var gulp         = require('gulp');
var sass         = require('gulp-sass');
var sourcemaps   = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');
var minify       = require('gulp-clean-css');
var browserSync  = require('browser-sync');
var handleErrors = require('../lib/handleErrors');
var config       = require('../config/sass');

gulp.task('sass', function () {
  return gulp.src(config.src)
    .pipe(sourcemaps.init())
    .pipe(sass(config.settings))
    .on('error', handleErrors)
    .pipe(minify())
    .on('error', handleErrors)
    .pipe(sourcemaps.write())
    .pipe(autoprefixer(config.autoprefixer))
    .pipe(gulp.dest(config.dest))
    .pipe(browserSync.reload({stream:true}));
});