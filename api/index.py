"""
Vercel Serverless Function for Document Auto Formatter API
모든 /api/* 요청을 처리합니다.
"""
import sys
import os
import json

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.main import DocumentAutoFormatter


def handler(request):
    """
    Vercel Serverless Function Handler
    
    모든 /api/* 요청을 처리합니다.
    POST 요청: 문서 생성
    GET 요청: 헬스 체크
    """
    # CORS 헤더 설정
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    # OPTIONS 요청 처리 (CORS preflight)
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # POST 요청 처리 (문서 생성)
        if request.method == 'POST':
            # 요청 본문 파싱
            body = {}
            try:
                if hasattr(request, 'body'):
                    if isinstance(request.body, str):
                        body = json.loads(request.body) if request.body else {}
                    elif isinstance(request.body, dict):
                        body = request.body
                    elif request.body:
                        body = json.loads(request.body)
            except json.JSONDecodeError as e:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'success': False,
                        'message': f'JSON 파싱 오류: {str(e)}'
                    }, ensure_ascii=False)
                }
            
            # 사용자 입력 추출
            user_input = body.get('input', {})
            if not user_input:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'success': False,
                        'message': '입력 데이터가 없습니다. "input" 필드가 필요합니다.'
                    }, ensure_ascii=False)
                }
            
            # 안전장치: 항상 'mock' 사용 (요금 방지)
            llm_provider_type = 'mock'
            
            # 문서 생성기 초기화
            try:
                formatter = DocumentAutoFormatter(llm_provider_type=llm_provider_type)
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                print(f"Formatter initialization error: {error_trace}")
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'success': False,
                        'message': f'문서 생성기 초기화 실패: {str(e)}'
                    }, ensure_ascii=False)
                }
            
            # 문서 생성
            try:
                result = formatter.generate(user_input)
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                print(f"Document generation error: {str(e)}")
                print(f"Traceback: {error_trace}")
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'success': False,
                        'message': f'문서 생성 오류: {str(e)}',
                        'error_type': type(e).__name__
                    }, ensure_ascii=False)
                }
            
            # 응답 반환
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'document': result,
                    'message': '문서가 성공적으로 생성되었습니다.'
                }, ensure_ascii=False)
            }
        
        # GET 요청 처리 (헬스 체크)
        elif request.method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'message': 'Document Auto Formatter API is running',
                    'version': '1.0.0',
                    'endpoints': {
                        'generate': '/api (POST) - 문서 생성',
                        'health': '/api (GET) - 상태 확인'
                    }
                }, ensure_ascii=False)
            }
        
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'message': 'Method not allowed'
                }, ensure_ascii=False)
            }
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        print(f"Unexpected error: {error_msg}")
        print(f"Traceback: {error_trace}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'message': f'서버 오류: {error_msg}',
                'error_type': type(e).__name__
            }, ensure_ascii=False)
        }
