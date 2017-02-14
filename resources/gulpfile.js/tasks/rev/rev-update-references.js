var config     = require('../../config')
var gulp       = require('gulp')
var path       = require('path')
var revReplace = require('gulp-rev-replace')

// 2) Update asset references with reved filenames in compiled css + js
gulp.task('rev-update-references', function(){
  var manifest = gulp.src(path.join(config.publicAssets, "rev-manifest.json"))

  return gulp.src([
    path.join(config.publicAssets,'/**/**.{css,js}'),
    '!'+path.join(config.publicAssets,'/selectize/*.{css,js}'),
    '!'+path.join(config.publicAssets,'/src-noconflict/*.{css,js}'),
    ])
    .pipe(revReplace({manifest: manifest}))
    .pipe(gulp.dest(config.publicAssets))
})

config.sourceAssets