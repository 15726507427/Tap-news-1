var bodyPaser = require('body-parser');
var cors = require('cors');
var express = require('express');
var path = require('path');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

app.use(bodyPaser.json());

var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

var authCheckerMiddleware = require('./middleware/auth_checker');

var passport = require('passport');
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// TODO: cross-origin handle, delete after development
// app.all('*', function(req, res, next) {
//     res.header("Access-Control-Allow-Origin", "*");
//     res.header("Access-Control-Allow-Headers", "X-Requested-With");
//     next();
// });
app.use(cors());

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static')));

app.use('/', index);
app.use('/auth', auth);
app.use('/news', authCheckerMiddleware);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    console.log(req);
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
