# API 요금 정보

## 현재 상태: 요금 없음 ✅

### 현재 사용 중인 설정

**LLM Provider**: `MockLLMProvider` (무료)

```javascript
// public/index.html
llm_provider_type: 'mock'  // 실제 API 호출 없음
```

### MockLLMProvider 작동 방식

- **실제 API 호출 없음**: 외부 서비스에 요청하지 않음
- **템플릿 기반 응답**: 미리 정의된 템플릿으로 응답 생성
- **완전 무료**: 인터넷 연결만 있으면 작동

### 요금 발생 조건

요금이 발생하려면 다음 조건이 모두 충족되어야 합니다:

1. ✅ `llm_provider_type: 'openai'`로 변경
2. ✅ Vercel 환경 변수에 `OPENAI_API_KEY` 설정
3. ✅ OpenAI API를 실제로 호출

**현재는 위 조건이 모두 충족되지 않았으므로 요금이 발생하지 않습니다.**

## OpenAI 사용 시 예상 비용

만약 OpenAI를 사용한다면:

### GPT-4 모델
- 입력: 약 $0.03 / 1K 토큰
- 출력: 약 $0.06 / 1K 토큰
- 예상: 문서 1개당 약 $0.10-0.50 (분량에 따라 다름)

### GPT-3.5 Turbo 모델 (더 저렴)
- 입력: 약 $0.0015 / 1K 토큰
- 출력: 약 $0.002 / 1K 토큰
- 예상: 문서 1개당 약 $0.01-0.05

### 무료 크레딧
- OpenAI 신규 가입 시 $5 무료 크레딧 제공
- 테스트용으로 충분함

## OpenAI 사용 방법 (선택사항)

### 1. Vercel 환경 변수 설정

1. Vercel 대시보드 접속
2. 프로젝트 → Settings → Environment Variables
3. 다음 추가:
   - Key: `OPENAI_API_KEY`
   - Value: 실제 OpenAI API 키
   - Environment: Production, Preview, Development 모두 선택

### 2. 코드 수정

```javascript
// public/index.html에서
body: JSON.stringify({
    input: input,
    llm_provider_type: 'openai'  // 'mock' → 'openai'로 변경
})
```

### 3. requirements.txt 업데이트 (필요시)

```txt
openai>=1.0.0
```

## 현재 권장사항

**Mock Provider 유지 권장** 이유:
- ✅ 완전 무료
- ✅ 빠른 응답 속도
- ✅ API 제한 없음
- ✅ 오프라인 작동 가능

**OpenAI 사용 고려** 경우:
- 더 고품질 문서 생성 필요
- 실제 LLM의 창의성과 맥락 이해 필요
- 프로덕션 환경에서 사용

## 비용 모니터링

OpenAI 사용 시:
1. OpenAI 대시보드에서 사용량 확인
2. Vercel Functions 탭에서 호출 횟수 확인
3. 예산 알림 설정 (OpenAI 대시보드)

## 결론

**현재 상태: 요금 0원** 💰

- Mock Provider 사용 중
- 실제 API 호출 없음
- 완전 무료로 작동 중

요금 걱정 없이 사용하셔도 됩니다!
