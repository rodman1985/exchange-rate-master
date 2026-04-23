#!/usr/bin/env python3
"""
发送CI构建报告到飞书
"""
import base64
import json
import os
import sys
from datetime import datetime
from xml.etree import ElementTree as ET

import requests

# ============ 配置 ============
FEISHU_APP_ID = 'cli_a9623fab0ea15bd2'
FEISHU_APP_SECRET = 'HnmtJk3CND4p2GsF3OvjGf5eY0OC58lT'
FEISHU_USER_OPEN_ID = 'ou_a50b9673d242e46db6c49d5574cdc65a'

GITHUB_REPO = os.environ.get("GITHUB_REPO", "rodman1985/exchange-rate-master")
GITHUB_RUN_ID = os.environ.get("GITHUB_RUN_ID", "test-run")
COMPILE_STATUS = os.environ.get("COMPILE_STATUS", "success")
TEST_STATUS = os.environ.get("TEST_STATUS", "success")

# 报告链接 - 直接指向Git仓库
REPO_URL = f"https://github.com/{GITHUB_REPO}"
CI_REPORT_URL = f"{REPO_URL}/blob/main/reports/ci-report-{GITHUB_RUN_ID}.html"
JUNIT_REPORT_URL = f"{REPO_URL}/blob/main/reports/test-report/index.html"
JACOCO_REPORT_URL = f"{REPO_URL}/blob/main/reports/coverage/index.html"


def get_feishu_token():
    """获取飞书访问令牌"""
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    r = requests.post(url, json={'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}, timeout=10)
    if r.status_code == 200:
        result = r.json()
        if result.get('code') == 0:
            return result.get('tenant_access_token')
    print(f"获取Token失败: {r.text}")
    return None


def send_feishu_message(token, card):
    """发送飞书消息"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "receive_id": FEISHU_USER_OPEN_ID,
        "msg_type": "interactive",
        "content": json.dumps(card)  # JSON字符串
    }
    params = {"receive_id_type": "open_id"}

    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    r = requests.post(url, headers=headers, json=data, params=params, timeout=10)

    if r.status_code == 200:
        result = r.json()
        if result.get('code') == 0:
            print("飞书消息发送成功")
            return True
        else:
            print(f"飞书API错误: {result}")
    else:
        print(f"HTTP错误: {r.status_code} - {r.text[:200]}")
    return False


def get_test_summary():
    """从XML获取测试结果"""
    import glob
    xml_files = glob.glob("target/surefire-reports/*.xml")

    total_tests = 0
    total_passed = 0
    total_failed = 0
    test_classes = []

    for f in xml_files:
        try:
            tree = ET.parse(f)
            root = tree.getroot()
            tests = int(root.get("tests", 0))
            failures = int(root.get("failures", 0))
            errors = int(root.get("errors", 0))
            passed = tests - failures - errors

            name = root.get("name", "unknown")
            short_name = name.replace("com.github.oceanbbbbbb.", "").replace("test.", "")

            test_classes.append({
                "name": short_name,
                "tests": tests,
                "passed": passed,
                "failed": failures + errors
            })

            total_tests += tests
            total_passed += passed
            total_failed += failures + errors
        except Exception:
            pass

    return {
        "total": total_tests,
        "passed": total_passed,
        "failed": total_failed,
        "classes": test_classes
    }


def build_feishu_card():
    """构建飞书消息卡片"""
    test_data = get_test_summary()

    # 确定整体状态
    overall_status = "成功" if test_data["failed"] == 0 else "部分失败"
    status_emoji = "✅" if test_data["failed"] == 0 else "⚠️"
    template = "green" if test_data["failed"] == 0 else "orange"

    # 测试类详情
    class_details = ""
    for cls in test_data["classes"]:
        status_icon = "✅" if cls["failed"] == 0 else "❌"
        class_details += f'{status_icon} {cls["name"]}: {cls["passed"]}/{cls["tests"]}\n'

    if not class_details:
        class_details = "暂无测试数据"

    # 构建卡片
    card = {
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"{status_emoji} CI构建报告 - Exchange Rate"
            },
            "template": template
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        f"**📅 执行时间：**{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                        f"**🔖 版本：**0.0.1-SNAPSHOT\n\n"
                        f"**📊 状态：{overall_status}**"
                    )
                }
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        f"**📈 测试汇总**\n\n"
                        f"- 总用例：{test_data['total']}\n"
                        f"- 通过：{test_data['passed']}\n"
                        f"- 失败：{test_data['failed']}"
                    )
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📝 测试详情**\n```\n{class_details}```"
                }
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**📎 报告链接**"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "📄 CI构建报告"},
                        "type": "primary",
                        "url": CI_REPORT_URL
                    },
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "🧪 单测报告"},
                        "type": "primary",
                        "url": JUNIT_REPORT_URL
                    },
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "📊 覆盖率报告"},
                        "type": "primary",
                        "url": JACOCO_REPORT_URL
                    }
                ]
            },
            {
                "tag": "note",
                "elements": [
                    {"tag": "plain_text", "content": f"Run ID: {GITHUB_RUN_ID}"}
                ]
            }
        ]
    }

    return card


def main():
    print("=" * 50)
    print("CI飞书报告发送")
    print("=" * 50)
    print(f"仓库: {GITHUB_REPO}")
    print(f"Run ID: {GITHUB_RUN_ID}")

    # 获取飞书Token
    token = get_feishu_token()
    if not token:
        print("无法获取飞书访问令牌")
        sys.exit(1)

    # 构建并发送卡片
    card = build_feishu_card()
    success = send_feishu_message(token, card)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
