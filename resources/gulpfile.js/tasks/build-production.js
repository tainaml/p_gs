var gulp         = require('gulp');
var gulpSequence = require('gulp-sequence');

gulp.task('build:production', function(cb) {
  gulpSequence(['fonts', 'images', 'iconFont', 'svg-sprite'], ['sass', 'webpack:production'], 'html', 'rev', cb);
});