var path = require('path');
var gulp = require('gulp');
var del = require('del');
var config = require('../config');
var iconFontConfig = require('../config/iconFont');

gulp.task('clean', function (cb) {
  del([
    path.join(config.publicAssets, 'stylesheets'),
    path.join(config.publicAssets, 'javascripts')
  ]
  , {force: true}
  , cb);
});
