# -*- coding: utf-8 -*-
"""把简历初稿改成真实内容版：删掉模板数字，重写工作/项目经历。"""
import copy
import docx
from docx.text.paragraph import Paragraph

SRC = r"D:\softwareTest\我的进步\docs\简历-改稿.docx"


def set_text(p, text):
    """改文本但保留段落格式：只留第一个 run。"""
    if p.runs:
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
        p.runs[0].text = text
    else:
        p.add_run(text)


def insert_after(p, text):
    """在 p 后面插入一个同格式段落。"""
    new_p = copy.deepcopy(p._p)
    p._p.addnext(new_p)
    para = Paragraph(new_p, p._parent)
    set_text(para, text)
    return para


def delete_para(p):
    p._p.getparent().remove(p._p)


d = docx.Document(SRC)
ps = d.paragraphs

# ---------- 个人简介 ----------
set_text(ps[5],
    "1 年开发经验 + 1 年软件测试经验，熟悉 Python / Java 技术栈。"
    "在保险行业负责新电销平台核心模块测试，覆盖功能、接口、性能、安全与兼容性五类测试。"
    "基于 pytest + requests 为客户管理模块搭建接口自动化测试，实现分层设计与 token 自动注入。")

# ---------- 专业技能表格 ----------
tbl = d.tables[0]
rows = tbl.rows
data = [
    ("自动化测试", "pytest / requests / Playwright / Selenium / Allure"),
    ("测试类型", "功能测试 / 接口测试 / 性能压测 / 安全功能测试 / 兼容性测试"),
    ("开发能力", "Python / Java / Spring + MyBatis / RocketMQ / SQL / Git"),
    ("质量体系", "用例设计 / 缺陷管理 / 回归测试 / 测试左移"),
]
# 原表 4 行（表头 + 3 行数据），补到 5 行
while len(tbl.rows) < len(data) + 1:
    tbl.add_row()
for i, (k, v) in enumerate(data, start=1):
    set_text(tbl.rows[i].cells[0].paragraphs[0], k)
    set_text(tbl.rows[i].cells[1].paragraphs[0], v)

# ---------- 工作经历（保持正序：开发 → 测试） ----------
set_text(ps[8], "XX 科技有限公司 · 开发工程师　|　2024.3 — 2025.8")
set_text(ps[9], "基于 Spring + MyBatis 完成后台业务模块开发，参与核心链路功能实现")
set_text(ps[10], "使用 RocketMQ 处理异步消息，JavaScript 实现前端页面交互")
set_text(ps[11], "（此处补充：具体业务模块与个人产出）")

set_text(ps[12], "XX 财产保险股份有限公司 · 测试工程师　|　2025.9 — 至今")
set_text(ps[13], "负责新电销平台（车险 / 非车 / 人管 / 薪酬）客户管理模块的功能测试与接口测试")
set_text(ps[14], "参与 C 端车险、人伤险流程项目的测试执行与缺陷跟踪")
set_text(ps[15], "使用 JMeter 开展性能压测，定位响应慢与并发瓶颈问题")
p = insert_after(ps[15], "执行安全功能测试（越权访问 / 敏感信息 / 验证码）与兼容性测试")
insert_after(p, "基于 pytest + requests 搭建客户管理模块接口自动化测试，覆盖 12 个核心接口，"
                "采用分层设计，实现 token 自动注入与参数化数据驱动")

# ---------- 项目经历 ----------
# 1. 新电销（原「电商后台web开发」位置）
set_text(ps[17], "新电销平台（车险 / 非车 / 人管 / 薪酬）| 2026")
set_text(ps[18], "项目背景：整合旧电销系统核心功能与人员管理、基本法、考试培训等模块，打造新一代电销平台")
set_text(ps[19], "我的职责：负责客户管理、非车二开、车险销售、活动管理、批量分配、OB 跑批等模块的测试")
insert_after(ps[19], "成果：1 个多月完成两轮完整测试，执行功能与接口用例 1400+ 条（去重）；"
                     "独立为客户管理模块编写接口自动化脚本，回归效率提升约 50%")

# 2. C 端车险（原「风勘平台」位置）
set_text(ps[20], "C 端车险流程平台 | 2025")
set_text(ps[21], "项目背景：（待补充）")
set_text(ps[22], "我的职责：（待补充）")
p2 = insert_after(ps[22], "成果：（待补充）")

# 3. 人伤险（原「新C端车险app平台」位置，只有标题，需要补 3 行）
set_text(ps[24], "人伤险出单平台 | 2025")
q = insert_after(ps[24], "项目背景：（待补充）")
q = insert_after(q, "我的职责：（待补充）")
insert_after(q, "成果：（待补充）")

# 4. 风勘（原「新人伤非车险人身保险出单平台」位置）
set_text(ps[25], "风勘平台 | 2025")
r = insert_after(ps[25], "项目背景：（待补充）")
r = insert_after(r, "我的职责：（待补充）")
insert_after(r, "成果：（待补充）")

# 5. 删掉「新电商销售平台」这个空标题
delete_para(ps[26])

# ---------- 个人亮点 ----------
set_text(ps[31], "开发 + 测试复合背景，既懂代码也懂质量")
set_text(ps[32], "独立搭建客户管理模块接口自动化测试，实现分层设计与 token 自动注入")
set_text(ps[33], "覆盖功能 / 接口 / 性能 / 安全 / 兼容性五类测试，熟悉保险业务全流程")
set_text(ps[34], "日常使用 Python 编写测试脚本，持续扩大自动化覆盖范围")

d.save(SRC)
print("saved:", SRC)
