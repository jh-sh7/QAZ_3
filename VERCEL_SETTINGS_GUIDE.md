# Vercel Build and Deployment 설정 가이드

## 현재 프로젝트 설정

### vercel.json (코드 기반 설정)
```json
{
  "buildCommand": "",
  "outputDirectory": ""
}
```

### Vercel 대시보드 설정 (권장)

**Build & Development Settings** 섹션에서:

1. **Framework Preset**
   - 선택: `Other` 또는 `No Framework`
   - 이유: Python 프로젝트이므로 프레임워크가 없음

2. **Build Command**
   - 값: **비워두기** (빈 문자열)
   - 이유: Python 서버리스 함수는 빌드 불필요

3. **Output Directory**
   - 값: **비워두기** (빈 문자열)
   - 이유: 정적 파일은 `public/` 폴더에서 자동 제공

4. **Install Command**
   - 값: **비워두기** 또는 `pip install -r requirements.txt` (의존성 필요시)
   - 현재: 표준 라이브러리만 사용하므로 비워도 됨

5. **Root Directory**
   - 값: `./` (기본값)
   - 이유: 프로젝트 루트가 저장소 루트와 동일

## 설정 우선순위

Vercel은 다음 순서로 설정을 적용합니다:

1. **vercel.json** (최우선)
2. **대시보드 설정** (vercel.json이 없을 때)
3. **자동 감지** (둘 다 없을 때)

## 현재 프로젝트 권장 설정

### ✅ 올바른 설정

**대시보드에서:**
```
Framework Preset: Other
Build Command: (비워두기)
Output Directory: (비워두기)
Install Command: (비워두기)
Root Directory: ./
```

**또는 vercel.json 사용:**
```json
{
  "buildCommand": "",
  "outputDirectory": ""
}
```

### ❌ 잘못된 설정

```
Framework Preset: Docusaurus, Next.js 등
Build Command: npm run build, docusaurus-build 등
Output Directory: .next, build 등
```

## Deployment Checks 설정

### Ignored Build Step
- **설정**: 비활성화 (기본값)
- **이유**: 모든 커밋에서 배포 필요

### Production Branch
- **설정**: `main` (기본값)
- **이유**: 메인 브랜치에서 프로덕션 배포

### Preview Deployments
- **설정**: 활성화 (기본값)
- **이유**: PR마다 프리뷰 배포 생성

## 문제 해결

### "docusaurus-build" 오류가 계속 발생하는 경우

1. **대시보드에서 Framework Preset 확인**
   - `Other` 또는 `No Framework`로 변경

2. **Build Command 확인**
   - 완전히 비워있는지 확인
   - 공백이나 줄바꿈이 있으면 제거

3. **vercel.json 확인**
   - `buildCommand: ""`로 명시적으로 설정

4. **프로젝트 재배포**
   - Settings → General → Redeploy

### NOT_FOUND 오류가 계속 발생하는 경우

1. **Output Directory 확인**
   - 비워있는지 확인
   - `public`로 설정되어 있으면 제거

2. **파일 구조 확인**
   ```
   public/index.html  ✅ 올바름
   index.html         ❌ 잘못됨
   ```

3. **배포 로그 확인**
   - Deployments → 최신 배포 → Logs
   - Functions 탭에서 API 함수 확인

## 설정 동기화

### vercel.json과 대시보드 설정이 다를 때

**우선순위**: vercel.json > 대시보드 설정

**권장 방법:**
- 코드 기반 설정(vercel.json) 사용
- 팀 협업 시 일관성 유지
- 버전 관리 가능

**또는:**
- 대시보드 설정만 사용
- vercel.json 제거
- 더 간단하지만 팀 동기화 어려움

## 체크리스트

배포 전 확인:
- [ ] Framework Preset이 "Other"로 설정됨
- [ ] Build Command가 비어있음
- [ ] Output Directory가 비어있음
- [ ] public/index.html 파일 존재
- [ ] api/*.py 파일들이 handler 함수 포함
- [ ] vercel.json이 올바르게 설정됨 (또는 없음)

## 참고 자료

- [Vercel Build Settings](https://vercel.com/docs/projects/project-configuration#build-and-development-settings)
- [Vercel Configuration](https://vercel.com/docs/projects/project-configuration)
- [Python Functions](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
