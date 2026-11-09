# 接口 + UI 自动化测试练习项目

基于 pytest 的接口自动化框架，配套 Flask mock 服务与 Playwright UI 测试。
分层设计：用例层只管断言，接口封装、token 管理、配置读取各自独立。

## 目录结构

```
core/           接口封装与全局状态
  api.py          TodoAPI：统一请求入口，日志 / 超时 / token 注入
  context.py      Context 单例：登录后存 token，后续请求自动带上

common/         配置读取
  config.py       读 YAML，按环境切换
  config.yaml     环境地址、账号、超时

mock_server/
  app.py          Flask 假后端：登录鉴权、Todo CRUD、慢接口、登录页

pages/          Page Object
  login_page.py    登录页封装：元素定位与操作收在类里

tests/          测试用例
  test_auth.py     鉴权：登录、带 token 访问、无 token 被拒
  test_crud.py     增删改查完整链路（自己建、自己删）
  test_todo.py     fixture 复用示例
  test_users.py    参数化、异常断言、超时
  test_ui.py       UI 首页元素与标题
  test_ui_login.py UI 登录流程、POM、自动等待

data/           测试数据（参数化用）
docs/           学习总结、面试素材
rewrite/        闭卷重写练习
```

## 怎么跑

### 1. 装依赖

```bash
pip install -r requirements.txt
playwright install chromium     # 首次跑 UI 用例需要
```

### 2. 起 mock 服务（另开一个窗口，别关）

```bash
python mock_server/app.py
```

看到 `Running on http://127.0.0.1:5000` 即可。

### 3. 跑测试

```bash
pytest                      # 全部
pytest -m smoke             # 只跑冒烟
pytest tests/test_auth.py   # 单个文件
pytest -k login             # 按关键字
pytest --lf                 # 只跑上次失败的
```

### 4. 看报告

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 几个设计点

**token 自动注入**
登录后 token 存进 `context` 单例，`_request` 发请求前统一读取并加进 header。
用例层永远不写 `Authorization`，换登录方式只改一处。

**用例隔离**
增删改查用例自己创建数据、用完删自己那条，不碰公共的 1 号数据。
避免「单独跑能过、一起跑就挂」。

**配置与代码分离**
地址、账号、超时全在 `config.yaml`，切环境只改配置。
`ENV=prod` 可覆盖当前环境。

**UI 的自动等待**
`expect(locator).to_have_text(...)` 自带重试，不用手写 `sleep` 或 `WebDriverWait`。

## 环境

- Python 3.13
- pytest 8.3
- Playwright（Chromium）
- 本地 mock 服务，不依赖外网
