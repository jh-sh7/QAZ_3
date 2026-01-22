"""
Input Parser 모듈
사용자 입력 파싱 및 검증, 기본값 추론
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from typing import Dict, Any, Optional
from src.models import UserInput, DocumentType, TargetAudience, WritingStyle


class InputParser:
    """사용자 입력 파서"""
    
    # 기본값 매핑
    DEFAULT_DOCUMENT_TYPE = DocumentType.REPORT.value
    DEFAULT_TARGET_AUDIENCE = TargetAudience.UNIVERSITY.value
    DEFAULT_WRITING_STYLE = WritingStyle.ACADEMIC.value
    DEFAULT_LENGTH = "A4 3장"
    
    # 분량 변환 (대략적)
    LENGTH_PATTERNS = {
        r"A4\s*(\d+)\s*장": lambda m: int(m.group(1)) * 2000,  # A4 1장 = 약 2000자
        r"(\d+)\s*장": lambda m: int(m.group(1)) * 2000,
        r"(\d+)\s*자": lambda m: int(m.group(1)),
        r"(\d+)\s*글자": lambda m: int(m.group(1)),
    }
    
    def parse(self, raw_input: Dict[str, Any]) -> UserInput:
        """
        원시 입력을 파싱하여 UserInput 객체로 변환
        
        Args:
            raw_input: 사용자 입력 딕셔너리
        
        Returns:
            UserInput 객체
        """
        # 기본값으로 초기화
        user_input = UserInput()
        
        # 각 필드 파싱
        user_input.document_type = self._parse_document_type(
            raw_input.get("document_type")
        )
        user_input.target_audience = self._parse_target_audience(
            raw_input.get("target_audience")
        )
        user_input.topic = self._parse_topic(raw_input.get("topic"))
        user_input.length = self._parse_length(raw_input.get("length"))
        user_input.writing_style = self._parse_writing_style(
            raw_input.get("writing_style")
        )
        user_input.required_keywords = self._parse_list(
            raw_input.get("required_keywords", [])
        )
        user_input.excluded_content = self._parse_list(
            raw_input.get("excluded_content", [])
        )
        user_input.evaluation_criteria = self._parse_list(
            raw_input.get("evaluation_criteria", [])
        )
        
        return user_input
    
    def _parse_document_type(self, value: Optional[str]) -> str:
        """문서 종류 파싱"""
        if not value:
            return self.DEFAULT_DOCUMENT_TYPE
        
        value = value.strip()
        
        # 키워드 매칭
        if any(kw in value for kw in ["레포트", "리포트", "report"]):
            return DocumentType.REPORT.value
        elif any(kw in value for kw in ["보고서", "보고"]):
            return DocumentType.BUSINESS_REPORT.value
        elif any(kw in value for kw in ["기획", "제안"]):
            return DocumentType.PROPOSAL.value
        elif any(kw in value for kw in ["실험", "실습"]):
            return DocumentType.EXPERIMENT_REPORT.value
        elif any(kw in value for kw in ["독서", "감상"]):
            return DocumentType.BOOK_REVIEW.value
        elif any(kw in value for kw in ["논술", "에세이"]):
            return DocumentType.ESSAY.value
        elif any(kw in value for kw in ["업무", "업보"]):
            return DocumentType.BUSINESS_DOCUMENT.value
        
        return value
    
    def _parse_target_audience(self, value: Optional[str]) -> str:
        """제출 대상 파싱"""
        if not value:
            return self.DEFAULT_TARGET_AUDIENCE
        
        value = value.strip()
        
        if any(kw in value for kw in ["중학", "중학교"]):
            return TargetAudience.MIDDLE_SCHOOL.value
        elif any(kw in value for kw in ["고등", "고등학교"]):
            return TargetAudience.HIGH_SCHOOL.value
        elif any(kw in value for kw in ["대학", "대학교", "대학원"]):
            return TargetAudience.UNIVERSITY.value
        elif any(kw in value for kw in ["회사", "기업", "직장"]):
            return TargetAudience.COMPANY.value
        elif any(kw in value for kw in ["공공", "기관", "정부"]):
            return TargetAudience.PUBLIC_AGENCY.value
        
        return value
    
    def _parse_topic(self, value: Optional[str]) -> str:
        """주제 파싱"""
        if not value:
            return "주제 미지정"
        return value.strip()
    
    def _parse_length(self, value: Optional[str]) -> str:
        """분량 파싱"""
        if not value:
            return self.DEFAULT_LENGTH
        
        value = value.strip()
        
        # 이미 적절한 형식인지 확인
        for pattern in self.LENGTH_PATTERNS.keys():
            if re.search(pattern, value, re.IGNORECASE):
                return value
        
        # 숫자만 있는 경우 "장" 추가
        if value.isdigit():
            return f"A4 {value}장"
        
        return value
    
    def _parse_writing_style(self, value: Optional[str]) -> str:
        """문체 파싱"""
        if not value:
            return self.DEFAULT_WRITING_STYLE
        
        value = value.strip()
        
        if any(kw in value for kw in ["설명", "설명형"]):
            return WritingStyle.EXPLANATORY.value
        elif any(kw in value for kw in ["논증", "논증형"]):
            return WritingStyle.ARGUMENTATIVE.value
        elif any(kw in value for kw in ["보고", "보고체"]):
            return WritingStyle.REPORT_STYLE.value
        elif any(kw in value for kw in ["서술", "서술형"]):
            return WritingStyle.NARRATIVE.value
        elif any(kw in value for kw in ["학술", "학술적"]):
            return WritingStyle.ACADEMIC.value
        
        return value
    
    def _parse_list(self, value: Any) -> list:
        """리스트 파싱"""
        if not value:
            return []
        if isinstance(value, str):
            # 쉼표로 구분된 문자열인 경우
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if item]
        return []
    
    def parse_length_to_chars(self, length_str: str) -> int:
        """
        분량 문자열을 글자 수로 변환
        
        Args:
            length_str: "A4 3장", "1500자" 등의 문자열
        
        Returns:
            글자 수
        """
        for pattern, converter in self.LENGTH_PATTERNS.items():
            match = re.search(pattern, length_str, re.IGNORECASE)
            if match:
                return converter(match)
        
        # 기본값: A4 3장 = 6000자
        return 6000
