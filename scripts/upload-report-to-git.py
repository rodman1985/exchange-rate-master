#!/usr/bin/env python3
"""
上传报告文件到Git仓库
用法: python upload-report-to-git.py --file <git路径> --content <本地文件路径>
"""
import base64
import os
import sys
import json
import argparse

import requests

GITHUB_API = "https://api.github.com"


def get_file_sha(repo, path, token):
    """获取文件的SHA（如果存在）"""
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json().get("sha")
    except Exception:
        pass
    return None


def upload_file(repo, path, file_path, message, token):
    """上传文件到Git仓库"""
    # 读取本地文件
    if not os.path.exists(file_path):
        print(f"警告: 文件不存在 {file_path}")
        return False

    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    # 准备请求
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }

    # 获取现有文件的SHA（用于更新）
    sha = get_file_sha(repo, path, token)

    # 准备数据
    data = {
        "message": message,
        "content": content,
    }
    if sha:
        data["sha"] = sha

    # 上传
    try:
        r = requests.put(url, headers=headers, json=data, timeout=60)
        if r.status_code in [200, 201]:
            print(f"✓ 上传成功: {path}")
            return True
        else:
            print(f"✗ 上传失败: {r.status_code} - {r.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ 上传异常: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="上传报告到Git仓库")
    parser.add_argument("--file", required=True, help="Git仓库中的目标路径")
    parser.add_argument("--content", required=True, help="本地文件路径")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPO", "rodman1985/exchange-rate-master"), help="仓库")
    parser.add_argument("--branch", default=os.environ.get("GITHUB_REF", "refs/heads/main").replace("refs/heads/", ""), help="分支")
    parser.add_argument("--message", default="ci: 上传测试报告", help="提交信息")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("错误: 未设置 GITHUB_TOKEN")
        sys.exit(1)

    # 确保目录存在
    os.makedirs(os.path.dirname(args.content) if os.path.dirname(args.content) else ".", exist_ok=True)

    success = upload_file(
        repo=args.repo,
        path=args.file,
        file_path=args.content,
        message=args.message,
        token=token
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
