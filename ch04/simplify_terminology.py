#!/usr/bin/env python3
"""
ch04.ipynb의 어려운 용어를 쉬운 언어로 변경하는 스크립트
"""
import json
import re

# 파일 읽기
with open('ch04.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# 용어 매핑 (어려운 용어 -> 쉬운 용어)
replacements = [
    # Part 2 제목
    ("## Part 2. 인과 다이어그램 DAG", "## Part 2. 원인-결과 지도 그리기 (DAG)"),
    
    # DAG 기본 설명
    ("**DAG** = **D**irected **A**cyclic **G**raph (방향성 비순환 그래프)", "**DAG** = 원인과 결과의 흐름을 화살표로 그린 지도\n\n- **D**irected (방향이 있음): 화살표 → 로 원인 → 결과 방향을 표시\n- **A**cyclic (다시 돌아오지 않음): A가 B의 원인이면, B는 A의 원인이 될 수 없음 (순환 금지)\n- **G**raph: 점과 화살표로 연결된 그림"),
    
    # 패턴 테이블
    ("| **교란변수 (Confounder)** | X ← Z → Y | ✅ 필수 | 편향 제거 |", "| **숨은 원인 (교란변수)** | X ← Z → Y | ✅ 필수 | 가짜 관계 제거 |"),
    ("| **매개변수 (Mediator)** | X → M → Y | 상황에 따라 | 간접 효과 제거 |", "| **중간 다리 (매개변수)** | X → M → Y | 상황에 따라 | 중간 단계 효과 제거 |"),
    ("| **충돌변수 (Collider)** | X → Z ← Y | ❌ 금지 | 허위 상관 발생 |", "| **합류점 (충돌변수)** | X → Z ← Y | ❌ 금지 | 가짜 관계 발생 |"),
   
    # 코드 내 print문  
    ("print(\"💡 교란변수(Confounder): X ← Z → Y\")", "print(\"💡 숨은 원인 (교란변수): X ← Z → Y\")"),
    ("print(\"  - Z를 통제하지 않으면 X→Y 효과가 편향됨\")", "print(\"  - Z를 고려하지 않으면 X→Y 관계가 왜곡됨\")"),
    ("print(\"  - 예: 고객 구매성향(Z)이 캠페인 노출(X)과 구매(Y) 모두에 영향\")", "print(\"  - 예: 고객의 원래 구매습관(Z)이 캠페인 노출(X)과 구매(Y) 둘 다에 영향\")"),
    ("print(\"  - 해결: Z를 통제 (층화, 매칭, 회귀 조정)\")", "print(\"  - 해결: Z를 같은 조건으로 만들고 비교하기\")"),
    
    ("print(\"💡 매개변수(Mediator): X → M → Y\")", "print(\"💡 중간 다리 (매개변수): X → M → Y\")"),
    ("print(\"  - 총 효과를 알려면 M을 통제하지 않는다\")", "print(\"  - 전체 효과를 알려면 M을 건드리지 않는다\")"),
    ("print(\"  - 직접 효과만 알려면 M을 통제한다\")", "print(\"  - 직접 효과만 알려면 M을 같은 조건으로 만든다\")"),
    ("print(\"  - 주의: M을 잘못 통제하면 총 효과를 과소추정!\")", "print(\"  - 주의: M을 잘못 고정하면 전체 효과를 작게 측정!\")")
,
    
    ("print(\"💡 충돌변수(Collider): X → Z ← Y\")", "print(\"💡 합류점 (충돌변수): X → Z ← Y\")"),
    ("print(\"  - X와 Y는 원래 독립 (재능과 노력은 관련 없음)\")", "print(\"  - X와 Y는 원래 상관없음 (재능과 노력은 독립적)\")")
,
    ("print(\"  - Z를 통제하면(성공한 사람만 분석) X-Y에 허위 상관 발생\")", "print(\"  - Z를 같은 조건으로 만들면(성공한 사람만 분석) X-Y에 가짜 관계 발생\")"),
    ("print(\"  - 이것이 '선택 편향(Selection Bias)'\")", "print(\"  - 이것이 '선택 편향(특정 집단만 보는 오류)'\")"),
    
    # 시뮬레이션 설명
    ("print(f\"💡 전체: 재능과 노력의 상관 r = {corr_all:.2f} (거의 독립)\")", "print(f\"💡 전체: 재능과 노력의 관계 r = {corr_all:.2f} (거의 상관없음)\")"),
    ("print(f\"💡 성공한 사람만: r = {corr_success:.2f} (부적 상관 → 허위!)\")", "print(f\"💡 성공한 사람만: r = {corr_success:.2f} (반비례처럼 보임 → 가짜!)\")")
,
    ("print(\"   → 성공(충돌변수)을 통제하면 재능과 노력이 반비례하는 것처럼 보인다\")", "print(\"   → 성공(합류점)을 같은 조건으로 만들면 재능과 노력이 반비례하는 것처럼 보인다\")"),
    ("print(\"   → 생존 기업만 분석, 응답자만 분석 등에서도 같은 문제 발생\")", "print(\"   → 살아남은 기업만 분석, 응답한 사람만 분석 등에서도 같은 문제 발생\")"),
    
    # Part 3 제목
    ("## Part 3. 인과 효과 추정", "## Part 3. 진짜 효과 계산하기"),
    
    ("## 5.3 관찰(Seeing) vs 개입(Doing)", "## 5.3 지켜보기 vs 직접 조작하기"),
    
    # do-연산자 테이블
    ("| 관찰 | 개입 |", "| 지켜보기 (관찰) | 직접 조작하기 (개입) |"),
    ("| P(Y \\| X=x) | P(Y \\| **do**(X=x)) |", "| P(Y \\| X=x) | P(Y \\| **do**(X=x)) |"),
    ("| X가 x인 것을 **관찰**했을 때 Y | X를 x로 **설정**했을 때 Y |", "| X가 x인 것을 **발견**했을 때 Y | X를 x로 **강제로 만들었을 때** Y |"),
    ("| 약 복용자의 회복률 | 약을 **복용시켰을 때** 회복률 |", "| 약 먹은 사람들의 회복률 | 약을 **먹게 했을 때** 회복률 |"),
    
    # 백도어 조정
    ("### 백도어 조정 (Backdoor Adjustment)", "### 백도어 조정 (숨은 뒷길 막기)"),
("관찰 데이터에서 P(Y|do(X=x))를 계산하는 공식:", "관찰 데이터만 있을 때 '직접 조작' 효과를 계산하는 방법:"),
    ("→ 교란변수 Z에 대해 조건화하고 가중 평균을 취하면, 관찰 데이터에서 인과 효과 추정 가능!", "→ 숨은 원인(Z)을 같은 조건으로 나눠서 가중 평균을 내면, 관찰한 데이터만으로도 진짜 효과를 알 수 있어요!"),
]

# 각 셀의 source를 순회하면서 교체
for cell in notebook['cells']:
    if 'source' in cell:
        # source는 문자열 리스트
        source_text = ''.join(cell['source'])
        
        # 모든 교체 수행
        for old, new in replacements:
            source_text = source_text.replace(old, new)
        
        # 다시 리스트로 변환 (원래 형식 유지)
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

print("✅ 용어 간소화 완료!")
print(f"   - {len(replacements)}개 표현 변경")
print("   - 교란변수 → 숨은 원인")
print("   - 매개변수 → 중간 다리")
print("   - 충돌변수 → 합류점")
print("   - 통제 → 같은 조건으로 만들기")
print("   - 허위/편향 → 가짜/왜곡")
