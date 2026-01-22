"""
Document Analyzer 모듈
문서 목적 분석, 난이도 및 문체 결정
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import (
    UserInput, DocumentMetadata, DocumentPurpose,
    DocumentType, TargetAudience, WritingStyle
)


class DocumentAnalyzer:
    """문서 분석기"""
    
    # 문서 종류별 목적 매핑
    DOCUMENT_PURPOSE_MAP = {
        DocumentType.REPORT.value: DocumentPurpose.EXPLANATORY,
        DocumentType.BUSINESS_REPORT.value: DocumentPurpose.REPORTING,
        DocumentType.PROPOSAL.value: DocumentPurpose.PERSUASIVE,
        DocumentType.EXPERIMENT_REPORT.value: DocumentPurpose.REPORTING,
        DocumentType.BOOK_REVIEW.value: DocumentPurpose.EVALUATION,
        DocumentType.ESSAY.value: DocumentPurpose.PERSUASIVE,
        DocumentType.BUSINESS_DOCUMENT.value: DocumentPurpose.REPORTING,
    }
    
    # 제출 대상별 난이도 매핑
    DIFFICULTY_MAP = {
        TargetAudience.MIDDLE_SCHOOL.value: {
            "vocabulary_level": "기본",
            "sentence_complexity": "단순",
            "explanation_depth": "기초"
        },
        TargetAudience.HIGH_SCHOOL.value: {
            "vocabulary_level": "일반",
            "sentence_complexity": "중간",
            "explanation_depth": "중급"
        },
        TargetAudience.UNIVERSITY.value: {
            "vocabulary_level": "학술용어_포함",
            "sentence_complexity": "복잡",
            "explanation_depth": "심화"
        },
        TargetAudience.COMPANY.value: {
            "vocabulary_level": "전문용어_포함",
            "sentence_complexity": "간결",
            "explanation_depth": "실무"
        },
        TargetAudience.PUBLIC_AGENCY.value: {
            "vocabulary_level": "공식용어_포함",
            "sentence_complexity": "명확",
            "explanation_depth": "공식"
        },
    }
    
    def analyze(self, user_input: UserInput, target_length_chars: int) -> DocumentMetadata:
        """
        사용자 입력을 분석하여 문서 메타데이터 생성
        
        Args:
            user_input: 사용자 입력
            target_length_chars: 목표 글자 수
        
        Returns:
            DocumentMetadata 객체
        """
        # 문서 목적 결정
        purpose = self._determine_purpose(user_input)
        
        # 난이도 및 문체 결정
        difficulty_info = self._determine_difficulty(user_input)
        
        # 평가 기준 추출
        evaluation_focus = self._extract_evaluation_criteria(user_input)
        
        # 페이지 수 계산 (대략적: A4 1장 = 2000자)
        target_length_pages = (target_length_chars + 1999) // 2000
        
        return DocumentMetadata(
            purpose=purpose,
            difficulty_level=user_input.target_audience,
            vocabulary_level=difficulty_info["vocabulary_level"],
            sentence_complexity=difficulty_info["sentence_complexity"],
            evaluation_focus=evaluation_focus,
            target_length_chars=target_length_chars,
            target_length_pages=target_length_pages
        )
    
    def _determine_purpose(self, user_input: UserInput) -> DocumentPurpose:
        """문서 목적 결정"""
        # 문서 종류 기반 매핑
        if user_input.document_type in self.DOCUMENT_PURPOSE_MAP:
            return self.DOCUMENT_PURPOSE_MAP[user_input.document_type]
        
        # 문체 기반 추론
        if user_input.writing_style == WritingStyle.ARGUMENTATIVE.value:
            return DocumentPurpose.PERSUASIVE
        elif user_input.writing_style == WritingStyle.REPORT_STYLE.value:
            return DocumentPurpose.REPORTING
        elif user_input.writing_style == WritingStyle.ACADEMIC.value:
            return DocumentPurpose.EXPLANATORY
        
        # 기본값
        return DocumentPurpose.EXPLANATORY
    
    def _determine_difficulty(self, user_input: UserInput) -> dict:
        """난이도 및 문체 결정"""
        target = user_input.target_audience
        
        if target in self.DIFFICULTY_MAP:
            base_info = self.DIFFICULTY_MAP[target].copy()
        else:
            # 기본값 (대학교 수준)
            base_info = self.DIFFICULTY_MAP[TargetAudience.UNIVERSITY.value].copy()
        
        # 문체에 따른 조정
        if user_input.writing_style == WritingStyle.ACADEMIC.value:
            base_info["vocabulary_level"] = "학술용어_포함"
            base_info["sentence_complexity"] = "복잡"
        elif user_input.writing_style == WritingStyle.REPORT_STYLE.value:
            base_info["sentence_complexity"] = "간결"
        
        return base_info
    
    def _extract_evaluation_criteria(self, user_input: UserInput) -> list:
        """평가 기준 추출"""
        if user_input.evaluation_criteria:
            return user_input.evaluation_criteria
        
        # 기본 평가 기준 (문서 목적 기반)
        purpose = self._determine_purpose(user_input)
        
        default_criteria = {
            DocumentPurpose.EXPLANATORY: ["명확성", "체계성", "완전성"],
            DocumentPurpose.PERSUASIVE: ["논리성", "설득력", "근거의 타당성"],
            DocumentPurpose.REPORTING: ["객관성", "정확성", "완전성"],
            DocumentPurpose.EVALUATION: ["비판적 사고", "객관성", "깊이"]
        }
        
        return default_criteria.get(purpose, ["논리성", "객관성", "완전성"])
