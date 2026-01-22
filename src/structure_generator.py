"""
Structure Generator 모듈
문서 구조 설계 및 분량 분배
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from src.models import (
    DocumentStructure, Section, DocumentMetadata,
    DocumentType, DocumentPurpose
)


class StructureGenerator:
    """문서 구조 생성기"""
    
    # 문서 유형별 구조 템플릿
    STRUCTURE_TEMPLATES = {
        DocumentType.REPORT.value: {
            "sections": [
                {"title": "서론", "level": 1, "ratio": 0.20},
                {"title": "본론", "level": 1, "ratio": 0.60},
                {"title": "결론", "level": 1, "ratio": 0.20},
            ],
            "subsections": {
                "서론": [
                    {"title": "연구 배경", "level": 2, "ratio": 0.5},
                    {"title": "연구 목적", "level": 2, "ratio": 0.5},
                ],
                "본론": [
                    {"title": "이론적 배경", "level": 2, "ratio": 0.3},
                    {"title": "주요 내용 분석", "level": 2, "ratio": 0.4},
                    {"title": "사례 및 적용", "level": 2, "ratio": 0.3},
                ],
                "결론": [
                    {"title": "요약", "level": 2, "ratio": 0.5},
                    {"title": "향후 전망", "level": 2, "ratio": 0.5},
                ],
            }
        },
        DocumentType.BUSINESS_REPORT.value: {
            "sections": [
                {"title": "배경", "level": 1, "ratio": 0.15},
                {"title": "문제점 분석", "level": 1, "ratio": 0.20},
                {"title": "상세 분석", "level": 1, "ratio": 0.30},
                {"title": "해결 방안", "level": 1, "ratio": 0.25},
                {"title": "기대 효과", "level": 1, "ratio": 0.10},
            ],
            "subsections": {}
        },
        DocumentType.ESSAY.value: {
            "sections": [
                {"title": "주장 제시", "level": 1, "ratio": 0.10},
                {"title": "근거 1", "level": 1, "ratio": 0.25},
                {"title": "근거 2", "level": 1, "ratio": 0.25},
                {"title": "반론 및 재반박", "level": 1, "ratio": 0.20},
                {"title": "결론", "level": 1, "ratio": 0.20},
            ],
            "subsections": {}
        },
        DocumentType.PROPOSAL.value: {
            "sections": [
                {"title": "기획 배경", "level": 1, "ratio": 0.15},
                {"title": "현황 분석", "level": 1, "ratio": 0.20},
                {"title": "기획 내용", "level": 1, "ratio": 0.35},
                {"title": "예상 효과", "level": 1, "ratio": 0.20},
                {"title": "실행 계획", "level": 1, "ratio": 0.10},
            ],
            "subsections": {}
        },
    }
    
    def generate(self, document_type: str, metadata: DocumentMetadata, topic: str) -> DocumentStructure:
        """
        문서 구조 생성
        
        Args:
            document_type: 문서 종류
            metadata: 문서 메타데이터
            topic: 주제
        
        Returns:
            DocumentStructure 객체
        """
        # 템플릿 선택
        template = self._get_template(document_type)
        
        # 섹션 생성
        sections = []
        order = 1
        
        for section_def in template["sections"]:
            # 메인 섹션
            section_length = int(metadata.target_length_chars * section_def["ratio"])
            
            # 서브섹션이 있는 경우
            if section_def["title"] in template.get("subsections", {}):
                subsections = template["subsections"][section_def["title"]]
                for subsec_def in subsections:
                    subsec_length = int(section_length * subsec_def["ratio"])
                    sections.append(Section(
                        title=subsec_def["title"],
                        level=subsec_def["level"],
                        content="",
                        target_length_chars=subsec_length,
                        order=order
                    ))
                    order += 1
            else:
                sections.append(Section(
                    title=section_def["title"],
                    level=section_def["level"],
                    content="",
                    target_length_chars=section_length,
                    order=order
                ))
                order += 1
        
        # 목차 생성
        outline = self._generate_outline(sections)
        
        return DocumentStructure(
            sections=sections,
            outline=outline
        )
    
    def _get_template(self, document_type: str) -> dict:
        """문서 유형에 맞는 템플릿 가져오기"""
        if document_type in self.STRUCTURE_TEMPLATES:
            return self.STRUCTURE_TEMPLATES[document_type]
        
        # 기본 템플릿 (레포트)
        return self.STRUCTURE_TEMPLATES[DocumentType.REPORT.value]
    
    def _generate_outline(self, sections: List[Section]) -> List[str]:
        """목차 생성"""
        outline = []
        for section in sections:
            indent = "  " * (section.level - 1)
            outline.append(f"{indent}{section.order}. {section.title}")
        return outline
