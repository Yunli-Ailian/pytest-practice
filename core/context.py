class Context:
    def __init__(self):
        self._data = {}
    
    def set(self,key,value):
        self._data[key] = value
    
    def get(self,key,default=None):
        return self._data.get(key,default)

    def set_token(self,token):
        self.set("token",token)

    def get_token(self):
        return self.get("token")

    def clear(self):
        self._data.clear()

context = Context()