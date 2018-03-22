from cloudAMQP_client import CloudAMQPClient

TEST_CLOUDAMQP_URL = 'amqp://pmxvfhxf:d09SbRv7BxRnhIQ8QBSe2pY1hwItbS64@donkey.rmq.cloudamqp.com/pmxvfhxf'
TEST_QUEUE_NAME = 'tap-news'

def test_basic():
    client = cloudAMQPClient(TEST_CLOUDAMQP_URL, TEST_QUEUE_NAME)

    msg = {"test": "test"}
    client.sendMessage(msg)
    receivedMsg = client.getMessage()
    assert receivedMsg == msg
    print("test basic passed.")

if __name__ == "__main__":
    test_basic()