"""
遍历「中药方剂.csv」，逐个爬取方剂详情页，每个方剂保存为一个 txt 文件

输入：同目录下的 中药方剂.csv（由 中医方剂.py 生成，列：大类,小类,名称,链接）
输出：同目录下的 formula/<方剂名称>.txt

详情页结构：
    <div class="p_content">
      <div class="card-panel">
        <h2>麻黄汤的药方</h2>          <- 板块标题
        <h3>出处</h3>                  <- 小标题
        <p>《伤寒论》</p>              <- 内容
        <ul><li>1、...</li></ul>       <- 列表内容
      </div>
      ...

特点：
    - 同一方剂可能出现在多个分类中，按名称去重，只爬一次
    - 通过 RESUME 参数选择模式：
        True  断点续爬：已经存在的 txt 跳过，只爬还没爬的（中断后重新运行即可接着爬）
        False 从头开始：所有方剂重新爬取，覆盖已有的 txt
    - 每次请求之间暂停一下，避免给网站造成压力

依赖：见项目根目录 requirements.txt（pip install -r requirements.txt）
"""
import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "中药方剂.csv"
SAVE_DIR = BASE_DIR / "formula"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
SLEEP_SECONDS = 1   # 每次请求后的等待时间（秒）
RETRY_TIMES = 3     # 请求失败时的重试次数
RESUME = True       # True：断点续爬，跳过已爬取的方剂；False：从头开始，全部重新爬取并覆盖


def read_csv(path: Path) -> list[dict]:
    """读取 CSV，按名称去重，返回 [{大类, 小类, 名称, 链接}, ...]"""
    with path.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    unique = {}
    for row in rows:
        unique.setdefault(row["名称"], row)   # 同名只保留第一次出现的
    return list(unique.values())


def fetch(url: str) -> str:
    """请求网页，失败自动重试，返回 HTML 文本"""
    for attempt in range(1, RETRY_TIMES + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text
        except requests.RequestException:
            if attempt == RETRY_TIMES:
                raise
            time.sleep(attempt * 2)   # 等一会儿再重试，等待时间逐次加长


def parse(html: str) -> str:
    """提取正文，整理成便于阅读的纯文本"""
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("div.p_content")
    if content is None:
        return ""

    lines = []
    for panel in content.select("div.card-panel"):   # 跳过广告 <ins>，只取内容卡片
        for element in panel.find_all(["h2", "h3", "p", "li"]):
            # 用 "" 拼接，避免「麻黄 9克」被 <a> 标签拆成两行
            text = element.get_text("", strip=True)
            if not text:
                continue
            if element.name == "h2":
                lines.append(f"\n## {text}")
            elif element.name == "h3":
                lines.append(f"\n【{text}】")
            else:
                lines.append(text)
    return "\n".join(lines).strip()


def safe_filename(name: str) -> str:
    """去掉文件名中不允许的字符"""
    return re.sub(r'[\\/:*?"<>|\s]', "_", name)


def save_txt(row: dict, text: str, path: Path) -> None:
    """保存为 txt，开头写上方剂的基本信息"""
    header = (
        f"名称：{row['名称']}\n"
        f"分类：{row['大类']} - {row['小类']}\n"
        f"链接：{row['链接']}\n"
    )
    # 先写临时文件，写完再改名：如果写到一半被中断，不会留下残缺的 txt，
    # 避免断点续爬时把残缺文件当成「已爬取」而跳过
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(header + "\n" + text + "\n", encoding="utf-8")
    tmp_path.replace(path)


def txt_path(row: dict) -> Path:
    """方剂对应的 txt 保存路径"""
    return SAVE_DIR / f"{safe_filename(row['名称'])}.txt"


def main(resume: bool = RESUME):
    SAVE_DIR.mkdir(exist_ok=True)
    rows = read_csv(CSV_PATH)
    total = len(rows)

    if resume:
        # 断点续爬：过滤掉已经有 txt 的方剂，只爬剩下的
        rows = [row for row in rows if not txt_path(row).exists()]
        print(f"断点续爬：共 {total} 个方剂，已爬取 {total - len(rows)} 个，本次需爬取 {len(rows)} 个")
    else:
        print(f"从头开始：共 {total} 个方剂，全部重新爬取（覆盖已有文件）")

    success, failed = 0, []
    # 进度条按全部方剂计算：total 是总数，initial 是已爬取的数量，
    # 断点续爬时进度条直接从已完成的位置开始，而不是从 0 开始
    progress = tqdm(rows, desc="爬取方剂", unit="个", total=total, initial=total - len(rows))
    for row in progress:
        name = row["名称"]
        progress.set_postfix(当前=name, 成功=success, 失败=len(failed))

        try:
            text = parse(fetch(row["链接"]))
            if not text:
                raise ValueError("页面中没有找到正文")
            save_txt(row, text, txt_path(row))
            success += 1
        except Exception:
            failed.append(name)

        time.sleep(SLEEP_SECONDS)

    progress.close()
    print(f"完成：成功 {success}，失败 {len(failed)}，保存目录: {SAVE_DIR}")
    if failed:
        print("失败的方剂（用断点续爬模式重新运行即可重试）：", "、".join(failed))


if __name__ == "__main__":
    main()
