#!/usr/bin/env python3
"""
ch04.ipynb의 모든 텍스트를 확실하게 검은색으로 설정
"""
import json
import re

with open('ch04.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

변경_카운트 = 0

for cell in notebook['cells']:
    if 'source' in cell and cell['cell_type'] == 'code':
        source_text = ''.join(cell['source'])
        original = source_text
        
        # 1. 중복 textfont 제거: textfont=dict(color='black'),\n    textfont=dict(...) 
        source_text = re.sub(
            r"textfont=dict\(color='black'\),\s*\n\s+textfont=dict\(([^)]+)\)",
            r"textfont=dict(\1)",
            source_text
        )
        
        # 2. textfont 내에서 color 확인 및 black 설정
        def fix_textfont(match):
            content = match.group(1)
            # color가 있으면 black으로 변경
            if 'color=' in content:
                content = re.sub(r"color='[^']*'", "color='black'", content)
            # color가 없으면 추가
            else:
                if content.strip().endswith(','):
                    content = content.rstrip(', ') + ", color='black'"
                else:
                    content = content + ", color='black'"
            return f"textfont=dict({content})"
        
        source_text = re.sub(r"textfont=dict\(([^)]+)\)", fix_textfont, source_text)
        
        # 3. font=dict 내의 white도 black으로
        source_text = re.sub(
            r"(font=dict\([^)]*?)color='white'",
            r"\1color='black'",
            source_text
        )
        
        # 4. font=dict 내에 color가 없으면 black 추가
        def fix_font(match):
            content = match.group(1)
            if 'color=' not in content:
                if content.strip().endswith(','):
                    content = content.rstrip(', ') + ", color='black'"
                else:
                    # size=11 같은 경우
                    content = content + ", color='black'"
            return f"font=dict({content})"
        
        source_text = re.sub(r"font=dict\(([^)]+)\)", fix_font, source_text)
        
        if source_text != original:
            변경_카운트 += 1
            cell['source'] = source_text.split('\n')
            cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line 
                             for i, line in enumerate(cell['source'])]

with open('ch04.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"✅ 텍스트 색상 확실하게 검은색으로 수정!")
print(f"   - {변경_카운트}개 셀 수정됨")
print("   - 모든 textfont/font에 color='black' 설정")
print("   - 중복 textfont 제거됨")
