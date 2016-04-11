var gulp = require('gulp');
var del = require('del');
var config = require('../config');
var iconFontConfig = require('../config/iconFont');

gulp.task('clean', function (cb) {
  del([
    config.publicAssets,
    iconFontConfig.sassDest
  ]
  , {force: true}
  , cb);
});
