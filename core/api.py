
#class 是「类」，把一组相关的函数打包成一个整体。TodoAPI 就是「todo 接口的所有操作」。
#__init__ 是初始化方法，创建对象时自动跑一次。简易来说就是将要多次复用并且参数不一样的对象进行封装。这里走的就是让对象初始化，
#方法调用这个TodoAPI的时候，里面每一个session和base_url都是新的实例属性而不是全局变量
#self 就是「这个对象自己」。self.session 的意思是「我这个对象身上带的 session」，这样别的函数才能拿到它。
#先把 api.py 放在 tests/ 目录下，避免 import 路径找不到。
#真实项目里用 logging，因为它能分级、能写进文件、能带时间戳。
import logging
import requests
from common import config
from core.context import context

logger = logging.getLogger("api")
logger.setLevel(logging.INFO)

class TodoAPI:
    def __init__(self,session,base_url,timeout=10):
        cfg = config.get()
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def _request(self,method,path,**kwargs):
        url = self.base_url +path

        token = context.get_token()
        if token:
            headers = kwargs.pop("headers",{})
            headers["Authorization"] = f"Bearer {token}"
            kwargs["headers"] = headers
        logger.info(f"->{method}{url}")
        try:
            resp = self.session.request(method,url,**kwargs)
        except requests.exceptions.Timeout:
            logger.error(f"[超时]{method}{url}")
            raise RuntimeError(f"[超时]{method}{url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"[连接失败]{method}{url}")
            raise RuntimeError(f"[连接失败]{method}{url}")
        logger.info(f"<-{resp.status_code}{resp.text[:200]}")
        return resp
    def get(self,todo_id):
        return self._request("GET",f"/todos/{todo_id}")   

    def create(self,title):
        return self._request("POST",f"/todos",json = {"title":title,"userId":1})
    
    def update(self,todo_id,data):
        return self._request("PATCH",f"/todos/{todo_id}",json = data)

    def delete(self,todo_id):
        return self._request("DELETE", f"/todos/{todo_id}")

    def login(self,username,password):
        r = self._request("POST","/login",json = {"username":username,"password":password})
        context.set_token(r.json()["data"]["access_token"])
        return r 

    def request(self,method,path,**kwargs):
        return self._request(method,path,**kwargs)
