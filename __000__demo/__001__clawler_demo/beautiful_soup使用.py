"""
BeautifulSoup介绍：
BeautifulSoup 是一个 HTML/XML 解析库，可用于从网页中提取结构化数据。它将原始 HTML 文本转换为“树形结构”，方便定位、遍历和提取标签内容，常与 requests 联合使用。

Author: danke
Date: 2026/11/4 17:04
"""

from bs4 import BeautifulSoup

# 假设有一段 HTML 内容
html = """
<html>
  <head><title>中药方剂示例</title></head>
  <body>
    <h1>方剂列表</h1>
    <div class="formula">
      <h2>葛根汤</h2>
      <p>功效：解肌发表，升阳止泻。</p>
    </div>
    <div class="formula">
      <h2>麻黄汤</h2>
      <p>功效：发汗解表，宣肺平喘。</p>
    </div>
  </body>
</html>
"""

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html, 'html.parser')

# 提取标题
title = soup.title.string
print("网页标题：", title)

# 提取所有方剂名称
names = soup.find_all('h2')
print("\n方剂名称：")
for tag in names:
    print("-", tag.get_text())

# 提取所有功效描述
effects = soup.find_all('p')
print("\n功效描述：")
for tag in effects:
    print("-", tag.get_text())