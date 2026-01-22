"""
Vercel Serverless Function for Document Auto Formatter API
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
    
    Args:
        request: Vercel request object with method, headers, body attributes
    
    Returns:
        Response dict with statusCode, headers, body
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
        # POST 요청 처리
        if request.method == 'POST':
            # 요청 본문 파싱
            body = {}
            if hasattr(request, 'body'):
                if isinstance(request.body, str):
                    body = json.loads(request.body)
                elif isinstance(request.body, dict):
                    body = request.body
                elif request.body:
                    try:
                        body = json.loads(request.body)
                    except:
                        body = {}
            
            # 사용자 입력 추출
            user_input = body.get('input', {})
            llm_provider_type = body.get('llm_provider_type', 'mock')
            
            # 문서 생성기 초기화
            formatter = DocumentAutoFormatter(llm_provider_type=llm_provider_type)
            
            # 문서 생성
            result = formatter.generate(user_input)
            
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
                    'version': '1.0.0'
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
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'message': f'서버 오류: {error_msg}'
            }, ensure_ascii=False)
        }
