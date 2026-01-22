# 문서/레포트 자동 포맷 생성기 (Document Auto Formatter)

사용자가 최소한의 정보만 입력해도, 학교/회사/연구/보고용 문서를 '논리적 구조 + 규격 포맷'으로 자동 생성하는 프로그램입니다.

## 🎯 주요 기능

- **자동 구조 설계**: 문서 목적에 맞는 최적의 문서 구조(목차, 흐름, 논리) 자동 설계
- **규격 포맷 적용**: 작성 규칙(학교/회사/보고서/논문 등)에 맞는 제목, 소제목, 번호, 문단 스타일 자동 적용
- **완성된 내용 생성**: 형식만 제시하는 것이 아닌, 실제 제출 가능한 완성 문장으로 작성
- **분량 자동 조절**: 목표 분량에 맞춰 각 섹션별 분량 자동 분배
- **문체 자동 조절**: 제출 대상(중학생/대학생/직장인)에 맞춰 어휘 수준, 문장 길이, 설명 깊이 자동 조절

## 📋 시스템 구조

```
Input Parser → Document Analyzer → Structure Generator → Content Generator → Formatter
```

### 주요 모듈

1. **Input Parser**: 사용자 입력 파싱 및 검증, 기본값 추론
2. **Document Analyzer**: 문서 목적 분석, 난이도 및 문체 결정
3. **Structure Generator**: 문서 구조 설계 및 분량 분배
4. **Content Generator**: 실제 문서 내용 생성 (LLM 기반)
5. **Formatter**: 최종 문서 포맷팅 및 체크포인트 생성

## 🚀 사용 방법

### 기본 사용

```python
from src.main import DocumentAutoFormatter

# 사용자 입력
user_input = {
    "document_type": "과제 레포트",
    "target_audience": "대학교",
    "topic": "인공지능의 미래와 사회적 영향",
    "length": "A4 3장",
    "writing_style": "학술적",
    "required_keywords": ["AI", "머신러닝"],
    "evaluation_criteria": ["논리성", "객관성"]
}

# 생성기 초기화
formatter = DocumentAutoFormatter(llm_provider_type="mock")

# 문서 생성
result = formatter.generate(user_input)
print(result)

# 파일로 저장
formatter.generate_and_save(user_input, "output.txt", format_type="text")
```

### OpenAI 사용 (실제 LLM 연동)

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"

formatter = DocumentAutoFormatter(
    llm_provider_type="openai",
    model="gpt-4"
)

result = formatter.generate(user_input)
```

## 📝 입력 형식

### 필수 입력
- `document_type`: 문서 종류 (예: "과제 레포트", "보고서", "논술문")
- `topic`: 주제 (자유 텍스트)

### 선택 입력
- `target_audience`: 제출 대상 (예: "중학교", "고등학교", "대학교", "회사")
- `length`: 분량 (예: "A4 3장", "1500자")
- `writing_style`: 문체 (예: "설명형", "논증형", "학술적")
- `required_keywords`: 반드시 포함할 키워드 (리스트)
- `excluded_content`: 제외할 내용 (리스트)
- `evaluation_criteria`: 평가 기준 (리스트)

## 📤 출력 형식

생성된 문서는 다음 구조를 따릅니다:

1. **전체 문서 개요**
   - 문서 목적 요약
   - 전체 구조 요약 (목차)

2. **자동 생성된 문서 본문**
   - 번호가 매겨진 제목/소제목
   - 각 문단은 실제 제출 가능한 완성 문장

3. **제출용 체크포인트**
   - 평가 기준 충족 여부
   - 보완 제안

## 🏗️ 프로젝트 구조

```
QAZ_3#/
├── src/
│   ├── __init__.py
│   ├── models.py              # 데이터 모델
│   ├── input_parser.py         # 입력 파서
│   ├── document_analyzer.py   # 문서 분석기
│   ├── structure_generator.py # 구조 생성기
│   ├── content_generator.py    # 내용 생성기
│   ├── formatter.py           # 포맷터
│   ├── llm_provider.py        # LLM 추상화 레이어
│   └── main.py                # 메인 실행 파일
├── ARCHITECTURE.md            # 시스템 아키텍처 문서
├── requirements.txt           # 필수 패키지
└── README.md                  # 이 파일
```

## 🔧 확장 가능성

코드는 다음 확장이 가능하도록 설계되었습니다:

- **PDF / DOCX / HWP 출력**: Formatter 모듈 확장
- **학교/회사별 포맷 프리셋**: Structure Generator에 프리셋 시스템 추가
- **평가 기준 기반 자동 첨삭**: 별도 모듈 추가
- **표 / 목록 / 인용 자동 생성**: Content Generator 확장
- **LLM 교체**: LLMProvider 인터페이스로 다양한 LLM 지원

## 📦 설치

```bash
# 저장소 클론 또는 파일 다운로드
# requirements.txt의 패키지 설치 (선택사항)
pip install -r requirements.txt
```

## 🎓 예제 실행

```bash
python src/main.py
```

이 명령어는 예제 입력으로 문서를 생성하고 `output_document.txt`와 `output_document.md` 파일로 저장합니다.

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 자유롭게 사용할 수 있습니다.

## 🤝 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!
