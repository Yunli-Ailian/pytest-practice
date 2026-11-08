import logging
import requests
from context import context

logger = logging.getLogger("api")
logger.setLevel(logging.INFO)

class TodoAPI:
    def __init__(self,session,base_url,timeout=10):
        self.session = session
        self.base_url = base_url
        self.timeout = timeout

    def _request(self,method,path, **kwargs):
        url = self.base_url + path


        logger.info(f"->{method}{url}")
        try:
            resp = self.session.request(method,url,timeout = self.timeout,**kwargs)
        except requests.exceptions.Timeout:
            logging.error(f"[超时]{method}{url}")
            raise RuntimeError(f"[超时]{method}{url}")
        except requests.exceptions.ConnectionError:
            raise RuntimeError(f"[连接失败]{method}{url}")
        logging.info(f"<-{resp.status_code}{resp.text[:200]}")
        return resp

    def get(self,todo_id):
        return self._request("GET",f"/todos/{todo_id}")
    def create(self,title):
        return self._request("POST",f"/todos",json={"title":title,"userId":1})
    def update(self,todo_id,data):
        return self._request("PATCH",f"/todos/{todo_id}",json = data)
    def delete(self,todo_id):
        return self._request("DELETE",f"/todos/{todo_id}")
