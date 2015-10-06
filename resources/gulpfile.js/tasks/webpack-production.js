var config  = require('../config/webpack')('production');
var gulp    = require('gulp');
var logger  = require('../libraries/compileLogger');
var webpack = require('webpack');

gulp.task('webpack:production', function(callback) {
  webpack(config, function(err, stats) {
    logger(err, stats);
    callback();
  });
});
