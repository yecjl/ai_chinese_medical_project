"""
爬虫基础示例：爬取百度首页

步骤：
1. 准备 URL 和请求头（User-Agent 伪装成浏览器）
2. 发送 GET 请求
3. 处理响应（状态码、编码）
4. 解析/保存数据

依赖：pip install requests
"""
import re
from pathlib import Path

import requests

# 1. 目标网址
URL = "https://www.baidu.com"

# 请求头：不带 User-Agent 时百度只返回一个简化版页面
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch(url: str) -> str:
    """发送请求，返回网页 HTML 文本"""
    # 2. 发送 GET 请求，设置超时防止一直卡住
    response = requests.get(url, headers=HEADERS, timeout=10)

    # 3. 检查状态码，非 2xx 会抛出异常
    response.raise_for_status()
    print("状态码:", response.status_code)

    # 设置正确的编码，避免中文乱码
    # 百度首页是 utf-8；apparent_encoding 自动猜测在这里会猜错（如 Windows-1254）
    response.encoding = "utf-8"
    print("编码:", response.encoding)

    return response.text


def main():
    html = fetch(URL)

    # 4.1 简单解析：用正则提取网页标题
    match = re.search(r"<title>(.*?)</title>", html, re.S)
    title = match.group(1).strip() if match else "未找到标题"
    print("网页标题:", title)
    print("网页长度:", len(html))

    # 4.2 保存到本地文件（与本脚本同目录） 
    save_path = Path(__file__).parent / "baidu.html"
    save_path.write_text(html, encoding="utf-8")
    print("已保存到:", save_path)


if __name__ == "__main__":
    main()
