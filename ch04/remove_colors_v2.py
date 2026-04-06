#!/usr/bin/env python3
"""
ch04.ipynb의 모든 그래프 색상을 검은색으로 변경하는 스크립트 v2
노드 dictionary의 'color' 키와 기타 색상 패턴 처리
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
        
        # 1. Dictionary 내의 'color': '#XXXXXX' → 'color': 'black' (노드 정의용)
        source_text = re.sub(
            r"'color':\s*'#[0-9A-F]{6}'",
            r"'color': 'black'",
            source_text
        )
        
        # 2. line=dict(color='#XXXXXX', ...) → line=dict(color='black', ...)
        source_text = re.sub(
            r"line=dict\(color='#[0-9A-F]{6}'",
            r"line=dict(color='black'",
            source_text
        )
        
        # 3. for loop의 색상 리스트: (df_treated, 'Campaign O', '#FF6B6B') → (df_treated, 'Campaign O', 'black')
        source_text = re.sub(
            r"\(df_treated,\s*'Campaign O',\s*'#[0-9A-F]{6}'\)",
            r"(df_treated, 'Campaign O', 'black')",
            source_text
        )
        source_text = re.sub(
            r"\(df_control,\s*'Campaign X',\s*'#[0-9A-F]{6}'\)",
            r"(df_control, 'Campaign X', 'gray')",
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

print(f"✅ 추가 색상 변경 완료!")
print(f"   - {변경_카운트}개 셀 추가 수정됨")
print("   - 노드 color: 'black'")
print("   - 선 color: 'black'")
print("   - 그룹별 라인: 'black', 'gray'")
