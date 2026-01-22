# Vercel NOT_FOUND 오류 완전 분석 가이드

## 1. 수정 제안 (The Fix)

### 문제점
현재 `vercel.json`의 rewrite 설정이 Vercel의 정적 파일 제공 메커니즘과 충돌할 수 있습니다.

### 해결 방법

**옵션 A: vercel.json 제거 (권장)**
```json
// vercel.json 삭제
```
Vercel은 자동으로:
- `public/` 폴더의 파일을 정적 파일로 제공
- `api/` 폴더의 `.py` 파일을 서버리스 함수로 인식

**옵션 B: 최소 설정 유지**
```json
{
  "buildCommand": "",
  "outputDirectory": ""
}
```
rewrite 없이 빌드 명령만 비활성화

**옵션 C: 명시적 rewrite (필요한 경우만)**
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/$1"
    }
  ]
}
```

## 2. 근본 원인 분석 (Root Cause)

### 실제 동작 vs 필요한 동작

**실제 동작:**
1. Vercel이 프로젝트를 스캔
2. `package.json`이나 프레임워크 설정을 찾지 못함
3. `public/` 폴더와 `api/` 폴더를 발견
4. 자동 감지 시도 중 오류 발생

**필요한 동작:**
1. `public/index.html` → 루트 경로(`/`)에서 제공
2. `api/generate.py` → `/api/generate` 엔드포인트로 제공
3. `api/index.py` → `/api/*` 엔드포인트로 제공

### 오류 발생 조건

1. **프로젝트 타입 오인식**
   - Vercel이 Docusaurus나 다른 프레임워크로 오인식
   - `buildCommand`가 설정되지 않아 기본값 사용 시도

2. **정적 파일 경로 불일치**
   - `rewrite`가 `/index.html`을 가리키지만
   - Vercel은 `public/index.html`을 찾음
   - 경로 매핑 불일치

3. **빌드 프로세스 간섭**
   - 빌드 명령이 실행되면서 정적 파일 제공 실패
   - Python 서버리스 함수와 정적 파일 간 충돌

### 오해와 실수

**오해 1: "rewrite가 필요하다"**
- 사실: Vercel은 `public/` 폴더를 자동으로 루트에 매핑
- 실수: 불필요한 rewrite 추가로 경로 충돌

**오해 2: "빌드 명령이 필요하다"**
- 사실: Python 서버리스 함수는 빌드 불필요
- 실수: 빌드 명령을 비워두지 않아 프레임워크 감지 시도

**오해 3: "vercel.json이 필수다"**
- 사실: 대부분의 경우 자동 감지로 충분
- 실수: 과도한 설정으로 자동 감지 방해

## 3. 개념 이해 (Conceptual Understanding)

### Vercel의 파일 제공 메커니즘

**정적 파일 (Static Files)**
```
public/index.html → https://your-domain.com/index.html
public/style.css → https://your-domain.com/style.css
```
- `public/` 폴더의 모든 파일이 루트 경로에 자동 매핑
- 별도 설정 불필요

**서버리스 함수 (Serverless Functions)**
```
api/generate.py → https://your-domain.com/api/generate
api/index.py → https://your-domain.com/api/index
```
- `api/` 폴더의 파일이 자동으로 엔드포인트로 변환
- Python 파일은 `handler(request)` 함수 필요

**라우팅 우선순위**
1. API 라우트 (`/api/*`) - 가장 높은 우선순위
2. 정적 파일 (`public/*`)
3. Rewrite 규칙
4. 404 페이지

### 왜 이 오류가 존재하는가?

**보호 기능:**
- 잘못된 경로로 인한 보안 문제 방지
- 존재하지 않는 리소스 접근 차단
- 명확한 오류 메시지로 디버깅 지원

**프레임워크 설계 철학:**
- Convention over Configuration (설정보다 관례)
- 자동 감지로 개발자 편의성 제공
- 명시적 설정으로 오버라이드 가능

### 올바른 정신 모델

**Vercel 프로젝트 구조:**
```
project/
├── public/          # 정적 파일 (자동 제공)
│   └── index.html
├── api/             # 서버리스 함수 (자동 엔드포인트)
│   └── *.py
├── src/             # 소스 코드 (함수에서 import)
└── vercel.json      # 선택적 설정 (필요시만)
```

**요청 처리 흐름:**
```
요청 → API 라우트 확인 → 정적 파일 확인 → Rewrite 확인 → 404
```

## 4. 경고 신호 (Warning Signs)

### 미래에 이 문제를 피하기 위한 패턴

**코드 냄새 (Code Smells):**

1. **과도한 vercel.json 설정**
   ```json
   // 나쁜 예: 불필요한 설정
   {
     "builds": [...],
     "routes": [...],
     "rewrites": [...],
     "headers": [...]
   }
   ```
   → 자동 감지 기능을 방해함

2. **프로젝트 루트에 정적 파일**
   ```
   project/
   ├── index.html  // 나쁨: public/에 있어야 함
   └── public/
   ```

3. **빌드 명령 미설정**
   ```json
   // 나쁨: 빌드 명령이 비어있지 않음
   {
     // buildCommand가 없으면 자동 감지 시도
   }
   ```

**유사한 실수:**

1. **Next.js 프로젝트에서 public/ 사용 오해**
   - Next.js는 `public/`을 자동 제공하지만
   - Vercel 설정과 충돌 가능

2. **API 라우트 경로 오타**
   ```
   api/generate.py → /api/generate (올바름)
   api/generate.py → /generate (잘못됨)
   ```

3. **환경 변수 경로 문제**
   - Python 함수에서 상대 경로 사용 시
   - Vercel 환경에서 경로 해석 오류

## 5. 대안 접근법 (Alternatives)

### 접근법 1: Zero Config (권장)
**장점:**
- 설정 최소화
- Vercel 자동 감지 활용
- 유지보수 용이

**단점:**
- 커스터마이징 제한
- 복잡한 라우팅 어려움

**사용 시기:**
- 간단한 정적 사이트 + API
- 표준 Vercel 구조 준수

### 접근법 2: Minimal Config
**장점:**
- 필요한 부분만 설정
- 자동 감지와 설정 병행

**단점:**
- 설정 파일 관리 필요

**사용 시기:**
- 빌드 명령 비활성화 필요
- 특정 rewrite 규칙 필요

### 접근법 3: Full Config
**장점:**
- 완전한 제어
- 복잡한 라우팅 가능

**단점:**
- 설정 복잡도 증가
- 자동 감지 비활성화

**사용 시기:**
- 복잡한 마이그레이션
- 특수한 요구사항

### 트레이드오프 비교

| 접근법 | 복잡도 | 유연성 | 유지보수 | 권장도 |
|--------|--------|--------|----------|--------|
| Zero Config | 낮음 | 낮음 | 높음 | ⭐⭐⭐⭐⭐ |
| Minimal Config | 중간 | 중간 | 중간 | ⭐⭐⭐⭐ |
| Full Config | 높음 | 높음 | 낮음 | ⭐⭐ |

## 실전 체크리스트

배포 전 확인사항:
- [ ] `public/` 폴더에 정적 파일 배치
- [ ] `api/` 폴더에 Python 함수 배치
- [ ] `vercel.json`이 정말 필요한가?
- [ ] 빌드 명령이 비어있는가? (Python 프로젝트)
- [ ] API 함수에 `handler(request)` 함수가 있는가?
- [ ] 상대 경로가 올바른가?

## 참고 자료

- [Vercel Python Functions](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Vercel Configuration](https://vercel.com/docs/projects/project-configuration)
- [Vercel Routing](https://vercel.com/docs/concepts/projects/project-configuration#rewrites)
