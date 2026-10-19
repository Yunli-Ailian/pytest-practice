import requests
import pytest
# 默认是 function，每个测试都重新做一遍；改成 session，整个测试会话只做一次。
# 什么时候用 session？典型例子是数据库连接，每次测试都重连太慢，就整个会话共用一个。
@pytest.fixture
def todo_response(session,base_url):
    r = session.get(f"{base_url}/todos/1")
    return r

def test_status_code(session,base_url,todo_response):
    assert todo_response.status_code == 200

def test_user_id(session,base_url,todo_response):
    assert todo_response.json()["userId"] == 1