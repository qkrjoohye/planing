#!/usr/bin/env python3
"""
ch04.ipynb Part 4, 5 및 기타 부분 간소화
"""
import json

with open('ch04.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

replacements = [
    # Part 4
    ("## Part 4. 실습: 마케팅 캠페인 효과 시뮬레이션", "## Part 4. 실습: 마케팅 캠페인의 진짜 효과 찾기"),
    
    # Part 5
    ("## Part 5. 종합 실습: DAG 구축 + 인과 효과 추정", "## Part 5. 종합 실습: 원인-결과 지도 + 진짜 효과 계산"),
    
    # 기타 일반적인 어려운 표현들
    ("인과추론", "원인-결과 찾기"),
    ("인과 추론", "원인-결과 찾기"),
    ("인과효과", "진짜 효과"),
    ("인과 효과", "진짜 효과"),
    ("평균 처리 효과", "평균 효과"),
    ("처리 효과", "효과"),
    ("처리받은", "받은"),
    ("처리군", "대상 그룹"),
    ("대조군", "비교 그룹"),
    ("통제하", "같은 조건으로 만들"),
    ("통제된", "같은 조건인"),
    ("층화", "그룹별로 나누기"),
    ("매칭", "비슷한 것끼리 짝짓기"),
    ("회귀 조정", "통계로 보정하기"),
    ("편향", "왜곡"),
    ("허위 상관", "가짜 관계"),
    ("허위", "가짜"),
    ("유의", "의미있"),
    ("유의한", "의미 있는"),
    ("관찰치", "관찰값"),
    ("추정량", "계산값"),
    ("추정치", "예측값"),
    ("설명변수", "원인 변수"),
    ("결과변수", "결과 변수"),
    ("독립변수", "원인 변수"),
    ("종속변수", "결과 변수"),
    
    # 더 쉬운 문장으로
    ("평행 추세 가정", "두 그룹이 원래 비슷하게 변했을 것이라는 가정"),
    ("외생성", "깨끗함 (다른 요인에 오염 안 됨)"),
    ("내생성", "오염됨 (다른 요인과 섞임)"),
    ("이질성", "다양함"),
    ("동질성", "비슷함"),
]

for cell in notebook['cells']:
    if 'source' in cell:
        source_text = ''.join(cell['source'])
        
        for old, new in replacements:
            source_text = source_text.replace(old, new)
        
        cell['source'] = [line + '\n' if not line.endswith('\n') and i < len(source_text.split('\n')) - 1 
                          else line 
                          for i, line in enumerate(source_text.split('\n'))]
        if cell['source'] and not cell['source'][-1].endswith('\n'):
            cell['source'][-1] += '\n'
        if cell['source'][-1] == '\n':
            cell['source'] = cell['source'][:-1]

with open('ch04.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("✅ Part 4, 5 및 전체 추가 간소화 완료!")
print(f"   - {len(replacements)}개 표현 변경")
print("   - 인과추론 → 원인-결과 찾기")
print("   - 통제 → 같은 조건으로 만들기")
print("   - 편향 → 왜곡")
print("   - 허위 → 가짜")
print("   - 처리군/대조군 → 대상/비교 그룹")
