var path      = require('path')
var gulp      = require('gulp')
var rev       = require('gulp-rev')
var revNapkin = require('gulp-rev-napkin')
var config    = require('../../config')

// 1) Add md5 hashes to assets referenced by CSS and JS files
gulp.task('rev-assets', function() {
  // Ignore files that may reference assets. We'll rev them next.
  var ignoreThese = '!' + path.join(config.publicAssets,'/**/*+(css|js|json|html)')

  return gulp.src([path.join(config.publicAssets,'/**/*'), ignoreThese])
    .pipe(rev())
    .pipe(gulp.dest(config.publicAssets))
    .pipe(revNapkin({verbose: false}))
    .pipe(rev.manifest(path.join(config.publicAssets, 'rev-manifest.json'), {merge: true}))
    .pipe(gulp.dest(''))
})