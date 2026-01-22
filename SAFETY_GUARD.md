# 요금 방지 안전장치 가이드

## 🛡️ 현재 적용된 안전장치

### 1. API 엔드포인트 레벨 보호

**파일**: `api/generate.py`

```python
# 강제로 'mock' 사용 (요금 방지)
llm_provider_type = 'mock'  # 사용자 입력 무시
```

**효과**: 
- 사용자가 `llm_provider_type: 'openai'`를 전달해도 무시됨
- 항상 무료 Mock Provider 사용

### 2. LLM Provider 팩토리 레벨 보호

**파일**: `src/llm_provider.py`

```python
def get_llm_provider(provider_type: str = "mock", **kwargs):
    # 환경 변수 확인: OPENAI_API_KEY가 없으면 강제로 mock 사용
    if provider_type == "openai" and not os.getenv("OPENAI_API_KEY"):
        return MockLLMProvider()  # 자동 폴백
    
    # 알 수 없는 타입도 mock으로 폴백
    if provider_type not in ["mock", "openai"]:
        return MockLLMProvider()
```

**효과**:
- API 키가 없으면 자동으로 Mock으로 전환
- 잘못된 타입 입력 시 Mock으로 폴백

### 3. DocumentAutoFormatter 레벨 보호

**파일**: `src/main.py`

```python
def __init__(self, llm_provider_type: str = "mock", **llm_kwargs):
    # OpenAI 사용 시 환경 변수 확인
    if llm_provider_type == "openai" and not os.getenv("OPENAI_API_KEY"):
        llm_provider_type = "mock"  # 자동 전환
```

**효과**:
- 초기화 단계에서 안전장치 적용
- API 키 없이는 OpenAI 사용 불가

### 4. 프론트엔드 레벨 보호

**파일**: `public/index.html`

```javascript
body: JSON.stringify({
    input: input,
    llm_provider_type: 'mock'  // 하드코딩
})
```

**효과**:
- 사용자가 개발자 도구에서 변경해도 서버에서 무시됨
- 항상 'mock' 전송

## 🔒 다층 방어 시스템

```
사용자 요청
    ↓
[1] 프론트엔드: 'mock' 하드코딩
    ↓
[2] API 엔드포인트: 'mock' 강제 설정
    ↓
[3] DocumentAutoFormatter: 환경 변수 확인
    ↓
[4] LLM Provider 팩토리: 최종 안전장치
    ↓
MockLLMProvider (무료) ✅
```

## ⚠️ OpenAI 사용 시 주의사항

### OpenAI를 사용하려면 (요금 발생)

**필수 조건:**
1. Vercel 환경 변수에 `OPENAI_API_KEY` 설정
2. `api/generate.py`에서 `llm_provider_type = 'openai'`로 변경
3. `public/index.html`에서 `llm_provider_type: 'openai'`로 변경

**현재 상태:**
- ✅ 위 조건이 모두 충족되지 않음
- ✅ 자동으로 Mock Provider 사용
- ✅ 요금 발생 없음

### 요금 발생 방지 체크리스트

- [x] API 엔드포인트에서 'mock' 강제 사용
- [x] 환경 변수 확인 로직 추가
- [x] 프론트엔드에서 'mock' 하드코딩
- [x] 잘못된 타입 입력 시 Mock으로 폴백
- [x] API 키 없으면 자동 폴백

## 🚨 실수 방지 가이드

### 하지 말아야 할 것

1. ❌ `api/generate.py`에서 `llm_provider_type`을 사용자 입력으로 받기
2. ❌ 환경 변수 확인 없이 OpenAI 사용
3. ❌ 프론트엔드에서 사용자가 타입을 선택할 수 있게 하기

### 해야 할 것

1. ✅ 항상 기본값을 'mock'로 설정
2. ✅ 환경 변수 확인 후에만 OpenAI 사용
3. ✅ 여러 레벨에서 안전장치 적용

## 📊 현재 보안 상태

| 보안 레벨 | 상태 | 설명 |
|----------|------|------|
| 프론트엔드 | ✅ 안전 | 'mock' 하드코딩 |
| API 엔드포인트 | ✅ 안전 | 'mock' 강제 설정 |
| 초기화 단계 | ✅ 안전 | 환경 변수 확인 |
| 팩토리 함수 | ✅ 안전 | 다중 폴백 로직 |

## 💰 요금 발생 가능성

**현재 설정**: 0% (완전 차단)

**이유**:
- 모든 레벨에서 'mock' 강제 사용
- 환경 변수 확인 로직
- 다중 안전장치 적용

## 🔄 OpenAI 활성화 방법 (필요시)

만약 나중에 OpenAI를 사용하고 싶다면:

1. **Vercel 환경 변수 설정**
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

2. **api/generate.py 수정**
   ```python
   # 주석 해제 및 수정
   llm_provider_type = body.get('llm_provider_type', 'mock')
   ```

3. **public/index.html 수정**
   ```javascript
   llm_provider_type: 'openai'  // 'mock' → 'openai'
   ```

**주의**: 위 단계를 모두 수행해야만 OpenAI가 사용됩니다.

## 결론

✅ **현재 상태: 완전히 안전**

- 다층 방어 시스템 적용
- 실수로 인한 요금 발생 불가능
- 모든 레벨에서 'mock' 강제 사용

요금 걱정 없이 안전하게 사용하실 수 있습니다! 🎉
