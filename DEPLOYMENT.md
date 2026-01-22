# 배포 가이드 (Deployment Guide)

## GitHub 업로드

### 1. GitHub 저장소 생성

1. GitHub에 로그인하고 https://github.com/new 에서 새 저장소를 생성합니다.
2. 저장소 이름을 입력하고 (예: `document-auto-formatter`) 생성합니다.
3. **중요**: README, .gitignore, license를 추가하지 마세요 (이미 있음)

### 2. 로컬 저장소를 GitHub에 연결

터미널에서 다음 명령어를 실행하세요:

```bash
# GitHub 저장소 URL을 원격 저장소로 추가
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 또는 SSH 사용 시
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# 메인 브랜치를 main으로 설정 (필요한 경우)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3. GitHub CLI 사용 (선택사항)

GitHub CLI가 설치되어 있다면:

```bash
gh repo create document-auto-formatter --public --source=. --remote=origin --push
```

## Vercel 배포

### 방법 1: Vercel 웹 대시보드 사용

1. **Vercel 가입/로그인**
   - https://vercel.com 에서 GitHub 계정으로 로그인

2. **프로젝트 가져오기**
   - "Add New..." → "Project" 클릭
   - GitHub 저장소 선택
   - "Import" 클릭

3. **프로젝트 설정**
   - Framework Preset: "Other" 선택
   - Root Directory: `./` (기본값)
   - Build Command: 비워두기 (Python은 빌드 불필요)
   - Output Directory: 비워두기
   - Install Command: `pip install -r requirements.txt` (필요한 경우)

4. **환경 변수 설정** (선택사항)
   - OpenAI API 키가 필요한 경우:
     - Key: `OPENAI_API_KEY`
     - Value: 실제 API 키

5. **배포**
   - "Deploy" 버튼 클릭
   - 배포 완료 후 제공되는 URL로 접속

### 방법 2: Vercel CLI 사용

```bash
# Vercel CLI 설치
npm i -g vercel

# 프로젝트 디렉토리에서 배포
vercel

# 프로덕션 배포
vercel --prod
```

### 배포 후 확인

배포가 완료되면:
- 웹 인터페이스: `https://YOUR_PROJECT.vercel.app`
- API 엔드포인트: `https://YOUR_PROJECT.vercel.app/api/generate`

### API 사용 예제

```javascript
// POST 요청
fetch('https://YOUR_PROJECT.vercel.app/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    input: {
      document_type: '과제 레포트',
      target_audience: '대학교',
      topic: '인공지능의 미래',
      length: 'A4 3장',
      writing_style: '학술적'
    },
    llm_provider_type: 'mock'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## 문제 해결

### Python 모듈 import 오류

Vercel에서 Python 모듈을 찾지 못하는 경우:
- `vercel.json`의 경로 설정 확인
- `requirements.txt`에 필요한 패키지 추가

### 타임아웃 오류

문서 생성에 시간이 오래 걸리는 경우:
- Vercel의 무료 플랜은 10초 타임아웃 제한이 있습니다
- Hobby 플랜은 60초까지 지원합니다

### CORS 오류

프론트엔드에서 API 호출 시 CORS 오류가 발생하면:
- `api/index.py`와 `api/generate.py`의 CORS 헤더 확인
- Vercel의 자동 CORS 처리 확인

## 추가 리소스

- [Vercel Python 문서](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [GitHub Actions로 자동 배포 설정](https://vercel.com/docs/concepts/git)
