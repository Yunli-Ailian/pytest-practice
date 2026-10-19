import pytest
import requests
import json
#@pytest.mark.parametrize("todo_id", [1, 2, 3, 4, 5]) —— 这行是告诉 pytest：「这个函数跑五次，每次 todo_id 换一个值」。
#跑出来的结果会显示成 test_todo_status[1]、[2]……一条一条列开。
#fixture 不是全局变量。 它不会自己出现在函数里，必须写进参数列表，pytest 才会去找它、塞进来。

with open ("data/todo.json",encoding="utf-8")as f:
    CASES = json.load(f)

    
with open ("data/todo2.json",encoding="utf-8")as f2:
    CASES2 = json.load(f2)


@pytest.mark.parametrize("case",CASES)
@pytest.mark.smoke
def test_todo_status(session,base_url,case):
    #f"..." —— 字符串前面加个 f，里面的 {todo_id} 就会被变量的值替换掉。这是 Python 最常用的字符串写法。
    r = session.get(f"{base_url}/todos/{case['id']}")
    assert r.status_code == case["expect"]

@pytest.mark.parametrize("case",CASES2)
def test_todo_not_found(session,base_url,case):
    r = session.get(f"{base_url}/todos/{case['id']}")
    assert r.status_code == case["expect"]

# data["email"] 这种写法是必修课。真实接口返回的 JSON 都是一层套一层，["address"]["city"] 这种取值你以后天天要用。
# in 是判断「里面有没有」。
# 想看 print 的输出，跑的时候加个 -s：pytest -v -s。

def test_user_has_email(session,base_url):
    r = session.get(f"{base_url}/users/1")
    data = r.json()
    print(data)
    assert "@" in data["email"]

#json=payload 这个参数 requests 会自动做两件事：把你给的字典转成 JSON 字符串，再设好 Content-Type: application/json。不用自己 json.dumps。
#201 是「创建成功」的状态码，不是 200。200 是「成功」，201 是「成功而且新建了东西」。
def test_create_todo(session,base_url):
    payload = {"title":"学pytest","userId":1,"completed":False}
    r = session.post(f"{base_url}/todos",json=payload)
    assert r.status_code == 201
    assert r.json()["title"] == "学pytest"

#文件名叫 test_ 开头，函数名也是 test_ 开头，pytest 就会自动收集进来，不需要任何装饰器。你的 test_create_todo、test_todo_status 都是这样被找到的。
#fixture：必须打上 @pytest.fixture 标记，pytest 才知道「这不是一条测试，是给测试准备数据用的」。
#fresh_todo 两边都不符合：名字不是 test_ 开头，所以不算测试；又没有装饰器，所以不算 fixture。它就只是一个普通函数，pytest 根本不会看它。
@pytest.fixture
def fresh_todo(session,base_url):
    r = session.post(f"{base_url}/todos",json={"title":"temps","userId":1})
    todo = r.json()
    yield todo
    session.delete(f"{base_url}/todos/{todo['id']}")

#一，httpbin.org/delay/5 会故意拖 5 秒才回应，你给 timeout=1，1 秒就掐断，所以会抛 Timeout 异常。
#二，pytest.raises(...) 的意思是「下面这段代码必须抛这个异常，不抛我才判你失败」。这是测试异常的标准写法：拿异常当预期。
#三，with 是 Python 的上下文写法，和 open() 那个一样，代码块结束时自动收尾。
@pytest.mark.smoke
def test_timeout():
    with pytest.raises(requests.exceptions.Timeout):
        requests.get("https://httpbin.org/delay/5",timeout=1)