#!/usr/bin/env python
"""
生成 OLED 用的 8x16 ASCII 字库 (oledfont.h)

字库格式 (与 SSD1306 的页寻址天然对应):
    每个字符 16 字节
      byte[0..7]  -> 第 0 页 (点阵第 0~7 行), 每字节一列, bit7 是该列最上面一个点
      byte[8..15] -> 第 1 页 (点阵第 8~15 行), 同上

    ASCII 32(' ') ~ 126('~') 共 95 个字符, 索引 = 字符码 - 32

用法:
    python tools/gen_font.py            # 只预览
    python tools/gen_font.py --write    # 预览并写出 BSP/Inc/oledfont.h
"""

import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 8, 16
FIRST, LAST = 32, 126
THRESHOLD = 128          # 灰度阈值

# 选型依据 (advance 必须 <= 8 px, 否则相邻字符会粘连):
#   Consolas 15 -> advance = 8.00, 大写高 10 px  <- 最高且不超宽
#   基线固定在 row 13, 让下伸部(g/y/p/q)有地方放
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_SIZE = 15
BASELINE  = 13
STRETCH   = 1.15         # 纵向拉伸: 让字填满 16 px 格, 同时下伸部不被裁掉
                         # (再大就会切掉 g/y/p/q 的尾巴)


def pick_font():
    try:
        return ImageFont.truetype(FONT_PATH, FONT_SIZE), FONT_PATH, FONT_SIZE
    except Exception as e:
        raise SystemExit(f"找不到字体 {FONT_PATH}: {e}")


def render_char(font, ch):
    """把一个字符画进 8x16 的位图, 返回二维 0/1 列表 rows[y][x]。"""
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)

    bbox = d.textbbox((0, 0), ch, font=font)
    x = (W - (bbox[2] - bbox[0])) // 2 - bbox[0]
    y = BASELINE - bbox[3]                     # 对齐基线, 而不是简单居中
    d.text((x, y), ch, fill=255, font=font)

    # 纵向拉伸, 并保持基线位置不变
    big = img.resize((W, int(round(H * STRETCH))), Image.LANCZOS)
    off = int(round(BASELINE * STRETCH)) - BASELINE
    img = big.crop((0, off, W, off + H))

    px = img.load()
    return [[1 if px[c, r] >= THRESHOLD else 0 for c in range(W)] for r in range(H)]


def to_bytes(rows):
    """把 rows 转成 SSD1306 页格式的 16 字节。

    关键: SSD1306 的 GDDRAM 里, 一个字节的 **bit0 对应页内最上面那一行**,
    bit7 对应最下面那一行(可对照 Adafruit_SSD1306 的 `1 << (y & 7)` 写法)。
    千万不要写成 1 << (7 - bit), 那样每个 8 像素高的页会被上下翻转,
    显示出来就是"能看出形状但整体是乱的"。
    """
    out = []
    for page in range(2):                # 2 页, 每页 8 行
        for col in range(W):
            b = 0
            for bit in range(8):
                if rows[page * 8 + bit][col]:
                    b |= (1 << bit)      # bit0 = 页内最上面一行
            out.append(b)
    return out


def preview(font, chars="A0abgXy%."):
    """在终端里用 ASCII art 预览, 确认字库没错再烧进板子。"""
    for ch in chars:
        rows = render_char(font, ch)
        print(f"--- {ch!r} ---")
        for r in rows:
            print("  " + "".join("#" if v else "." for v in r))
        print()


def main():
    font, path, size = pick_font()
    print(f"使用字体: {path}  (size={size})\n")

    preview(font)

    if "--write" not in sys.argv:
        print("(预览模式, 未写文件; 加 --write 生成头文件)")
        return

    lines = []
    lines.append("/**")
    lines.append("  * @file    oledfont.h")
    lines.append("  * @brief   8x16 ASCII 字库, 由 tools/gen_font.py 自动生成, 请勿手工修改")
    lines.append("  *")
    lines.append(f"  * 字体来源: {path} (size={size})")
    lines.append("  * 数据格式: 每字符 16 字节, 前 8 字节为第 0 页(0~7行),")
    lines.append("  *           后 8 字节为第 1 页(8~15行);")
    lines.append("  *           每字节一列, bit0 为该列最上面一行(SSD1306 原生顺序)")
    lines.append("  */")
    lines.append("")
    lines.append("#ifndef __OLEDFONT_H")
    lines.append("#define __OLEDFONT_H")
    lines.append("")
    lines.append("#include <stdint.h>")
    lines.append("")
    lines.append(f"/* ASCII 32~126 共 {LAST - FIRST + 1} 个字符, 索引 = 字符码 - 32 */")
    lines.append(f"const uint8_t oled_asc2_1608[{LAST - FIRST + 1}][16] = {{")

    for code in range(FIRST, LAST + 1):
        ch = chr(code)
        data = to_bytes(render_char(font, ch))
        body = ",".join(f"0x{b:02X}" for b in data)
        lines.append(f"  {{{body}}},  /* '{ch}' */")

    lines.append("};")
    lines.append("")
    lines.append("#endif /* __OLEDFONT_H */")

    out = r"BSP/Inc/oledfont.h"
    import os
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"已写出 {out}")


if __name__ == "__main__":
    main()
