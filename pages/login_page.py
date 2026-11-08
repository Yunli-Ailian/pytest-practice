from playwright.sync_api import Page,expect

class LoginPage:

    def __init__(self,page:Page,base_url:str):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(f"{self.base_url}/login")

    def fill_username(self,username):
        self.page.get_by_label("用户名").fill(username)

    def fill_password(self,password):
        self.page.get_by_label("密码").fill(password)

    def click_login(self):
        self.page.get_by_role("button",name="登录").click()

    def login(self,username,password):
        self.open()
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def expect_message(self,text):
        expect(self.page.locator("#msg")).to_have_text(text)
