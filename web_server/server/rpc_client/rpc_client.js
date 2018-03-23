var jayson = require('jayson');
var config = require('../config/config.json');

// create a client
var client = jayson.client.http({
    hostname: config.server_host,
    port: config.server_port
});

// invoke "add"
function add(a, b, callback) {
    client.request('add', [a, b], function(err, response) {
        if(err) throw err;
        console.log(response);
        callback(response.result);
    });
}

// get news summaries for a user
function getNewsSummariesForUser(user_id, page_num, callback) {
    client.request('getNewsSummariesForUser', [user_id, page_num], function(err, response) {
        if (err) throw err;
        console.log(response);
        callback(response.result);
    })
}

// send click log from a user
function logNewsClickForUser(user_id, news_id, callback) {
    client.request('logNewsClickForUser', [user_id, news_id], function(err, response) {
        if (err) throw err;
        // do not need to handle the response
        console.log(response);
    })
}

module.exports = {
    add: add,
    getNewsSummariesForUser : getNewsSummariesForUser,
    logNewsClickForUser : logNewsClickForUser
};