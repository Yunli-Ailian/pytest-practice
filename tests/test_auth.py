from core.context import context


def test_login_success(session,base_url):
    r = session.post(f"{base_url}/login",json = {"username":"admin","password":"123456"})
    body = r.json()
    assert body["code"] == 200
    token = body["data"]["access_token"]
    assert token == "fake-token-abc123"

    context.set_token(token)
    assert context.get_token() == token

def test_me_with_token(session,base_url):
    r = session.post(f"{base_url}/login",json = {"username":"admin","password":"123456"})
    token = r.json()["data"]["access_token"]

    r = session.get(f"{base_url}/me",headers = {"Authorization":f"Bearer {token}"})

    assert r.json()["code"] == 200
    assert r.json()["data"]["username"] == "admin"

def test_me_without_token(session,base_url):
    r = session.get(f"{base_url}/me")
    assert r.json()["code"] == 401