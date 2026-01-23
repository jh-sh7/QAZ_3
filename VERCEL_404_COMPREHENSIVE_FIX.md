# Vercel 404 오류 종합 해결 가이드

## 1. 수정 제안 (Immediate Fix)

### 문제 진단
현재 `/api` 엔드포인트가 404를 반환하는 이유는 **Vercel이 Python 서버리스 함수를 인식하지 못하기 때문**입니다.

### 즉시 적용할 수정사항

#### A. `vercel.json` 최적화
```json
{
  "functions": {
    "api/index.py": {
      "runtime": "@vercel/python"
    }
  },
  "rewrites": [
    {
      "source": "/api",
      "destination": "/api/index.py"
    }
  ]
}
```

#### B. 프로젝트 설정 확인
Vercel 대시보드 → Settings → General:
- **Framework Preset**: `Other` 또는 `No Framework`
- **Build Command**: 비워두기
- **Output Directory**: 비워두기
- **Install Command**: 비워두기

#### C. Python 함수 형식 확인
`api/index.py`의 `handler` 함수가 올바른 형식인지 확인:
- 함수명: `handler` (필수)
- 매개변수: `request` 객체
- 반환값: `dict` with `statusCode`, `headers`, `body`

## 2. 근본 원인 설명 (Root Cause Analysis)

### 코드가 실제로 하는 것 vs 필요한 것

**현재 코드의 동작:**
```python
def handler(request):
    # request 객체에서 method, body 등을 추출
    # JSON 응답 반환
    return {'statusCode': 200, 'headers': {...}, 'body': '...'}
```

**Vercel이 기대하는 것:**
1. `api/` 폴더의 `.py` 파일을 자동으로 서버리스 함수로 인식
2. `handler` 함수를 export하여 Vercel 런타임이 호출
3. `@vercel/python` 런타임이 함수를 빌드하고 배포

### 오류가 발생하는 조건

1. **프로젝트 설정 오류**
   - Framework Preset이 잘못 설정됨 (예: Next.js, Docusaurus)
   - Vercel이 Python 파일을 무시하고 다른 프레임워크로 빌드 시도

2. **빌드 캐시 문제**
   - 이전 빌드 캐시가 남아있어 Python 함수가 재빌드되지 않음
   - `vercel.json` 변경사항이 반영되지 않음

3. **파일 구조 문제**
   - `api/index.py`가 올바른 위치에 있지 않음
   - `handler` 함수가 올바르게 정의되지 않음

### 오류를 유발한 오해

**오해 1**: "Vercel이 자동으로 Python 파일을 인식한다"
- **실제**: Vercel은 `api/` 폴더의 파일을 자동으로 인식하지만, 프로젝트 설정이 올바르지 않으면 인식하지 못함

**오해 2**: "`vercel.json` 없이도 작동한다"
- **실제**: 대부분의 경우 자동 감지가 작동하지만, 혼합 프로젝트(정적 파일 + 서버리스 함수)에서는 명시적 설정이 필요할 수 있음

**오해 3**: "`handler` 함수만 있으면 된다"
- **실제**: 함수 형식뿐만 아니라 프로젝트 설정, 빌드 설정도 올바르게 구성되어야 함

## 3. 개념 설명 (Conceptual Understanding)

### Vercel 서버리스 함수의 작동 원리

#### 왜 이 오류가 존재하는가?
Vercel은 **다중 프레임워크 지원**을 위해 프로젝트를 자동으로 감지합니다:
- `package.json`이 있으면 → Node.js 프로젝트로 인식
- `next.config.js`가 있으면 → Next.js 프로젝트로 인식
- `docusaurus.config.js`가 있으면 → Docusaurus 프로젝트로 인식

**문제**: Python 서버리스 함수만 있는 프로젝트는 "프레임워크 없음"으로 설정해야 하는데, Vercel이 다른 프레임워크로 잘못 인식할 수 있음

#### 올바른 정신 모델

```
프로젝트 구조:
├── public/          # 정적 파일 (자동 서빙)
│   └── index.html
├── api/             # 서버리스 함수 (자동 감지)
│   └── index.py     # → /api 엔드포인트
└── vercel.json      # 명시적 설정 (선택사항)
```

**Vercel의 처리 과정:**
1. 프로젝트 스캔 → 프레임워크 감지
2. `api/` 폴더 스캔 → Python 파일 발견
3. `@vercel/python` 런타임으로 함수 빌드
4. 배포 시 함수를 `/api` 경로에 매핑

**문제 발생 지점**: 1단계에서 잘못된 프레임워크로 인식하면 2-4단계가 실행되지 않음

#### 프레임워크 설계의 맥락

Vercel은 **"Convention over Configuration"** 원칙을 따릅니다:
- 기본적으로 자동 감지로 작동
- 하지만 명시적 설정(`vercel.json`)으로 오버라이드 가능

**장점**: 간단한 프로젝트는 설정 없이 작동
**단점**: 복잡한 프로젝트는 명시적 설정이 필요

## 4. 경고 신호 (Warning Signs)

### 미래에 이 문제를 피하기 위한 패턴

#### 코드 스멜 (Code Smells)

