import pytest
import requests
import os

#yield 和 return 的区别：return 是给完结果就结束；yield 是把东西交给你，等你用完，它会再回来继续做后面的步骤。
#os.getenv("BASE_URL", 默认值) 的意思是：先看环境变量里有没有 BASE_URL，有就用它，没有就用后面那个默认值。
@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL","https://jsonplaceholder.typicode.com")

@pytest.fixture(scope="session")
# session 会保留 cookie、headers、连接池。连续请求同一个域名时，它复用之前的 TCP 连接，会快一些；你登录一次，cookie 存在里面，后面自动带上。
#它是装权限认证的容器。token、cookie、headers、连接池，都放在里面。
def session():
    s = requests.Session()
    yield s
    s.close()