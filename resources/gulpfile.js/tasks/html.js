var browserSync  = require('browser-sync');
var config       = require('../config/html');
var gulp         = require('gulp');
// var render       = require('gulp-nunjucks-render');
var gulpif       = require('gulp-if');
var htmlmin      = require('gulp-htmlmin');
var handleErrors = require('../lib/handleErrors');

gulp.task('html', function() {
  // render.nunjucks.configure(config.nunjucks, {watch: false });
  // return gulp.src(config.src)
  //   // Renderiza os templates
  //   // .pipe(render())
  //   .on('error', handleErrors)
  //   // Comprime os templates já processados
  //   // .pipe(gulpif(process.env.NODE_ENV == 'production', htmlmin(config.htmlmin)))
  //   // .pipe(gulp.dest(config.dest))
  //   .pipe(browserSync.reload({
  //     stream: true
  //   }));
});
