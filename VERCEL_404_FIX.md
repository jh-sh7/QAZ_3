# Vercel 404 오류 해결 가이드

## 현재 상황
- `/api` 엔드포인트가 404를 반환
- F12 오류는 없음 (프론트엔드 정상)
- Vercel이 Python 서버리스 함수를 인식하지 못함

## 확인해야 할 사항

### 1. Vercel 대시보드 - Functions 탭

**경로**: 프로젝트 → Deployments → 최신 배포 → Functions 탭

**확인 사항**:
- `api/index` 함수가 목록에 있는가?
- Runtime이 `python3.9`로 표시되는가?
- 함수가 없다면 → Vercel이 Python 파일을 인식하지 못함

### 2. Vercel 대시보드 - Build Logs

**경로**: 프로젝트 → Deployments → 최신 배포 → Build Logs

**확인 사항**:
- Python 관련 오류 메시지
- "Function not found" 오류
- "Module not found" 오류
- Import 오류

### 3. Vercel 대시보드 - 프로젝트 설정

**경로**: 프로젝트 → Settings → General

**확인 사항**:
- Framework Preset: `Other` 또는 `No Framework`
- Build Command: **비워두기** (빈 문자열)
- Output Directory: **비워두기** (빈 문자열)
- Install Command: **비워두기**

## 해결 방법

### 방법 1: 수동 재배포 (권장)

1. Vercel 대시보드 접속
2. 프로젝트 → Deployments
3. 최신 배포 옆 "..." 메뉴 클릭
4. "Redeploy" 선택
5. **"Use existing Build Cache" 체크 해제** (중요!)
6. "Redeploy" 클릭

### 방법 2: Vercel CLI로 재배포

```bash
# Vercel CLI 설치 (없는 경우)
npm install -g vercel

# 프로젝트 디렉토리에서
vercel --prod --force
```

### 방법 3: GitHub에서 재배포 트리거

1. 빈 커밋 생성
2. GitHub에 푸시
3. Vercel이 자동으로 재배포

## 파일 구조 확인

현재 구조:
```
api/
├── index.py     → /api (자동 인식되어야 함)
└── generate.py  → /api/generate (자동 인식되어야 함)
```

Vercel은 `api/` 폴더의 `.py` 파일을 자동으로 서버리스 함수로 인식해야 합니다.

## 디버깅 정보

### api/index.py 확인 사항

1. `handler(request)` 함수가 있는가? ✅
2. 올바른 응답 형식을 반환하는가? ✅
3. Import 오류가 없는가? ✅

### Vercel 로그 확인

배포 로그에서 다음을 확인:
- Python 파일이 빌드되는가?
- `handler` 함수가 인식되는가?
- Import 오류가 있는가?

## 대안: Vercel 프로젝트 재생성

만약 위 방법이 모두 실패한다면:

1. Vercel 대시보드에서 프로젝트 삭제
2. 새 프로젝트 생성
3. 같은 GitHub 저장소 연결
4. Framework Preset: `Other` 선택
5. Build Command: 비워두기
6. 재배포

## 예상 원인

1. **Vercel 캐시 문제**: 이전 배포의 잘못된 설정이 캐시됨
2. **프로젝트 설정 충돌**: 대시보드 설정과 코드 불일치
3. **Python 인식 실패**: Vercel이 Python 파일을 서버리스 함수로 인식하지 못함

## 다음 단계

1. Vercel 대시보드에서 Functions 탭 확인
2. Functions 탭 스크린샷 공유 (함수 목록)
3. Build Logs의 오류 메시지 공유
4. 위 정보를 바탕으로 추가 해결책 제시
