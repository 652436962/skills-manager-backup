#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建 CHANGELOG 的版本索引与锚点。

用法:
    python3 sync_changelog_index.py [docs/CHANGELOG.md] [--dry-run] [--backup]

规则:
    - 索引放在 "# CHANGELOG" 之后，表格列为: 版本 | 日期/说明
    - 索引行链接到显式锚点 <a id="vx.y.z"></a>，锚点插在版本小节标题前
    - 索引按版本号倒序；保留旧索引行中的说明文字(含 git 号)
    - 不改动版本小节正文与标题

参数:
    --dry-run   只打印重建结果到 stdout，不写文件
    --backup    写文件前先备份为 <path>.bak
"""

import argparse
import re
import shutil
import sys

INDEX_TITLE = '## 版本索引'
# 版本号主体：V 开头，后跟数字/字母/点/连字符（兼容 V1.3.7-beta 之类）
VER = r'V[0-9][0-9A-Za-z.\-]*'
ANCHOR_RE = re.compile(r'^<a id="(v[0-9][0-9A-Za-z.\-]*)"></a>\s*$')
SECTION_RE = re.compile(r'^## \[' + VER + r'\]\s*-\s*(.*)$')
SECTION_VER_RE = re.compile(r'^## \[(' + VER + r')\]')
INDEX_ROW_RE = re.compile(r'^\|\s*\[(' + VER + r')\]\(#[^)]*\)\s*\|\s*(.*?)\s*\|\s*$')


def version_key(version):
    """返回排序键：数字段按数值、后缀（如 beta）排在正式版之后。"""
    core = version[1:]
    nums = tuple(int(n) for n in re.findall(r'\d+', core)) or (0,)
    suffix = re.sub(r'[\d.]', '', core).lower()
    # 空后缀=正式版，用 (1,'') 使其在倒序中排在同版本预发布之前
    suffix_key = (1, '') if suffix == '' else (0, suffix)
    return (nums, suffix_key)


def parse_args():
    parser = argparse.ArgumentParser(description='重建 CHANGELOG 的版本索引与锚点')
    parser.add_argument('path', nargs='?', default='docs/CHANGELOG.md',
                        help='CHANGELOG 文件路径（默认 docs/CHANGELOG.md）')
    parser.add_argument('--dry-run', action='store_true',
                        help='只打印结果，不写文件')
    parser.add_argument('--backup', action='store_true',
                        help='写文件前备份为 <path>.bak')
    return parser.parse_args()


def main():
    args = parse_args()
    path = args.path

    try:
        with open(path, encoding='utf-8') as handle:
            raw = handle.read()
    except OSError as exc:
        sys.exit(f'读取失败 {path}: {exc}')

    # 统一换行符：兼容 Windows CRLF 与旧 Mac CR
    lines = raw.replace('\r\n', '\n').replace('\r', '\n').split('\n')

    # 1. 先保留旧索引里的说明（含 git 号），重建时沿用
    old_desc = {}
    for line in lines:
        match = INDEX_ROW_RE.match(line.strip())
        if match:
            old_desc[match.group(1)] = match.group(2).strip()

    # 2. 删除旧的索引区块：从 "## 版本索引" 到下一个二级标题或锚点为止
    #    避免误删索引与首个版本小节之间的其它二级章节
    cleaned = []
    index = 0
    while index < len(lines):
        if lines[index].strip() == INDEX_TITLE:
            index += 1
            while index < len(lines):
                stripped = lines[index].strip()
                if stripped.startswith('## ') or ANCHOR_RE.match(lines[index]):
                    break
                index += 1
            continue
        cleaned.append(lines[index])
        index += 1

    # 3. 删除旧锚点，稍后统一重建
    cleaned = [line for line in cleaned if not ANCHOR_RE.match(line)]

    # 4. 收集版本小节（版本与标题行中的位置）
    sections = []
    for position, line in enumerate(cleaned):
        match = SECTION_VER_RE.match(line)
        if match:
            version = match.group(1)
            desc = SECTION_RE.match(line)
            sections.append((version, desc.group(1) if desc else '', position))
    if not sections:
        sys.exit('未找到版本小节（格式应为: ## [Vx.y.z] - 日期）')

    # 5. 重复版本检测：一个版本只允许一个小节，否则锚点会重复
    counts = {}
    for version, _, _ in sections:
        counts[version] = counts.get(version, 0) + 1
    duplicates = sorted(v for v, n in counts.items() if n > 1)
    if duplicates:
        print('警告: 发现重复版本小节，锚点会重复 -> ' + ', '.join(duplicates),
              file=sys.stderr)

    # 6. 重建索引（版本号倒序，优先用旧说明）
    ordered = sorted(sections, key=lambda item: version_key(item[0]), reverse=True)
    index_lines = [INDEX_TITLE, '', '| 版本 | 日期/说明 |', '| ---- | --------- |']
    for version, heading_desc, _ in ordered:
        desc = old_desc.get(version, heading_desc).strip()
        index_lines.append(f'| [{version}](#{version.lower()}) | {desc} |')
    index_lines.append('')

    # 7. 在版本标题前插锚点（倒序插入，避免下标偏移）
    for version, _, position in sorted(sections, key=lambda item: item[2], reverse=True):
        cleaned.insert(position, f'<a id="{version.lower()}"></a>')

    # 8. 组装：索引插到 "# CHANGELOG" 之后
    output = []
    inserted = False
    for line in cleaned:
        output.append(line)
        if not inserted and line.strip() == '# CHANGELOG':
            output.append('')
            output.extend(index_lines)
            inserted = True
    if not inserted:
        output = ['# CHANGELOG', ''] + index_lines + cleaned

    # 9. 连续空行最多保留 2 行
    result = []
    blanks = 0
    for line in output:
        if line.strip() == '':
            blanks += 1
            if blanks > 2:
                continue
        else:
            blanks = 0
        result.append(line)

    content = '\n'.join(result).rstrip('\n') + '\n'

    if args.dry_run:
        sys.stdout.write(content)
        print(f'[dry-run] 共 {len(sections)} 个版本，未写入文件', file=sys.stderr)
        return

    if args.backup:
        shutil.copyfile(path, path + '.bak')
        print(f'已备份: {path}.bak', file=sys.stderr)

    with open(path, 'w', encoding='utf-8') as handle:
        handle.write(content)

    print(f'完成: {len(sections)} 个版本 -> {path}')
    for version, _, _ in ordered:
        print(f'  #{version.lower()}  {version}')


if __name__ == '__main__':
    main()
