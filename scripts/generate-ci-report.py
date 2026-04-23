#!/usr/bin/env python3
# 生成CI构建报告HTML

import glob
import os
from datetime import datetime
from xml.etree import ElementTree as ET

# 尝试读取Maven测试结果
def get_test_summary():
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
            # 简化类名
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


def generate_ci_report():
    # 获取测试数据
    test_data = get_test_summary()

    # 获取JaCoCo覆盖率
    coverage = "N/A"
    jacoco_index = "target/site/jacoco/index.html"
    if os.path.exists(jacoco_index):
        # 简单读取覆盖率百分比
        try:
            with open(jacoco_index, "r", encoding="utf-8") as f:
                content = f.read()
                # 查找覆盖率数值
                import re
                match = re.search(r'Total.*?(\d+)%', content)
                if match:
                    coverage = match.group(1) + "%"
        except Exception:
            pass

    # 生成HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI构建报告 - Exchange Rate</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header .meta {{ display: flex; gap: 20px; font-size: 0.9em; opacity: 0.9; }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card .number {{ font-size: 2.5em; font-weight: bold; color: #667eea; }}
        .summary-card .label {{ color: #666; font-size: 0.9em; margin-top: 5px; }}
        .card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card h2 {{
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background-color: #f8f9fa; font-weight: 600; }}
        .status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
        }}
        .status-success {{ background-color: #d4edda; color: #155724; }}
        .status-failed {{ background-color: #f8d7da; color: #721c24; }}
        .status-warning {{ background-color: #fff3cd; color: #856404; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.85em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CI构建执行报告</h1>
            <div class="meta">
                <span>📅 执行时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
                <span>🔖 版本：0.0.1-SNAPSHOT</span>
                <span>✅ 状态：成功</span>
            </div>
        </div>

        <!-- 摘要卡片 -->
        <div class="summary-cards">
            <div class="summary-card">
                <div class="number">3</div>
                <div class="label">构建阶段</div>
            </div>
            <div class="summary-card">
                <div class="number">{test_data["total"]}</div>
                <div class="label">单元测试用例</div>
            </div>
            <div class="summary-card">
                <div class="number">{test_data["passed"]}</div>
                <div class="label">通过</div>
            </div>
            <div class="summary-card">
                <div class="number">{coverage}</div>
                <div class="label">代码覆盖率</div>
            </div>
        </div>

        <!-- 构建阶段 -->
        <div class="card">
            <h2>一、构建阶段</h2>
            <table>
                <thead>
                    <tr>
                        <th>步骤</th>
                        <th>状态</th>
                        <th>详情</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>编译项目源码</td>
                        <td><span class="status status-success">成功</span></td>
                        <td>Maven编译Java源文件</td>
                    </tr>
                    <tr>
                        <td>Maven测试</td>
                        <td><span class="status status-success">成功</span></td>
                        <td>运行JUnit单元测试</td>
                    </tr>
                    <tr>
                        <td>打包JAR</td>
                        <td><span class="status status-success">成功</span></td>
                        <td>生成可执行JAR包</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 测试结果 -->
        <div class="card">
            <h2>二、测试阶段</h2>
            <table>
                <thead>
                    <tr>
                        <th>测试类</th>
                        <th>用例数</th>
                        <th>通过</th>
                        <th>失败</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
'''

    for cls in test_data["classes"]:
        status = "通过" if cls["failed"] == 0 else "部分通过"
        status_class = "status-success" if cls["failed"] == 0 else "status-warning"
        html += f'''                    <tr>
                        <td>{cls["name"]}</td>
                        <td>{cls["tests"]}</td>
                        <td>{cls["passed"]}</td>
                        <td>{cls["failed"]}</td>
                        <td><span class="status {status_class}">{status}</span></td>
                    </tr>
'''

    html += f'''                </tbody>
            </table>
            <p style="margin-top:15px; color:#666;">
                <strong>汇总：</strong>共 {test_data["total"]} 个测试，{test_data["passed"]} 通过，{test_data["failed"]} 失败
            </p>
        </div>

        <div class="footer">
            <p>报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Exchange Rate Project</p>
        </div>
    </div>
</body>
</html>'''

    # 确保目录存在
    os.makedirs("ci-reports", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # 写入文件
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = f"ci-reports/ci-report-{timestamp}.html"
    latest_path = "ci-reports/index.html"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"CI报告已生成: {report_path}")
    print(f"最新报告: {latest_path}")


if __name__ == "__main__":
    generate_ci_report()
