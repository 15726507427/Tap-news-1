var client = require('./rpc_client');

// client.add(4, 5, function(response) {
//     console.assert(response == 9);
// });

// // invoke "getNewsSummariesForUser"
// client.getNewsSummariesForUser('test_user', 1, function(response) {
//     console.assert(response !== null);
// });

// invoke "logNewsClickForUser"
client.logNewsClickForUser('test_user', '2ba1e7273979fd8f581e0e7bb0561c0a');