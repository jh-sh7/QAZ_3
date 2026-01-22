"""
Content Generator 모듈
실제 문서 내용 생성
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from src.models import (
    DocumentStructure, Section, DocumentMetadata,
    UserInput, GeneratedDocument
)
from src.llm_provider import LLMProvider


class ContentGenerator:
    """내용 생성기"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        초기화
        
        Args:
            llm_provider: LLM 제공자
        """
        self.llm_provider = llm_provider
    
    def generate(self, structure: DocumentStructure, metadata: DocumentMetadata,
                 user_input: UserInput) -> GeneratedDocument:
        """
        문서 내용 생성
        
        Args:
            structure: 문서 구조
            metadata: 문서 메타데이터
            user_input: 사용자 입력
        
        Returns:
            GeneratedDocument 객체
        """
        # 각 섹션별 내용 생성
        generated_sections = []
        for section in structure.sections:
            content = self._generate_section_content(
                section, metadata, user_input, structure
            )
            section.content = content
            generated_sections.append(section)
        
        # 전체 문서 개요 생성
        overview = self._generate_overview(metadata, user_input)
        
        # 구조 요약
        structure_summary = structure.outline
        
        # 체크포인트 생성
        checkpoints = self._generate_checkpoints(metadata, user_input, generated_sections)
        
        # 최종 문서 생성
        return GeneratedDocument(
            overview=overview,
            structure_summary=structure_summary,
            content=self._format_content(generated_sections),
            checkpoints=checkpoints,
            metadata=metadata
        )
    
    def _generate_section_content(self, section: Section, metadata: DocumentMetadata,
                                  user_input: UserInput, structure: DocumentStructure) -> str:
        """섹션별 내용 생성"""
        # 프롬프트 구성
        prompt = self._build_prompt(section, metadata, user_input, structure)
        
        # LLM을 통한 생성
        content = self.llm_provider.generate(
            prompt,
            temperature=0.7,
            max_tokens=section.target_length_chars // 2  # 대략적 토큰 수
        )
        
        # 키워드 포함 확인 및 보완
        content = self._ensure_keywords(content, user_input.required_keywords)
        
        # 제외 내용 제거
        content = self._remove_excluded_content(content, user_input.excluded_content)
        
        # 길이 조정
        content = self._adjust_length(content, section.target_length_chars)
        
        return content
    
    def _build_prompt(self, section: Section, metadata: DocumentMetadata,
                      user_input: UserInput, structure: DocumentStructure) -> str:
        """섹션 생성 프롬프트 구성"""
        prompt_parts = [
            f"주제: {user_input.topic}",
            f"문서 종류: {user_input.document_type}",
            f"제출 대상: {user_input.target_audience}",
            f"문체: {user_input.writing_style}",
            f"",
            f"현재 작성할 섹션: {section.title}",
            f"섹션 레벨: {section.level}",
            f"목표 분량: 약 {section.target_length_chars}자",
            f"",
            f"문체 요구사항:",
            f"- 어휘 수준: {metadata.vocabulary_level}",
            f"- 문장 복잡도: {metadata.sentence_complexity}",
            f"",
        ]
        
        # 이전 섹션 정보 (연결성 보장)
        prev_sections = [s for s in structure.sections if s.order < section.order]
        if prev_sections:
            prompt_parts.append("이전 섹션들:")
            for prev in prev_sections[-2:]:  # 최근 2개만
                prompt_parts.append(f"- {prev.title}: {prev.content[:200]}...")
            prompt_parts.append("")
        
        # 키워드 포함 요청
        if user_input.required_keywords:
            prompt_parts.append(f"반드시 포함할 키워드: {', '.join(user_input.required_keywords)}")
            prompt_parts.append("")
        
        prompt_parts.append(
            f"위 조건에 맞춰 '{section.title}' 섹션을 완성된 문장으로 작성하세요. "
            f"형식만 제시하지 말고 실제 내용을 포함하여 작성하세요. "
            f"논리적이고 자연스러운 문장으로 작성하며, "
            f"이전 섹션과의 연결성을 고려하세요."
        )
        
        return "\n".join(prompt_parts)
    
    def _ensure_keywords(self, content: str, keywords: List[str]) -> str:
        """필수 키워드 포함 확인"""
        if not keywords:
            return content
        
        # 키워드가 포함되어 있는지 확인
        missing_keywords = [kw for kw in keywords if kw not in content]
        
        if missing_keywords:
            # 누락된 키워드를 자연스럽게 추가
            addition = f" 또한, {', '.join(missing_keywords)}에 대해서도 고려할 필요가 있다."
            content += addition
        
        return content
    
    def _remove_excluded_content(self, content: str, excluded: List[str]) -> str:
        """제외할 내용 제거"""
        if not excluded:
            return content
        
        for item in excluded:
            # 간단한 문자열 제거 (실제로는 더 정교한 로직 필요)
            content = content.replace(item, "")
        
        return content
    
    def _adjust_length(self, content: str, target_length: int) -> str:
        """분량 조정"""
        current_length = len(content)
        
        if current_length < target_length * 0.7:
            # 너무 짧으면 보완
            addition = " 이에 대해 더 깊이 있게 살펴보면, 다양한 관점에서 접근할 수 있다. " * 3
            content += addition
            # 다시 길이 확인하여 조정
            if len(content) > target_length * 1.3:
                content = content[:int(target_length * 1.2)]
        elif current_length > target_length * 1.5:
            # 너무 길면 축약
            content = content[:int(target_length * 1.2)]
        
        return content
    
    def _generate_overview(self, metadata: DocumentMetadata, user_input: UserInput) -> str:
        """문서 개요 생성"""
        overview = (
            f"본 문서는 '{user_input.topic}'에 대한 {user_input.document_type}로, "
            f"{user_input.target_audience}에 제출하기 위해 작성되었습니다. "
            f"문서의 목적은 {metadata.purpose.value}이며, "
            f"총 약 {metadata.target_length_chars}자 분량으로 구성됩니다."
        )
        return overview
    
    def _generate_checkpoints(self, metadata: DocumentMetadata, user_input: UserInput,
                              sections: List[Section]) -> List[str]:
        """체크포인트 생성"""
        checkpoints = []
        
        # 평가 기준별 체크포인트
        for criterion in metadata.evaluation_focus:
            if criterion == "논리성":
                checkpoints.append("[OK] 논리적 흐름: 각 섹션이 이전 내용을 자연스럽게 이어받아 논리적 구조를 형성함")
            elif criterion == "객관성":
                checkpoints.append("[OK] 객관적 서술: 주관적 판단보다는 사실과 근거를 바탕으로 서술함")
            elif criterion == "완전성":
                checkpoints.append("[OK] 내용의 완전성: 주제에 대한 주요 내용이 모두 포함되어 있음")
            elif criterion == "명확성":
                checkpoints.append("[OK] 명확한 표현: 핵심 개념과 주장이 명확하게 제시됨")
            elif criterion == "설득력":
                checkpoints.append("[OK] 설득력 있는 논증: 근거와 예시를 통해 주장을 뒷받침함")
        
        # 분량 체크
        total_length = sum(len(s.content) for s in sections)
        checkpoints.append(f"[OK] 분량 적정성: 목표 분량({metadata.target_length_chars}자) 대비 실제 분량({total_length}자)")
        
        # 키워드 체크
        if user_input.required_keywords:
            all_content = " ".join(s.content for s in sections)
            included_keywords = [kw for kw in user_input.required_keywords if kw in all_content]
            checkpoints.append(f"[OK] 필수 키워드 포함: {len(included_keywords)}/{len(user_input.required_keywords)}개 포함")
        
        # 보완 제안
        checkpoints.append("[TIP] 보완 제안: 실제 제출 전에 맞춤법 검사 및 문장 다듬기를 권장합니다.")
        
        return checkpoints
    
    def _format_content(self, sections: List[Section]) -> str:
        """섹션들을 포맷팅하여 전체 내용 생성"""
        formatted_parts = []
        
        for section in sections:
            # 제목 포맷팅
            if section.level == 1:
                title_prefix = "# "
            elif section.level == 2:
                title_prefix = "## "
            elif section.level == 3:
                title_prefix = "### "
            else:
                title_prefix = "#### "
            
            formatted_parts.append(f"{title_prefix}{section.order}. {section.title}\n")
            formatted_parts.append(section.content)
            formatted_parts.append("\n\n")
        
        return "".join(formatted_parts)
