var config    = require('../../config')
var gulp      = require('gulp')
var path      = require('path')
var rev       = require('gulp-rev')
var revNapkin = require('gulp-rev-napkin')

// 1) Rev and compress CSS and JS files (this is done after assets, so that if a
//    referenced asset hash changes, the parent hash will change as well
gulp.task('rev-css', function(){
  return gulp.src([
    path.join(config.publicAssets,'/**/*.{css,js}'),
    '!'+path.join(config.publicAssets,'/selectize/*.{css,js}'),
    '!'+path.join(config.publicAssets,'/src-noconflict/**/*.{css,js}'),
    '!'+path.join(config.publicAssets, 'javascripts/summernote-*.js'),
    '!'+path.join(config.publicAssets, 'javascripts/jquery-*.js'),
    '!'+path.join(config.publicAssets, 'javascripts/django-*.js'),

  ])
    .pipe(rev())
    .pipe(gulp.dest(config.publicAssets))
    // .pipe(revNapkin({ force: true}))
    .pipe(rev.manifest(path.join(config.publicAssets, 'rev-manifest.json'), {
      merge: true
    }))
    .pipe(gulp.dest(''))
})
