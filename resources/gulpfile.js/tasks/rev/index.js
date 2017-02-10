// var config = require('../../config/sass')
// if(!config.tasks.production.rev) return
var gulp         = require('gulp')
var gutil        = require('gulp-util')
var gulpSequence = require('gulp-sequence')

// If you are familiar with Rails, this task the equivalent of `rake assets:precompile`
var revTask = function(cb) {
  gulpSequence(
    // 1) Rev and compress CSS and JS files (this is done after assets, so that if a referenced asset hash changes, the parent hash will change as well
    'rev-css',
  cb)
}

gulp.task('rev', revTask)
module.exports = revTask
