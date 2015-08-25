var gulp     = require('gulp');
// var exec  = require('express');
var exec     = require('child_process').exec;
var config   = require('../config/server');
var gutil    = require('gulp-util');
var compress = require('compression');
var logger   = require('morgan');
var open     = require('open');

gulp.task('server', function() {
    // var isWin = /^win/.test(process.platform);
    //  var cmd =  '../../../';

    // if (isWin) { //for Windows
    //     cmd = '..\\Scripts\\activate';
    // }

    // var proc = exec(cmd+' && python manage.py runserver 0.0.0.0:8000');
    var url = 'http://localhost:' + config.port;

    express()
    .use(compress())
    .use(logger(config.logLevel))
    .use('/', express.static(config.root, config.staticOptions))
    .listen(config.port);

    gutil.log('production server started on ' + gutil.colors.green(url));
    open(url);
});
