#!/usr/bin/env python3
# 生成单测HTML报告

import glob
import os
from xml.etree import ElementTree as ET

def generate_test_report():
    xml_files = glob.glob('target/surefire-reports/*.xml')

    html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>单测报告</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #4CAF50; color: white; }
.pass { color: green; }
.fail { color: red; }
</style></head><body>
<h1>单元测试报告</h1>
<table><tr><th>测试类</th><th>总数</th><th>通过</th><th>失败</th><th>状态</th></tr>
'''

    for f in xml_files:
        try:
            tree = ET.parse(f)
            root = tree.getroot()
            name = root.get('name', 'unknown')
            tests = root.get('tests', '0')
            failures = root.get('failures', '0')
            errors = root.get('errors', '0')
            passed = int(tests) - int(failures) - int(errors)
            status = 'PASS' if int(failures) == 0 and int(errors) == 0 else 'FAIL'
            status_class = 'pass' if status == 'PASS' else 'fail'
            html += f'<tr><td>{name}</td><td>{tests}</td><td>{passed}</td><td>{failures}</td><td class="{status_class}">{status}</td></tr>'
        except:
            pass

    html += '</table></body></html>'

    # 确保目录存在
    os.makedirs('test-reports', exist_ok=True)

    with open('test-reports/index.html', 'w', encoding='utf-8') as out:
        out.write(html)

    print(f'Generated test report with {len(xml_files)} test files')

if __name__ == '__main__':
    generate_test_report()
