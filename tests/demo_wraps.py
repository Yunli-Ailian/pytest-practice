import pytest
from functools import wraps

def log_time(func):          # 先不加 @wraps
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@log_time
@pytest.mark.smoke
def test_demo():
    print("我是测试")