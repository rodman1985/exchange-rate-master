#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送飞书卡片消息 - CI/CD 报告通知（富文本格式）
"""

import json
import requests
from datetime import datetime

# 飞书配置（优先使用环境变量）
APP_ID = "cli_a9623fab0ea15bd2"
APP_SECRET = "HnmtJk3CND4p2GsF3OvjGf5eY0OC58lT"
USER_OPEN_ID = "ou_a50b9673d242e46db6c49d5574cdc65a"

# 如果有环境变量则覆盖
import os
APP_ID = os.getenv("FEISHU_APP_ID", APP_ID)
APP_SECRET = os.getenv("FEISHU_APP_SECRET", APP_SECRET)
USER_OPEN_ID = os.getenv("FEISHU_USER_OPEN_ID", USER_OPEN_ID)
API_BASE = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"


def get_tenant_token():
    """获取 tenant_access_token"""
    url = API_BASE
    headers = {"Content-Type": "application/json"}
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result.get("tenant_access_token")
        else:
            print(f"[ERROR] Get token failed: {result}")
            return None
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def send_card_message(token, user_id, card_content):
    """发送卡片消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "receive_id": user_id,
        "msg_type": "interactive",
        "content": json.dumps(card_content)
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        result = response.json()
        if result.get("code") == 0:
            print(f"[OK] Card message sent successfully")
            return True
        else:
            print(f"[ERROR] Send failed: {result}")
            return False
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return False


def build_card_message():
    """构建卡片消息内容"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "🚀 CI/CD 构建报告 - Exchange Rate"
            },
            "template": "blue"
        },
        "elements": [
            # 执行时间
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**执行时间**: {timestamp}"
                }
            },
            {"tag": "hr"},
            
            # 状态概览卡片
            {
                "tag": "column_set",
                "flex_mode": "bisect",
                "background_style": "grey",
                "columns": [
                    {
                        "tag": "column",
                        "width": "stretched",
                        "vertical_align": "top",
                        "elements": [
                            {"tag": "div", "text": {"tag": "lark_md", "content": "**🟢 构建状态**\nSUCCESS"}}
                        ]
                    },
                    {
                        "tag": "column",
                        "width": "stretched",
                        "vertical_align": "top",
                        "elements": [
                            {"tag": "div", "text": {"tag": "lark_md", "content": "**📊 代码覆盖率**\n65%"}}
                        ]
                    }
                ]
            },
            {
                "tag": "column_set",
                "flex_mode": "bisect",
                "columns": [
                    {
                        "tag": "column",
                        "width": "stretched",
                        "vertical_align": "top",
                        "elements": [
                            {"tag": "div", "text": {"tag": "lark_md", "content": "**✅ 单元测试**\n63/64 通过"}}
                        ]
                    },
                    {
                        "tag": "column",
                        "width": "stretched",
                        "vertical_align": "top",
                        "elements": [
                            {"tag": "div", "text": {"tag": "lark_md", "content": "**✅ API测试(Mock)**\n50/50 通过"}}
                        ]
                    }
                ]
            },
            {"tag": "hr"},
            
            # 测试详情
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**📋 测试用例统计**"
                }
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": "OceanRatesTest: 14✅ | ReptileCMCTest: 9✅/1❌ | ConvertFXHTest: 10✅ | DataCacheTest: 12✅ | ExchangeRateBusinessTest: 18✅"
                    }
                ]
            },
            {"tag": "hr"},
            
            # 新增业务测试
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**🆕 新增测试用例 - ExchangeRateBusinessTest (18个)**"
                }
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": "• 边界值测试 (3): 零值、负数、超大金额\n• 精度计算测试 (4): 浮点精度、汇率小数位\n• 异常处理测试 (4): 空指针、网络异常、无效输入\n• 汇率准确性测试 (3): BTC/USD、ETH/USD、USD/CNY\n• 批量计算测试 (2): 多币种批量转换\n• 缓存一致性测试 (2): 缓存命中、数据一致性"
                    }
                ]
            },
            {"tag": "hr"},
            
            # 构建阶段
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**📦 构建阶段**\n\n• 编译源码 (Maven Compiler)\n• 编译测试类 (Maven Surefire)\n• 依赖下载 (Spring Boot Dependencies)\n• 打包 JAR (Spring Boot Repackage)"
                }
            },
            {"tag": "hr"},
            
            # 报告链接
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📄 查看完整报告"
                        },
                        "type": "primary",
                        "multi_url": {
                            "url": "https://github.com/oceanbbbbbb/exchange-rate/actions",
                            "pc_url": "https://github.com/oceanbbbbbb/exchange-rate/actions"
                        }
                    }
                ]
            }
        ]
    }
    
    return card


def main():
    print("[INFO] Getting tenant token...")
    token = get_tenant_token()
    
    if token:
        print("[INFO] Building card message...")
        card = build_card_message()
        print("[INFO] Sending card message...")
        send_card_message(token, USER_OPEN_ID, card)
    else:
        print("[ERROR] Failed to get token. Please check APP_SECRET.")


if __name__ == "__main__":
    main()
