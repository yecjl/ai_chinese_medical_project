"""
爬取中医百科「中药大全」页面，提取每味药的名称和完整链接，保存为表格（CSV）

页面结构：
    <div class="p_content">
      <h2>解表药</h2>                       <- 大类
      <ol>
        <li>
          <strong>发散风寒药</strong>        <- 小类
          <ul>
            <li><a href="/wiki/羌活">羌活</a></li>   <- 名称 + 相对链接
            ...

依赖：见项目根目录 requirements.txt（pip install -r requirements.txt）
"""
import csv
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# URL = "https://zhongyibaike.com/wiki/%E4%B8%AD%E8%8D%AF%E5%A4%A7%E5%85%A8"
URL = "https://zhongyibaike.com/wiki/%E4%B8%AD%E5%8C%BB%E6%96%B9%E5%89%82"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
# SAVE_PATH = Path(__file__).parent / "中药大全.csv"
SAVE_PATH = Path(__file__).parent / "中药方剂.csv"


def fetch(url: str) -> str:
    """请求网页，返回 HTML 文本"""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def parse(html: str) -> list[dict]:
    """解析 HTML，返回 [{大类, 小类, 名称, 链接}, ...]"""
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("div.p_content")  # 正文区域，避开导航栏和页脚的链接

    rows = []
    category = ""
    # 按顺序遍历正文的直接子元素：遇到 h2 记下大类，遇到列表就提取其中的药
    # 注意：有的大类下是 <ol>（带 <strong> 小类），有的直接是 <ul>（没有小类）
    for element in content.find_all(recursive=False):
        if element.name == "h2":
            category = element.get_text(strip=True)     # 大类，如「解表药」
            continue
        if element.name not in ("ol", "ul"):
            continue

        for a in element.select("a[href]"):             # 列表里的每味药
            rows.append({
                "大类": category,
                "小类": find_sub_category(a) or category,   # 没有小类时用大类代替
                "名称": a.get_text(strip=True),
                # 相对链接 /wiki/羌活 -> 完整链接 https://zhongyibaike.com/wiki/羌活
                "链接": urljoin(URL, a["href"]),
            })
    return rows


def find_sub_category(a) -> str:
    """向上找包含 <strong> 的 <li>，其中 strong 的文字就是小类名"""
    for li in a.find_parents("li"):
        strong = li.find("strong", recursive=False)
        if strong:
            return strong.get_text(strip=True)
    return ""


def save_csv(rows: list[dict], path: Path) -> None:
    """保存为 CSV；utf-8-sig 编码让 Excel 打开时中文不乱码"""
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["大类", "小类", "名称", "链接"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    html = fetch(URL)
    rows = parse(html)
    save_csv(rows, SAVE_PATH)

    print(f"共获取 {len(rows)} 条数据，已保存到: {SAVE_PATH}")
    for row in rows[:5]:
        print(row)


if __name__ == "__main__":
    main()
