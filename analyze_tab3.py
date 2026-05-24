#!/usr/bin/env python3
import re

# 读取文件
with open('/workspace/mdcx/views/MDCx.ui', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找tab_3区域
tab3_start = content.find('<widget class="QWidget" name="tab_3">')
tab3_end = content.find('<widget class="QWidget" name="tab_4">', tab3_start)
if tab3_end == -1:
    tab3_end = content.find('</widget>', content.find('<widget class="QWidget" name="tab_6">', tab3_start))

tab3_content = content[tab3_start:tab3_end]
print("=" * 80)
print("Analyzing tab_3 groupBox positions...")
print("=" * 80)

# 查找所有groupBox
groupbox_pattern = re.compile(
    r'<widget class="QGroupBox" name="(groupBox_\d+)">\s*'
    r'<property name="geometry">\s*'
    r'<rect>\s*'
    r'<x>(\d+)</x>\s*'
    r'<y>(\d+)</y>\s*'
    r'<width>(\d+)</width>\s*'
    r'<height>(\d+)</height>\s*'
    r'</rect>\s*'
    r'</property>\s*'
    r'(?:.*?<property name="title">\s*<string>(.*?)</string>\s*</property>)?',
    re.DOTALL
)

groupboxes = []
for match in groupbox_pattern.finditer(tab3_content):
    name, x, y, w, h, title = match.groups()
    y = int(y)
    h = int(h)
    title = title or name
    groupboxes.append({
        'name': name,
        'title': title,
        'y': y,
        'height': h,
        'end_y': y + h
    })

# 按原始y位置排序
groupboxes.sort(key=lambda x: x['y'])

print("\nOriginal positions:")
print("-" * 80)
for i, gb in enumerate(groupboxes):
    print(f"{i+1}. {gb['name']} [{gb['title']}]: y={gb['y']}, h={gb['height']}, end={gb['end_y']}")

# 检查重叠
print("\nChecking for overlaps...")
overlaps = []
for i in range(len(groupboxes)-1):
    current = groupboxes[i]
    next_gb = groupboxes[i+1]
    if next_gb['y'] < current['end_y']:
        overlaps.append((current, next_gb))
        print(f"⚠️  OVERLAP: {current['name']} ends at {current['end_y']}, {next_gb['name']} starts at {next_gb['y']}")

if not overlaps:
    print("✅ No overlaps found!")

# 计算新位置
print("\nCalculating new positions...")
current_y = 20  # 从最上面开始
spacing = 20  # 组间间距
new_positions = []
for gb in groupboxes:
    new_positions.append({
        **gb,
        'new_y': current_y,
        'new_end': current_y + gb['height']
    })
    current_y += gb['height'] + spacing

print("\nNew positions:")
print("-" * 80)
for i, gb in enumerate(new_positions):
    print(f"{i+1}. {gb['name']} [{gb['title']}]: old_y={gb['y']} -> new_y={gb['new_y']}")

total_height = new_positions[-1]['new_end'] + 100  # 额外留出空间
print(f"\nRequired scroll area height: {total_height}")

# 现在查找滚动区域的高度设置
scrollarea_pattern = re.compile(r'<widget class="QWidget" name="scrollAreaWidgetContents_mingming">\s*<property name="geometry">\s*<rect>\s*<x>(\d+)</x>\s*<y>(\d+)</y>\s*<width>(\d+)</width>\s*<height>(\d+)</height>')

scrollarea_match = scrollarea_pattern.search(tab3_content)
if scrollarea_match:
    x, y, w, old_h = scrollarea_match.groups()
    print(f"\nCurrent scroll area height: {old_h}")

# 现在让我们生成修复方案
print("\n" + "=" * 80)
print("Generating fix...")
print("=" * 80)

# 读取完整文件用于修复
with open('/workspace/mdcx/views/MDCx.ui', 'r', encoding='utf-8') as f:
    full_content = f.read()

fixed_content = full_content

# 应用新位置
for gb in new_positions:
    # 查找并替换这个groupBox的y坐标
    pattern = re.compile(
        fr'(<widget class="QGroupBox" name="{gb["name"]}">\s*'
        r'<property name="geometry">\s*'
        r'<rect>\s*'
        r'<x>\d+</x>\s*'
        r')<y>\d+</y>'
    )
    replacement = fr'\1<y>{gb["new_y"]}</y>'
    fixed_content = pattern.sub(replacement, fixed_content)

# 更新滚动区域高度
scroll_pattern = re.compile(
    r'(<widget class="QWidget" name="scrollAreaWidgetContents_mingming">\s*'
    r'<property name="geometry">\s*'
    r'<rect>\s*'
    r'<x>\d+</x>\s*'
    r'<y>\d+</y>\s*'
    r'<width>\d+</width>\s*'
    r')<height>\d+</height>'
)
fixed_content = scroll_pattern.sub(fr'\1<height>{total_height}</height>', fixed_content)

# 写入修复后的文件
with open('/workspace/mdcx/views/MDCx.ui', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("\n✅ Fix applied successfully!")
print(f"   - {len(new_positions)} groupBox positions updated")
print(f"   - Scroll area height updated from {old_h} to {total_height}")
