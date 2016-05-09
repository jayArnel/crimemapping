var gulp       = require('gulp');
var sass       = require('gulp-sass');
var watch      = require('gulp-watch');
var plumber    = require('gulp-plumber');
var autoprefixer = require('gulp-autoprefixer');

var paths = {
    watch: [
        'map/static/map/scss/*.scss',
        ],
    style: 'storage/static/core/scss/base.scss',
    base: 'storage/static/core/scss',
    build: 'storage/static/core/css'
}


/* Task to build css from scss files */
gulp.task('buildcss', function() {
  gulp.src(paths.style, {base: paths.base})
    .pipe(plumber())
    .pipe(sass())
    .pipe(autoprefixer({ browsers: ['last 2 versions'] }))
    .pipe(gulp.dest(paths.build));
});

/* Task to watch sass changes */
gulp.task('watch', function() {
  gulp.watch(paths.watch,
             ['buildcss']);
});

/* Task when running `gulp` from terminal */
// gulp.task('default', ['compile-less', 'imagemin', 'watch-less']);
// gulp.task('default', ['compile-less', 'watch']);