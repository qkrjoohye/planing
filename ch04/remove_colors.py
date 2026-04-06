#!/usr/bin/env python3
"""
ch04.ipynb의 모든 그래프 색상을 검은색으로 변경하는 스크립트
"""
import json
import re

# 파일 읽기
with open('ch04.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

변경_카운트 = 0

# 각 셀을 순회하면서 색상 패턴 교체
for cell in notebook['cells']:
    if 'source' in cell and cell['cell_type'] == 'code':
        source_text = ''.join(cell['source'])
        original = source_text
        
        # 1. marker=dict(size=XX, color='#XXXXXX') → marker=dict(size=XX, color='white', line=dict(color='black', width=2))
        source_text = re.sub(
            r"marker=dict\(size=(\d+),\s*color='#[0-9A-F]{6}'\)",
            r"marker=dict(size=\1, color='white', line=dict(color='black', width=2))",
            source_text
        )
        
        # 2. marker=dict(size=XX, color=node['color']) → marker=dict(size=XX, color='white', line=dict(color='black', width=2))
        source_text = re.sub(
            r"marker=dict\(size=(\d+),\s*color=node\['color'\]\)",
            r"marker=dict(size=\1, color='white', line=dict(color='black', width=2))",
            source_text
        )
        
        # 3. marker=dict(size=XX, color=n.get('color', ...)) → marker=dict(size=XX, color='white', line=dict(color='black', width=2))
        source_text = re.sub(
            r"marker=dict\(size=(\d+),\s*color=n\.get\('color',\s*'#[0-9A-F]{6}'\)\)",
            r"marker=dict(size=\1, color='white', line=dict(color='black', width=2))",
            source_text
        )
        
        # 4. marker_color='#XXXXXX' → marker=dict(color='white', line=dict(color='black', width=1))
        source_text = re.sub(
            r"marker_color='#[0-9A-F]{6}'",
            r"marker=dict(color='white', line=dict(color='black', width=1))",
            source_text
        )
        
        # 5. marker=dict(size=X, color='#XXXXXX', opacity=X) → marker=dict(size=X, color='white', line=dict(color='black', width=1))
        source_text = re.sub(
            r"marker=dict\(size=(\d+),\s*color='#[0-9A-F]{6}',\s*opacity=[\d.]+\)",
            r"marker=dict(size=\1, color='white', line=dict(color='black', width=1))",
            source_text
        )
        
        # 6. marker=dict(size=XX, color=temperature, colorscale=...) → marker=dict(size=XX, color='white', line=dict(color='black', width=1))
        source_text = re.sub(
            r"marker=dict\(size=(\d+),\s*color=temperature,\s*colorscale='[^']+',\s*colorbar=dict\([^)]+\)\)",
            r"marker=dict(size=\1, color='white', line=dict(color='black', width=1))",
            source_text
        )
        
        # 7. line=dict(color='#XXXXXX', width=X) → line=dict(color='black', width=X)
        source_text = re.sub(
            r"line=dict\(color='#[0-9A-F]{6}',\s*width=(\d+)\)",
            r"line=dict(color='black', width=\1)",
            source_text
        )
        
        # 8. textfont=dict(size=XX, color='white') → textfont=dict(size=XX, color='black')
        source_text = re.sub(
            r"textfont=dict\(size=(\d+),\s*color='white'\)",
            r"textfont=dict(size=\1, color='black')",
            source_text
        )
        
        # 9. textfont=dict(color='white') → textfont=dict(color='black')
        source_text = re.sub(
            r"textfont=dict\(color='white'\)",
            r"textfont=dict(color='black')",
            source_text
        )
        
        # 10. textposition='top center' 뒤에 textfont 추가
        if 'textposition=' in source_text and 'mode=\'markers+text\'' in source_text:
            source_text = re.sub(
                r"textposition='([^']+)'",
                r"textposition='\1',\n        textfont=dict(color='black')",
                source_text
            )
        
        # 11. colors = ['#XX', ...] 제거
        source_text = re.sub(
            r"colors\s*=\s*\[(?:'#[0-9A-F]{6}',?\s*)+\]\n\n",
            "",
            source_text
        )
        
        if source_text != original:
            변경_카운트 += 1
            # 다시 리스트로 변환
            cell['source'] = source_text.split('\n')
            # 각 라인에 \n 추가 (마지막 제외)
            cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line 
                             for i, line in enumerate(cell['source'])]

# 파일 저장
with open('ch04.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"✅ 색상 변경 완료!")
print(f"   - {변경_카운트}개 셀 수정됨")
print("   - 모든 마커: 흰색 배경 + 검은색 테두리")
print("   - 모든 텍스트: 검은색")
print("   - 모든 선: 검은색 또는 회색")
