#!/usr/bin/env python3
"""
ch04.ipynb의 textfont 들여쓰기 수정 및 size 추가
"""
import json

with open('ch04.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

변경_카운트 = 0

for cell in notebook['cells']:
    if 'source' in cell and cell['cell_type'] == 'code':
        modified = False
        
        for i, line in enumerate(cell['source']):
            # textfont=dict(color='black')를 찾아서 size 추가
            if 'textfont=dict(color=' in line and 'size=' not in line:
                # color만 있는 경우 size 추가
                cell['source'][i] = line.replace(
                    "textfont=dict(color='black')",
                    "textfont=dict(size=12, color='black')"
                )
                modified = True
            
            # 잘못된 들여쓰기 수정: "    textfont=" → "            textfont="
            if line.strip().startswith('textfont=') and not line.startswith('            textfont='):
                # 앞의 공백 세기
                stripped = line.lstrip()
                current_spaces = len(line) - len(stripped)
                # 12칸 들여쓰기로 맞추기 (marker, text 등과 같은 레벨)
                if current_spaces < 12:
                    cell['source'][i] = '            ' + stripped
                    modified = True
        
        if modified:
            변경_카운트 += 1

with open('ch04.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"✅ textfont 수정 완료!")
print(f"   - {변경_카운트}개 셀 수정됨")
print("   - size 없는 textfont에 size=12 추가")
print("   - 들여쓰기 정리")
