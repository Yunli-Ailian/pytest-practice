import pytest
from playwright.sync_api import sync_playwright

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

def test_home_title(page):
    page.goto(BASE)
    assert page.title() == "Mock Server"

def test_home_text(page):
    page.goto(BASE)
    assert page.locator("#title").inner_text() == "Mock 服务已启动"