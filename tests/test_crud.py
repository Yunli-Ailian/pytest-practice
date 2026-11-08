import pytest
import time
from functools import wraps
from core.api import TodoAPI

def test_todo_crud(session,base_url):

    api = TodoAPI(session,base_url)

    r = api.create("crud 测试")
    assert r.status_code == 201
    new_id = r.json()["id"]
    assert new_id is not None

    r = api.get(new_id)
    assert r.status_code == 200

    r = api.update(new_id,{"completed": True})
    assert r.status_code == 200

    r = api.delete(new_id)
    assert r.status_code == 200

#一个 *：管「按顺序给的」，也就是位置参数
#两个 **：管「带名字给的」，也就是关键字参数

#不加 @wraps(func)，pytest 会根本找不到这条测试。
# 原因：@log_time 本质是 test_xxx = log_time(test_xxx)，也就是用 wrapper 函数替换了原函数。如果不加 @wraps，wrapper 自己的名字叫 wrapper，不是 test_xxx 了。
# pytest 靠「函数名以 test_ 开头」来认测试。现在函数名叫 wrapper，不满足 test_ 前缀 → 不被收集 → 你跑的时候它直接消失，还不会报错，最坑就坑在这——静默丢失。
# 加了 @wraps(func)，wrapper 会继承原函数的名字、文档字符串、__module__ 等元信息，于是 pytest 看到的还是 test_xxx，照常收集。
# 顺带一句：你单位框架那些 login 装饰器、AOP 切面，底层都是同一招——包一层、用 wraps 保住原名。你之前在 api_base.py 里看到的 @wraps 就是干这个的。
def log_time(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        result = func(*args,**kwargs)
        cost = (time.perf_counter() - start) * 1000
        print(f"\n[{func.__name__}]跑了{cost:.0f}ms")
        return result
    return wrapper
