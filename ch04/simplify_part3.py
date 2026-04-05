#!/usr/bin/env python3
"""
ch04.ipynb Part 3 (인과 효과 추정) 간소화 - 반사실, 준실험 등
"""
import json

with open('ch04.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Part 3 고급 개념 간소화
replacements = [
    # 반사실적 사고
    ("## 5.4 반사실적 사고 (Counterfactual Reasoning)", "## 5.4 \"만약 ~했다면?\" 사고법 (반사실적 사고)"),
    ("**반사실(Counterfactual)**: 실제로 일어나지 않은 \"만약에\"의 세계", "**반사실**: \"실제로는 안 일어났지만, 만약 ~했다면 어땠을까?\"를 생각하는 것"),
    ("반사실적 추론은 **개별 사례의 인과 효과**를 추정한다.", "이 방법은 **각각의 경우마다** 효과가 얼마인지 알려줍니다."),
    
    # 준실험 설계
    ("## 5.5 준실험 설계 (Quasi-Experimental Designs)", "## 5.5 실험처럼 비교하는 방법들"),
    ("무작위 실험(RCT)이 불가능할 때 사용하는 인과 추론 방법.", "진짜 실험을 못 할 때, 실험처럼 만들어서 비교하는 방법들입니다."),
    
    # DID
    ("### 1. 이중차분법 (Difference-in-Differences, DID)", "### 1. 이중차분법 (변화 vs 변화 비교하기)"),
    ("**핵심 아이디어**: 정책 변화 전후를 비교하되, 대조군으로 시간 추세를 통제", "**핵심**: 정책 실시 전후로 비교하되, 변화 없는 그룹과도 비교해서 진짜 효과만 걸러내기"),
    ("**가정**: 평행 추세 가정 (Parallel Trends Assumption)", "**전제**: 정책이 없었다면 두 그룹 모두 비슷하게 변했을 것"),
    
    # RDD
    ("### 2. 회귀불연속설계 (Regression Discontinuity Design, RDD)", "### 2. 경계선 비교법 (RDD)"),
    ("**핵심 아이디어**: 기준점(cutoff) 근처의 관측치들은 거의 무작위 배정된 것처럼 간주", "**핵심**: 기준점 바로 위/아래는 거의 비슷한데 처리만 다르니까, 여기서 비교하면 진짜 효과를 알 수 있음"),
    ("**예시**: 시험 점수 70점을 기준으로 장학금 지급 → 69점 vs 71점은 거의 동일하지만 처리 유무만 다름", "**예**: 시험 점수 70점 이상만 장학금 → 69점과 71점 학생은 능력이 거의 같은데 장학금만 다름"),
    
    # IV
    ("### 3. 도구변수 (Instrumental Variable, IV)", "### 3. 도구변수 (우회로 이용하기)"),
    ("**핵심 아이디어**: 교란되지 않은 변동 부분만을 이용하여 인과 효과 추정", "**핵심**: 다른 요인에 오염되지 않은 \"깨끗한 변화\"만 골라서 효과 측정"),
    ("도구변수 Z는 다음 조건을 만족해야 한다:", "도구변수 Z는 다음 조건을 꼭 만족해야 합니다:"),
    ("1. **관련성 (Relevance)**: Z → X (Z가 X에 영향)", "1. **관련성**: Z가 X를 실제로 바꿔야 함 (Z → X)"),
    ("2. **배제제약 (Exclusion)**: Z가 Y에 미치는 영향은 오직 X를 통해서만", "2. **배제제약**: Z가 Y에 영향을 주는 길은 오직 X를 거쳐서만 가능"),
    ("3. **외생성 (Exogeneity)**: Z는 교란되지 않음", "3. **깨끗함**: Z는 다른 것들에 오염되지 않았어야 함"),
    
    # ATE vs ATT vs CATE
    ("### 효과의 이질성 (Heterogeneous Treatment Effects)", "### 사람마다 효과가 다를 때"),
    ("- **ATE (Average Treatment Effect)**: 전체 평균 효과", "- **ATE**: 전체 평균 효과"),
    ("- **ATT (Average Treatment Effect on the Treated)**: 실제 처리받은 집단의 평균 효과", "- **ATT**: 실제로 받은 사람들에게만 나타난 평균 효과"),
    ("- **CATE (Conditional ATE)**: 특정 조건(나이, 성별 등)에서의 평균 효과", "- **CATE**: 특정 그룹별 평균 효과 (예: 남성만, 20대만)"),
    ("- **ITE (Individual Treatment Effect)**: 개인별 효과 (실제로는 관측 불가)", "- **ITE**: 각 개인별 효과 (실제로는 알 수 없음, 한 사람은 두 가지 상황을 동시에 경험 못하니까)"),
    
    # 코드 주석들
    ("'Seeing: P(Y | X=x)'", "'지켜보기: P(Y | X=x)'"),
    ("'Doing: P(Y | do(X=x))'", "'직접 조작: P(Y | do(X=x))'"),
    ("# See: 원래 DAG", "# 지켜보기: 원래 구조"),
    ("# See arrows: Z→X, Z→Y, X→Y (all active)", "# 지켜보기: Z→X, Z→Y, X→Y (모두 작동)"),
    ("# Do: 개입 DAG", "# 직접 조작: 변경된 구조"),
    ("# Do arrows: Z→Y, X→Y (Z→X removed!)", "# 직접 조작: Z→Y, X→Y (Z→X 제거됨!)"),
    
    # 준실험 코드 설명
    ("# DID 추정량", "# 이중차분 계산"),
    ("# 처리 전후 차이", "# 정책 실시 전후 변화"),
    ("# 대조군 전후 차이 (시간 추세)", "# 비교 그룹 전후 변화 (원래 흐름)"),
    ("# DID = 두 차이의 차이", "# 이중차분 = (처리그룹 변화) - (비교그룹 변화)"),
    
    # 테이블 헤더
    ("| 구분 | 관찰 | 개입 |", "| 구분 | 지켜보기 | 직접 조작 |"),
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

print("✅ Part 3 간소화 완료!")
print(f"   - {len(replacements)}개 표현 변경")
print("   - 반사실 → '만약 ~했다면?' 사고")
print("   - 준실험 설계 → 실험처럼 비교하기")
print("   - DID → 변화 vs 변화 비교")
print("   - RDD → 경계선 비교법")
print("   - IV → 우회로 이용하기")