1. **Resources 탭에 Static Assets만 보임**
   - ✅ 정상: Static Assets + Serverless Functions
   - ❌ 문제: Static Assets만 있음 → 함수가 인식되지 않음

2. **Functions 탭이 없음**
   - ✅ 정상: Functions 탭에 `api/index` 함수 표시
   - ❌ 문제: Functions 탭 자체가 없음 → Python 함수 미인식

3. **Build Logs에 Python 관련 메시지 없음**
   - ✅ 정상: "Installing @vercel/python", "Building functions..."
   - ❌ 문제: Python 관련 로그가 전혀 없음

#### 유사한 시나리오에서 주의할 점

1. **혼합 프로젝트 (정적 파일 + 서버리스 함수)**
   - Framework Preset을 `Other`로 설정
   - `vercel.json`에 명시적 설정 추가

2. **프로젝트 이름 변경 후**
   - 새 프로젝트는 기본 설정이 다를 수 있음
   - Settings에서 Framework Preset 확인 필수

3. **GitHub 연동 후 자동 배포**
   - Vercel이 저장소를 스캔할 때 잘못된 프레임워크로 인식할 수 있음
   - 첫 배포 후 Functions 탭 확인 필수

#### 문제를 나타내는 패턴

```python
# ❌ 잘못된 형식
def my_handler(req):  # 함수명이 'handler'가 아님
    return "Hello"

# ✅ 올바른 형식
def handler(request):  # 함수명이 'handler'
    return {'statusCode': 200, 'body': 'Hello'}
```

```json
// ❌ 잘못된 vercel.json
{
  "builds": {  // 구버전 형식
    "src": "@vercel/python"
  }
}

// ✅ 올바른 vercel.json
{
  "functions": {  // 최신 형식
    "api/index.py": {
      "runtime": "@vercel/python"
    }
  }
}
```

## 5. 대안 접근법 (Alternative Approaches)

### 접근법 1: 명시적 설정 (현재 사용 중)
```json
{
  "functions": {
    "api/index.py": {
      "runtime": "@vercel/python"
    }
  }
}
```

**장점:**
- Vercel이 정확히 어떤 함수를 빌드할지 명시
- 프로젝트 설정과 독립적으로 작동

**단점:**
- 각 함수마다 설정 필요
- 파일 추가 시 `vercel.json` 업데이트 필요

### 접근법 2: 자동 감지 (설정 없음)
`vercel.json` 없이 Vercel이 자동으로 감지

**장점:**
- 설정 파일 불필요
- 파일 추가 시 자동 인식

**단점:**
- 프로젝트 설정에 의존
- 혼합 프로젝트에서 실패할 수 있음

### 접근법 3: 폴더 기반 라우팅
```
api/
  ├── index.py      # → /api
  └── generate/
      └── index.py  # → /api/generate
```

**장점:**
- RESTful API 구조와 일치
- 각 엔드포인트를 독립적으로 관리

**단점:**
- 더 많은 파일 필요
- 중복 코드 가능성

### 접근법 4: 단일 함수 + 내부 라우팅
`api/index.py`에서 모든 경로 처리:
```python
def handler(request):
    path = request.path
    if path == '/api/generate':
        return handle_generate(request)
    elif path == '/api/health':
        return handle_health(request)
    # ...
```

**장점:**
- 단일 파일로 모든 엔드포인트 관리
- 공통 로직 재사용 용이

**단점:**
- 파일이 커질 수 있음
- 경로 관리 복잡

### 권장 접근법

**현재 프로젝트**: 접근법 1 (명시적 설정) + 접근법 4 (단일 함수)
- `vercel.json`으로 명시적 설정
- `api/index.py`에서 모든 요청 처리

**이유:**
- Vercel 설정 문제를 피할 수 있음
- 단일 엔드포인트로 CORS, 인증 등 공통 로직 관리 용이

## 추가 디버깅 체크리스트

### Vercel 대시보드 확인사항

1. **Deployments → 최신 배포**
   - [ ] Functions 탭에 `api/index` 함수가 있는가?
   - [ ] Runtime이 `python3.9` 또는 `@vercel/python`인가?
   - [ ] Build Logs에 Python 관련 메시지가 있는가?

2. **Settings → General**
   - [ ] Framework Preset이 `Other` 또는 `No Framework`인가?
   - [ ] Build Command가 비어있는가?
   - [ ] Output Directory가 비어있는가?

3. **Resources 탭**
   - [ ] Static Assets와 Serverless Functions가 모두 보이는가?
   - [ ] `api/index` 함수가 목록에 있는가?

### 로컬 테스트

```bash
# Vercel CLI로 로컬 테스트
npm i -g vercel
vercel dev

# 브라우저에서 http://localhost:3000/api 접속
# GET 요청으로 헬스 체크 확인
```

## 결론

404 오류의 근본 원인은 **Vercel이 Python 서버리스 함수를 인식하지 못하는 것**입니다. 이를 해결하려면:

1. **즉시**: `vercel.json`에 명시적 설정 추가
2. **확인**: Vercel 대시보드에서 Functions 탭 확인
3. **재배포**: 캐시 없이 재배포
4. **검증**: `/api` 엔드포인트 직접 접속 테스트

이 가이드를 따라하면 문제를 해결하고, 미래에 유사한 문제를 피할 수 있습니다.
