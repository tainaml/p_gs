var path = require('path');
var gulp = require('gulp');
var del = require('del');
var config = require('../config');
var iconFontConfig = require('../config/iconFont');

gulp.task('clean', function (cb) {
  del([
    path.join(config.publicAssets, 'stylesheets/**'),
    path.join(config.publicAssets, 'javascripts/**'),
    '!'+path.join(config.publicAssets, 'javascripts'),
    '!'+path.join(config.publicAssets, 'javascripts/summernote-*.js'),
    '!'+path.join(config.publicAssets, 'javascripts/jquery-*.js'),
    '!'+path.join(config.publicAssets, 'javascripts/django-*.js'),
    '!'+path.join(config.publicAssets, 'javascripts/sw.js'),
    '!'+path.join(config.publicAssets, 'javascripts/firebase-*.js'),
  ]
  , {force: true}
  , cb);
});
