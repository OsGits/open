#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 https://www.anpn.cc/api/t.php 获取影视列表，
解析标题与链接，按现有格式更新 /workspace/影视目录.md

现有列表格式：
    - 标题  
      <small>`链接`</small>
"""

import re
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

API_URL = "https://www.anpn.cc/api/t.php"
MD_FILE = Path("/workspace/影视目录.md")


def fetch_api() -> str:
    """拉取 API 原始文本。"""
    req = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0 Safari/537.36",
            "Accept": "text/plain,text/html,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    # 尝试 utf-8，失败则回退 gbk
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def simplify_title(title: str) -> str:
    """从原始文件名中提取简洁标题。策略：
    1) 若包含书名号《...》，以书名号内容作为主标题，其他丢弃
    2) 去掉前缀图标与分类词
    3) 去掉所有方括号/中文方括号的内容
    4) 去掉 SxxExx、季集范围
    5) 去掉文件扩展名与末尾编码关键字
    6) 去掉 "作者：xxx"、"by xxx"
    """
    t = title.strip()

    # 0) 书名号优先：若存在《...》，以第一个书名号内容为主标题
    m_book = re.search(r"《([^》]+)》", t)
    if m_book:
        inner = m_book.group(1).strip()
        if inner:
            t = inner  # 只用书名号内的内容，之后走常规清洗

    # 1) 去掉前缀图标与分类词
    t = re.sub(r"^(📺|🎬|📀|🎞️|🎥)\s*", "", t)
    t = re.sub(r"^(电视剧[：:]|电影[：:]|剧[：:]|影[：:])", "", t)

    # 2) 去掉 tmdbid-xxx（先单独干掉，防止后续处理残留）
    t = re.sub(r"[\[\（]?\s*tmdbid-\d+\s*[\]\）]?", "", t, flags=re.IGNORECASE)

    # 3) 反复去掉所有方括号/中文方括号内容（包括嵌套或紧邻的）
    #    例如：【S01全】【4K.HDR】、[1080P]、（附番外）等
    prev = None
    loops = 0
    while prev != t and loops < 20:
        prev = t
        t = re.sub(r"[【\[\（][^】\]\）]{0,80}[】\]\）]", " ", t)
        loops += 1

    # 4) 去掉 Sxx / SxxExx / SxxExx-SyyEyy 这类季集范围
    #    注意要覆盖 "S01E01-E10" 这样的写法
    t = re.sub(
        r"(?i)\b[s]\d{1,2}(?:[e]\d{1,3})?(?:\s*[-~–]\s*[s]?\d{0,2}[e]?\d{0,3})?\b",
        "", t,
    )
    # 以及单独出现的 Exx
    t = re.sub(r"(?i)\b[e]\d{1,3}\b", "", t)
    # 去掉孤立的 "-E10"、"-E11" 之类
    t = re.sub(r"(?i)\s*[-–~]\s*[e]\d{1,3}\b", "", t)

    # 5) 去掉文件扩展名（末尾 .txt / .zip / .mp4 / .mkv 等）
    t = re.sub(r"\.(txt|zip|mp4|mkv|m4v|avi|rmvb|rar|7z)$", "", t,
               flags=re.IGNORECASE)

    # 5b) 末尾残留的容器/编码关键字（MPEG / MP4 / AAC / HDR / ...）
    t = re.sub(
        r"\s*\b(MPEG|MP4|MKV|AVI|AAC|AC3|EAC3|DTS|HDR|SDR|1080P|2160P|4K|8K|HEVC|x264|x265|Blu-ray|BLURAY|WEBDL|WEBRIP|DVDRIP|HDTV|REMUX|FLAC)\b\s*$",
        "", t, flags=re.IGNORECASE,
    )

    # 6) 去掉 "作者：xxx" / "by xxx" 等次要信息
    t = re.sub(r"作者[:：]\s*\S+(?:\s+by\s+\S+)?", "", t, flags=re.IGNORECASE)
    # "xxx by xxx"、"xxxbyxxx"（中文常无空格）
    t = re.sub(r"\s*by\s*\S+.*$", "", t, flags=re.IGNORECASE)

    # 7) 清理多余空白、标点
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"^[\s,，\-_·【\[]+", "", t)
    t = re.sub(r"[\s,，\-_·【\]]+$", "", t)
    t = t.strip(" 　·—-_,，。.")

    # 8) 最终再扫一次残留的空方括号 / 方括号半截
    t = re.sub(r"[【\[]\s*[】\]]", "", t)
    t = re.sub(r"[【\]]", "", t)
    t = t.strip()

    return t


def parse_items(text: str):
    """
    从 API 返回文本中解析出 (title, url) 对。
    兼容两种格式：
        HTML: <div class="item"> ... <span class="label">文件名称:</span>
                        <span class="value">...</span>
                        <span class="label">链接:</span>
                        <span class="value"><a href="URL">URL</a></span> ...
        纯文本:
                文件名称: ...
                链接:[URL](URL)
    """
    items = []

    # ---------- HTML 格式（优先，当前 API 默认返回 HTML） ----------
    # 1) 切分出每个 <div class="item"> ... </div>
    item_blocks = re.findall(
        r'<div\s+class\s*=\s*"item">(.*?)</div>\s*(?=<div\s+class\s*=\s*"item"|$)',
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if not item_blocks:
        # 更宽松的切分：用 class="item" 作为锚点
        parts = re.split(r'<div\s+class\s*=\s*"item"', text, flags=re.IGNORECASE)
        item_blocks = [p for p in parts[1:] if p.strip()]

    seen_keys = set()
    for block in item_blocks:
        # 标题：优先从 <span class="label">文件名称:</span><span class="value">...</span>
        title = None
        m = re.search(
            r'<span[^>]*class\s*=\s*"label"[^>]*>\s*文件名称\s*[:：]?\s*</span>'
            r'\s*<span[^>]*class\s*=\s*"value"[^>]*>(.*?)</span>',
            block,
            re.DOTALL | re.IGNORECASE,
        )
        if not m:
            # 回退：任意包含 "文件名称" 的文本
            m = re.search(r'文件名称\s*[:：]\s*([^<\n]+)', block)
        if m:
            title = m.group(1).strip()
            # 去掉 HTML tag
            title = re.sub(r"<[^>]+>", "", title)
            title = re.sub(r"[`*_]", "", title)

        # 链接：优先从 <a href="URL"> 提取
        url = None
        m = re.search(
            r'<a[^>]+href\s*=\s*"([^"]+)"[^>]*>',
            block,
            re.IGNORECASE,
        )
        if not m:
            # 回退：在 "链接:" 之后紧跟的 URL
            m = re.search(r'链接\s*[:：]\s*(?:\[(.+?)\])?', block)
            if m:
                inner = m.group(1) or m.group(0)
                m2 = re.search(r"(https?://[^\s\"'`<>)]+)", inner)
                if m2:
                    url = m2.group(1).strip()
        else:
            url = m.group(1).strip()

        if title and url:
            clean_title = simplify_title(title)
            if clean_title and (clean_title, url) not in seen_keys:
                seen_keys.add((clean_title, url))
                items.append((clean_title, url))

    if items:
        return items

    # ---------- 纯文本格式（兼容旧 API） ----------
    current_title = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        m = re.match(r"(?:文件名称|文件名|名称|标题)[:：]\s*(.+)", line)
        if m:
            current_title = m.group(1).strip().strip("*_`")
            continue

        if current_title is not None:
            m_link = re.search(r"\[(https?://[^\]\s]+)\]\s*\([^\)]+\)", line)
            if not m_link:
                m_link = re.search(r"`(https?://[^`\s]+)`", line)
            if not m_link:
                m_link = re.search(r"(https?://[^\s\"'`<>)]+)", line)
            if m_link:
                url = m_link.group(1).strip()
                clean = simplify_title(current_title)
                if clean and url:
                    items.append((clean, url))
                current_title = None

    # 去重
    seen = set()
    uniq = []
    for t, u in items:
        k = (t, u)
        if k in seen:
            continue
        seen.add(k)
        uniq.append(k)
    return uniq


def build_list_block(items) -> str:
    """按现有格式生成列表块。"""
    lines = []
    for title, url in items:
        lines.append(f"- {title}  ")
        lines.append(f"  <small>`{url}`</small>")
    return "\n".join(lines)


def update_markdown(items) -> bool:
    """把 items 写回 MD_FILE。返回是否有改动。"""
    text = MD_FILE.read_text(encoding="utf-8")

    # 1) 更新时间戳：匹配 "💡 更新时间：YYYY.MM.DD HH:MM:SS"
    now = datetime.now(timezone(timedelta(hours=8)))
    timestamp = now.strftime("%Y.%m.%d %H:%M:%S")
    new_header_line = f"> 💡 更新时间：{timestamp} 以下列表采用循环更新模式，内容会不定期更新替换"

    new_text = re.sub(
        r"> 💡 更新时间[：:].*?以下列表采用循环更新模式[，,].*?\n",
        new_header_line + "\n",
        text,
        count=1,
    )

    # 2) 替换列表区块：
    #    从 "### 📝 影视名称列表" 之后，到下一个二级/三级标题或 "---" 分隔符之前
    list_anchor = "### 📝 影视名称列表"
    if list_anchor not in new_text:
        raise RuntimeError(f"未在 {MD_FILE} 中找到 '{list_anchor}' 锚点")

    new_block = build_list_block(items)

    # 匹配：list_anchor 之后的空行 + 列表内容，直到遇到 "---" 或 "#" 标题
    pattern = re.compile(
        r"(" + re.escape(list_anchor) + r"\n\n)"
        r".*?"
        r"(?=\n---|$\n?#|$\Z)",
        re.DOTALL,
    )

    replacement = r"\1" + new_block + "\n\n"
    new_text, n_subs = pattern.subn(replacement, new_text, count=1)

    if n_subs == 0:
        # 兜底：直接在锚点后重写整段
        before, after = text.split(list_anchor, 1)
        # 找 after 中下一个段落分隔符或标题
        m = re.search(r"\n---|$\n?#", after)
        tail = after[m.start():] if m else ""
        new_text = before + list_anchor + "\n\n" + new_block + "\n\n" + tail

    if new_text.strip() == text.strip():
        return False

    MD_FILE.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 开始更新影视列表…")
    try:
        raw = fetch_api()
    except Exception as exc:
        print(f"[ERROR] 拉取 API 失败: {exc}")
        return 1

    items = parse_items(raw)
    if not items:
        print("[WARN] 未解析到任何条目，跳过更新")
        return 1

    print(f"  -> 解析到 {len(items)} 条记录")

    try:
        changed = update_markdown(items)
    except Exception as exc:
        print(f"[ERROR] 写入 {MD_FILE.name} 失败: {exc}")
        return 1

    if changed:
        print(f"  -> 已更新 {MD_FILE}")
    else:
        print("  -> 内容无变化")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
