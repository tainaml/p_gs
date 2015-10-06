var config       = require('../../config');
var gulp         = require('gulp');
var repeatString = require('../../libraries/repeatString');
var sizereport   = require('gulp-sizereport');

// 6) Report sizes
gulp.task('size-report', function() {
  var hashedFiles = '/**/*-' + repeatString('[a-z,0-9]', 8)  + '*.*';

  return gulp.src([config.publicAssets + hashedFiles, '*!rev-manifest.json'])
    .pipe(sizereport({
        gzip: true
    }));
});
