# GitHub 업로드 및 Vercel 배포 가이드

## ✅ 완료된 작업

1. ✅ Git 저장소 초기화 완료
2. ✅ 모든 파일 커밋 완료
3. ✅ Vercel 배포 설정 완료
4. ✅ 웹 인터페이스 추가 완료

## 📤 GitHub에 업로드하기

### 방법 1: GitHub 웹사이트 사용

1. **GitHub 저장소 생성**
   - https://github.com/new 접속
   - Repository name 입력 (예: `document-auto-formatter`)
   - Public 또는 Private 선택
   - **중요**: README, .gitignore, license 추가하지 않기 (이미 있음)
   - "Create repository" 클릭

2. **로컬 저장소 연결 및 푸시**
   
   PowerShell 또는 명령 프롬프트에서 다음 명령어 실행:

   ```powershell
   # GitHub 저장소 URL을 원격 저장소로 추가
   # YOUR_USERNAME과 YOUR_REPO_NAME을 실제 값으로 변경하세요
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   
   # 메인 브랜치 확인
   git branch -M main
   
   # GitHub에 푸시
   git push -u origin main
   ```

   GitHub 인증이 필요하면:
   - Personal Access Token 사용 (Settings → Developer settings → Personal access tokens)
   - 또는 GitHub Desktop 사용

### 방법 2: GitHub CLI 사용

```powershell
# GitHub CLI 설치 (없는 경우)
# winget install GitHub.cli

# 저장소 생성 및 푸시
gh repo create document-auto-formatter --public --source=. --remote=origin --push
```

## 🚀 Vercel 배포하기

### 방법 1: Vercel 웹 대시보드 (권장)

1. **Vercel 가입/로그인**
   - https://vercel.com 접속
   - "Sign Up" → GitHub 계정으로 로그인

2. **프로젝트 가져오기**
   - 대시보드에서 "Add New..." → "Project" 클릭
   - GitHub 저장소 선택
   - "Import" 클릭

3. **프로젝트 설정**
   - Framework Preset: **"Other"** 선택
   - Root Directory: `./` (기본값 유지)
   - Build Command: **비워두기**
   - Output Directory: **비워두기**
   - Install Command: **비워두기** (표준 라이브러리만 사용)

4. **환경 변수** (선택사항)
   - OpenAI API를 사용하는 경우:
     - Key: `OPENAI_API_KEY`
     - Value: 실제 API 키

5. **배포**
   - "Deploy" 버튼 클릭
   - 배포 완료 대기 (약 1-2분)
   - 배포 완료 후 제공되는 URL 확인

### 방법 2: Vercel CLI

```powershell
# Vercel CLI 설치
npm install -g vercel

# 프로젝트 디렉토리에서
cd C:\Users\S\Desktop\QAZ_3#

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

## 🌐 배포 후 접속

배포가 완료되면:

- **웹 인터페이스**: `https://YOUR_PROJECT.vercel.app`
- **API 엔드포인트**: `https://YOUR_PROJECT.vercel.app/api/generate`

## 📝 사용 예제

### 웹 인터페이스 사용

1. 배포된 URL로 접속
2. 폼에 정보 입력
3. "문서 생성하기" 버튼 클릭
4. 생성된 문서 확인

### API 직접 호출

```javascript
fetch('https://YOUR_PROJECT.vercel.app/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    input: {
      document_type: '과제 레포트',
      target_audience: '대학교',
      topic: '인공지능의 미래와 사회적 영향',
      length: 'A4 3장',
      writing_style: '학술적',
      required_keywords: ['AI', '머신러닝'],
      evaluation_criteria: ['논리성', '객관성']
    },
    llm_provider_type: 'mock'
  })
})
.then(res => res.json())
.then(data => {
  console.log('생성된 문서:', data.document);
});
```

## ⚠️ 주의사항

1. **타임아웃 제한**
   - Vercel 무료 플랜: 10초 타임아웃
   - Hobby 플랜: 60초 타임아웃
   - 문서 생성이 오래 걸리면 타임아웃될 수 있음

2. **Python 버전**
   - Vercel은 Python 3.9를 기본으로 사용
   - `vercel.json`에서 설정 가능

3. **의존성**
   - 현재는 표준 라이브러리만 사용
   - 외부 패키지가 필요하면 `requirements.txt`에 추가

## 🔧 문제 해결

### 모듈을 찾을 수 없음
- `vercel.json`의 경로 설정 확인
- `api/` 폴더의 파일명 확인

### CORS 오류
- `api/index.py`와 `api/generate.py`의 CORS 헤더 확인

### 배포 실패
- Vercel 대시보드의 로그 확인
- `requirements.txt` 확인

## 📚 추가 리소스

- [Vercel Python 문서](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [GitHub 문서](https://docs.github.com)
