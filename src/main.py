"""
문서/레포트 자동 포맷 생성기 - 메인 실행 파일
"""
import sys
import os
# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.input_parser import InputParser
from src.document_analyzer import DocumentAnalyzer
from src.structure_generator import StructureGenerator
from src.content_generator import ContentGenerator
from src.formatter import Formatter
from src.llm_provider import get_llm_provider
from src.models import UserInput


class DocumentAutoFormatter:
    """문서 자동 포맷 생성기 메인 클래스"""
    
    def __init__(self, llm_provider_type: str = "mock", **llm_kwargs):
        """
        초기화
        
        Args:
            llm_provider_type: LLM 제공자 타입 ("mock" 또는 "openai")
            **llm_kwargs: LLM 제공자별 설정
        """
        self.input_parser = InputParser()
        self.document_analyzer = DocumentAnalyzer()
        self.structure_generator = StructureGenerator()
        self.llm_provider = get_llm_provider(llm_provider_type, **llm_kwargs)
        self.content_generator = ContentGenerator(self.llm_provider)
        self.formatter = Formatter()
    
    def generate(self, user_input_dict: dict) -> str:
        """
        문서 생성 메인 프로세스
        
        Args:
            user_input_dict: 사용자 입력 딕셔너리
        
        Returns:
            포맷팅된 문서 문자열
        """
        # 1. 입력 파싱
        print("[1단계] 사용자 입력 파싱 중...")
        user_input = self.input_parser.parse(user_input_dict)
        
        # 2. 분량 계산
        target_length_chars = self.input_parser.parse_length_to_chars(user_input.length)
        
        # 3. 문서 분석
        print("[2단계] 문서 목적 및 구조 분석 중...")
        metadata = self.document_analyzer.analyze(user_input, target_length_chars)
        
        # 4. 구조 생성
        print("[3단계] 문서 구조 설계 중...")
        structure = self.structure_generator.generate(
            user_input.document_type,
            metadata,
            user_input.topic
        )
        
        # 5. 내용 생성
        print("[4단계] 문서 내용 생성 중...")
        document = self.content_generator.generate(
            structure,
            metadata,
            user_input
        )
        
        # 6. 포맷팅
        print("[5단계] 문서 포맷팅 중...")
        formatted_document = self.formatter.format(document)
        
        print("문서 생성 완료!")
        return formatted_document
    
    def generate_and_save(self, user_input_dict: dict, output_path: str, format_type: str = "text"):
        """
        문서 생성 및 파일 저장
        
        Args:
            user_input_dict: 사용자 입력 딕셔너리
            output_path: 출력 파일 경로
            format_type: "text" 또는 "markdown"
        """
        # 1-5단계는 동일
        user_input = self.input_parser.parse(user_input_dict)
        target_length_chars = self.input_parser.parse_length_to_chars(user_input.length)
        metadata = self.document_analyzer.analyze(user_input, target_length_chars)
        structure = self.structure_generator.generate(
            user_input.document_type,
            metadata,
            user_input.topic
        )
        document = self.content_generator.generate(
            structure,
            metadata,
            user_input
        )
        
        # 파일 저장
        self.formatter.save_to_file(document, output_path, format_type)
        print(f"문서가 '{output_path}'에 저장되었습니다.")


def main():
    """메인 실행 함수"""
    # 예제 사용자 입력
    example_input = {
        "document_type": "과제 레포트",
        "target_audience": "대학교",
        "topic": "인공지능의 미래와 사회적 영향",
        "length": "A4 3장",
        "writing_style": "학술적",
        "required_keywords": ["AI", "머신러닝", "사회적 영향"],
        "evaluation_criteria": ["논리성", "객관성", "완전성"]
    }
    
    # 생성기 초기화 (Mock LLM 사용)
    formatter = DocumentAutoFormatter(llm_provider_type="mock")
    
    # 문서 생성
    result = formatter.generate(example_input)
    
    # 결과 출력
    print("\n" + "=" * 80)
    print("생성된 문서:")
    print("=" * 80)
    print(result)
    
    # 파일로 저장
    formatter.generate_and_save(example_input, "output_document.txt", format_type="text")
    formatter.generate_and_save(example_input, "output_document.md", format_type="markdown")


if __name__ == "__main__":
    main()
