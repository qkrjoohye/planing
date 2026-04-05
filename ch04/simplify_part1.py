#!/usr/bin/env python3
"""
ch04.ipynb Part 1을 더 쉽게 만들기
"""
import json

# 파일 읽기
with open('ch04.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Part 1 추가 간소화
replacements = [
    # 추가 용어 간소화
    ("Judea Pearl이 체계화한 인과구조 시각화 도구", "원인과 결과를 쉽게 보기 위한 그림"),
    ("**노드(Node)**: 변수를 나타냄", "**점(Node)**: 각각의 변수 (예: 날씨, 매출 등)"),
    ("**엣지(Edge)**: 화살표로 인과 방향을 표현 (X → Y = \"X가 Y의 원인\")", "**화살표(Edge)**: 원인 → 결과를 표시 (X → Y = \"X가 Y를 만듦\")"),
    ("**방향성**: 인과의 방향을 명시", "**방향이 있음**: 누가 원인이고 누가 결과인지 명확함"),
    ("**비순환**: 순환 고리가 없음 (시간적 선후관계 반영)", "**돌고 돌지 않음**: A→B→C 가능, 하지만 C→A는 불가 (시간 순서대로)"),
    
    # 과제 부분
    ("**Judea Pearl**의 인과 다이어그램(DAG)에서 \"방향성(Directed)\"과 \"비순환성(Acyclic)\"이 각각 무엇을 의미하는지 설명하시오.", "원인-결과 지도(DAG)에서 \"방향이 있다\"와 \"돌고 돌지 않는다\"가 각각 무슨 뜻인지 쉬운 말로 설명하시오."),
    ("다음 상황에서 변수의 역할(교란/매개/충돌)을 판단하시오:", "다음 상황에서 변수가 어떤 역할을 하는지 판단하시오:"),
    ("\"디지털 투자(X) → 프로세스 효율(M) → 비용절감(Y)\" 에서 M은?", "\"디지털 투자(X) → 업무 효율(M) → 비용절감(Y)\" 에서 M은?"),
    ("**충돌변수를 통제하면 안 되는 이유**를 \"생존 편향(Survivorship Bias)\"의 예시를 들어 설명하시오. (2-3문장)", "**합류점을 같은 조건으로 만들면 안 되는 이유**를 \"살아남은 것만 보는 오류\"의 예시를 들어 설명하시오. (2-3문장)"),
    
    # 코드 주석 부분도 간소화
    ("'Pattern 1: Confounder (Must Control ✅)'", "'패턴 1: 숨은 원인 (반드시 고려해야 함 ✅)'"),
    ("'e.g., Customer Value → Campaign + Purchase'", "'예: 고객 가치 → 캠페인 + 구매'"),
    ("'Pattern 2: Mediator (Control Depends on Goal)'", "'패턴 2: 중간 다리 (목적에 따라 다름)'"),
    ("'Direct effect: X→Y (signaling)\\n'", "'직접 효과: X→Y (신호 효과)\\n'"),
    ("'Indirect effect: X→M→Y (skill building)'", "'간접 효과: X→M→Y (실력 향상)'"),
    ("'Pattern 3: Collider (Never Control ❌)'", "'패턴 3: 합류점 (절대 고려하면 안 됨 ❌)'"),
    ("'X and Y: originally INDEPENDENT'", "'X와 Y: 원래는 상관없음'"),
    ("'Controlling Z creates false X↔Y correlation!'", "'Z를 고정하면 X-Y에 가짜 관계가 생김!'"),
    
    # Simpson's Paradox 설명 전체를 간단하게
    ("Simpson's Paradox는 **집단을 나누는 방식**에 따라 결론이 정반대로 바뀌는 현상이다.",
     "Simpson's Paradox는 **어떻게 나눠보느냐**에 따라 결론이 완전히 뒤바뀌는 놀라운 현상입니다."),
]

# 각 셀의 source를 순회하면서 교체
for cell in notebook['cells']:
    if 'source' in cell:
        source_text = ''.join(cell['source'])
        
        for old, new in replacements:
            source_text = source_text.replace(old, new)
        
        # 다시 리스트로 변환
        cell['source'] = [line + '\n' if not line.endswith('\n') and i < len(source_text.split('\n')) - 1 
                          else line 
                          for i, line in enumerate(source_text.split('\n'))]
        if cell['source'] and not cell['source'][-1].endswith('\n'):
            cell['source'][-1] += '\n'
        if cell['source'][-1] == '\n':
            cell['source'] = cell['source'][:-1]

# 파일 저장
with open('ch04.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("✅ Part 1 추가 간소화 완료!")
print(f"   - {len(replacements)}개 추가 표현 변경")
print("   - 전문 용어 → 일상 언어")
print("   - 학술적 표현 → 쉬운 설명")
