var config = require('./');
var html = require('./html');

module.exports = {
    // server: {},
    proxy: "localhost:8000",
    files: html.src
};