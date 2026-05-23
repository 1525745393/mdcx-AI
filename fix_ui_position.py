#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open('mdcx/views/MDCx.ui', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('mdcx/views/MDCx.ui', 'w', encoding='utf-8') as f:
    for line in lines:
        # 修改 groupBox_vsmeta 的位置
        if '<y>2980</y>' in line and 'groupBox_vsmeta' in ''.join(lines[max(0, lines.index(line)-5):lines.index(line)+5]):
            line = line.replace('<y>2980</y>', '<y>3300</y>')
        # 修改 groupBox_67 的位置
        elif '<y>3290</y>' in line and 'groupBox_67' in ''.join(lines[max(0, lines.index(line)-5):lines.index(line)+5]):
            line = line.replace('<y>3290</y>', '<y>3440</y>')
        # 增加 scrollAreaWidgetContents_mingming 的高度
        elif '<height>3660</height>' in line and 'scrollAreaWidgetContents_mingming' in ''.join(lines[max(0, lines.index(line)-5):lines.index(line)+5]):
            line = line.replace('<height>3660</height>', '<height>3720</height>')
        f.write(line)

print("UI 文件位置已修复！")
