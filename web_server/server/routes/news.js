var express = require('express');
var router = express.Router();
var rpc_client = require('../rpc_client/rpc_client');

router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
    console.log("Fetching news...");

    // use ":" to get variable in url
    const user_id = req.params['userId'];
    const page_num = req.params['pageNum'];

    rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
        res.json(response);
    });
});

router.post('/userId/:userId/newsId/:newsId', function(req, res, next) {
    console.log("Logging news click...");

    const user_id = req.params['userId'];
    const news_id = req.params['newsId'];

    rpc_client.logNewsClickForUser(user_id, news_id);

    // no response needed at client side, just status code is sufficient
    res.status(200)
});

module.exports = router;