import recommendation_service_client as client

def test_basic():
    preference = client.getPreferenceForUser('test_user')
    assert preference is not None and len(preference) > 0
    print("test_basic passed!")

if __name__ == '__main__':
    test_basic()