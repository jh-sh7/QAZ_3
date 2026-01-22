"""
데이터 모델 정의
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class DocumentType(str, Enum):
    """문서 종류"""
    REPORT = "과제 레포트"
    BUSINESS_REPORT = "보고서"
    PROPOSAL = "기획서"
    EXPERIMENT_REPORT = "실험 보고서"
    BOOK_REVIEW = "독서감상문"
    ESSAY = "논술문"
    BUSINESS_DOCUMENT = "업무 보고"


class TargetAudience(str, Enum):
    """제출 대상"""
    MIDDLE_SCHOOL = "중학교"
    HIGH_SCHOOL = "고등학교"
    UNIVERSITY = "대학교"
    COMPANY = "회사"
    PUBLIC_AGENCY = "공공기관"


class WritingStyle(str, Enum):
    """문체"""
    EXPLANATORY = "설명형"
    ARGUMENTATIVE = "논증형"
    REPORT_STYLE = "보고체"
    NARRATIVE = "서술형"
    ACADEMIC = "학술적"


class DocumentPurpose(str, Enum):
    """문서 목적"""
    EXPLANATORY = "설명용"
    PERSUASIVE = "설득용"
    REPORTING = "보고용"
    EVALUATION = "평가용"


@dataclass
class UserInput:
    """사용자 입력 데이터"""
    document_type: Optional[str] = None
    target_audience: Optional[str] = None
    topic: Optional[str] = None
    length: Optional[str] = None
    writing_style: Optional[str] = None
    required_keywords: List[str] = field(default_factory=list)
    excluded_content: List[str] = field(default_factory=list)
    evaluation_criteria: List[str] = field(default_factory=list)


@dataclass
class DocumentMetadata:
    """문서 메타데이터 (분석 결과)"""
    purpose: DocumentPurpose
    difficulty_level: str
    vocabulary_level: str
    sentence_complexity: str
    evaluation_focus: List[str]
    target_length_chars: int
    target_length_pages: Optional[int] = None


@dataclass
class Section:
    """문서 섹션"""
    title: str
    level: int  # 제목 레벨 (1, 2, 3...)
    content: str
    target_length_chars: int
    order: int


@dataclass
class DocumentStructure:
    """문서 구조"""
    sections: List[Section]
    outline: List[str]  # 목차


@dataclass
class GeneratedDocument:
    """생성된 문서"""
    overview: str
    structure_summary: List[str]
    content: str
    checkpoints: List[str]
    metadata: DocumentMetadata
