import pytest
from playwright.sync_api import sync_playwright,expect
from pages.login_page import LoginPage
# selenium 里你的写法	                     Playwright 对应
# find_element(By.ID, "user")	            page.locator("#user")
# find_element(By.NAME, "username")	        page.get_by_role("textbox", name="用户名")
# find_element(By.XPATH, ...)	            page.get_by_text(...) / get_by_role(...)
# send_keys("admin")	                    fill("admin")
# WebDriverWait(driver, 5).until(...)	    expect(locator).to_be_visible()
# implicitly_wait(10)	                    不需要，Playwright 默认自动等待
BASE = "http://127.0.0.1:5000"

@pytest.fixture(scope = "session")
def browser():
    pw = sync_playwright().start()
    b = pw.chromium.launch(headless=True)
    yield b
    b.close()
    pw.stop()

@pytest.fixture
def page(browser):
    p = browser.new_page()
    yield p
    p.close()


def test_login_page_elements(page):
    page.goto(f"{BASE}/login")
    assert page.get_by_role("heading",name = "请登录").is_visible()
    assert page.get_by_role("textbox",name = "用户名").is_visible()
    assert page.get_by_role("button",name = "登录").is_visible()

def test_login_success_ui(page,base_url):
    # page.goto(f"{BASE}/login")
    # page.get_by_label("用户名").fill("admin")
    # page.get_by_label("密码").fill("123456")
    # page.get_by_role("button",name = "登录").click()
    # expect(page.locator("#msg")).to_have_text("登陆成功")
    login = LoginPage(page,base_url)
    login.open()
    login.login("admin","123456")
    login.expect_message("登录成功")

def test_login_fail_ui(page):
    page.goto(f"{BASE}/login")
    page.get_by_label("用户名").fill("admin")
    page.get_by_label("密码").fill("wrong")
    page.get_by_role("button",name = "登录").click()
    expect(page.locator("#msg")).to_have_text("用户名或密码错误")

def test_auto_wait(page):
    page.goto(f"{BASE}/login")
    page.get_by_role("button", name="加载").click()
    expect(page.locator("#late")).to_have_text("迟到的内容")