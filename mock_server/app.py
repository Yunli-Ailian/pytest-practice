import time
from flask import Flask, request,jsonify

app = Flask(__name__)

TOKEN = "fake-token-abc123"
USER = {"username":"admin","password":"123456"}
TODOS = {i: {"id": i, "title": f"todo {i}", "userId": 1, "completed": False} for i in range(1, 201)}



@app.get("/slow")
def slow():
    time.sleep(3)                          # 故意拖 3 秒
    return jsonify({"message": "终于来了"})

@app.post("/login")
def login():
    data = request.get_json() or {}
    if data.get("username") == USER["username"] and data.get("password") == USER["password"]:
        return jsonify({"code":200,"data":{"access_token":TOKEN}})
    return jsonify({"code":400, "message": "用户名或密码错误"})

@app.get("/me")
def me():
    auth = request.headers.get("Authorization","")
    if auth == f"Bearer {TOKEN}":
        return jsonify({"code":200,"data":{"username":"admin"}})
    return jsonify({"code":401,"message":"令牌不能为空"})

@app.get("/todos/<int:todo_id>")
def get_todo(todo_id):
    todo = TODOS.get(todo_id)
    if todo is None:
        return jsonify({"message": "not found"}), 404
    return jsonify(todo)

@app.post("/todos")
def create_todo():
    data = request.get_json() or {}
    new_id = max(TODOS) + 1
    todo = {"id": new_id, "title": data.get("title", ""), "userId": data.get("userId", 1), "completed": False}
    TODOS[new_id] = todo
    return jsonify(todo), 201

@app.patch("/todos/<int:todo_id>")
def update_todo(todo_id):
    todo = TODOS.get(todo_id)
    if todo is None:
        return jsonify({"message": "not found"}), 404
    todo.update(request.get_json() or {})
    return jsonify(todo)

@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    if TODOS.pop(todo_id, None) is None:
        return jsonify({"message": "not found"}), 404
    return jsonify({})

@app.get("/users/<int:user_id>")
def get_user(user_id):
    return jsonify({"id": user_id, "username": "admin", "email": "admin@example.com"})

@app.get("/")
def index():
    return "<html><head><title>Mock Server</title></head><body><h1 id='title'>Mock 服务已启动</h1><a href='/todos/1'>看看 todo 1</a></body></html>"

LOGIN_PAGE = """<!doctype html>
<button id="load">加载</button>
<div id="box"></div>
<script>
document.getElementById('load').addEventListener('click', function () {
  setTimeout(function () {
    document.getElementById('box').innerHTML = '<p id="late">迟到的内容</p>';
  }, 2000);
});
</script>
<html lang="zh">
<head><title>登录</title></head>
<body>
  <h1>请登录</h1>
  <form action="/web/login" method="post">
    <label for="user">用户名</label>
    <input id="user" name="username" placeholder="请输入用户名" type="text">
    <label for="pwd">密码</label>
    <input id="pwd" name="password" placeholder="请输入密码" type="password">
    <button type="submit">登录</button>
  </form>
</body></html>"""

@app.get("/login")
def login_page():
    return LOGIN_PAGE

@app.post("/web/login")
def web_login():
    u = request.form.get("username")
    p = request.form.get("password")
    if u == USER["username"] and p == USER["password"]:
        return "<h1 id = 'msg'>登录成功</h1>"
    return "<h1 id = 'msg'>用户名或密码错误</h1>",400
if __name__ == "__main__":
    app.run(port=5000)