"""
Formatter 모듈
최종 문서 포맷팅 및 출력
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import GeneratedDocument


class Formatter:
    """문서 포맷터"""
    
    def format(self, document: GeneratedDocument) -> str:
        """
        문서를 최종 포맷으로 변환
        
        Args:
            document: 생성된 문서
        
        Returns:
            포맷팅된 문자열
        """
        parts = []
        
        # [1] 전체 문서 개요
        parts.append("=" * 80)
        parts.append("[1] 전체 문서 개요")
        parts.append("=" * 80)
        parts.append("")
        parts.append(document.overview)
        parts.append("")
        parts.append("전체 구조:")
        for item in document.structure_summary:
            parts.append(f"  {item}")
        parts.append("")
        parts.append("")
        
        # [2] 자동 생성된 문서 본문
        parts.append("=" * 80)
        parts.append("[2] 자동 생성된 문서 본문")
        parts.append("=" * 80)
        parts.append("")
        parts.append(document.content)
        parts.append("")
        
        # [3] 제출용 체크포인트
        parts.append("=" * 80)
        parts.append("[3] 제출용 체크포인트")
        parts.append("=" * 80)
        parts.append("")
        for checkpoint in document.checkpoints:
            parts.append(checkpoint)
        parts.append("")
        
        return "\n".join(parts)
    
    def format_markdown(self, document: GeneratedDocument) -> str:
        """마크다운 형식으로 포맷팅"""
        parts = []
        
        # 제목
        parts.append("# 문서/레포트 자동 생성 결과\n")
        
        # 개요
        parts.append("## 📋 전체 문서 개요\n")
        parts.append(document.overview)
        parts.append("\n")
        
        # 구조
        parts.append("### 문서 구조\n")
        for item in document.structure_summary:
            parts.append(f"- {item}")
        parts.append("\n")
        
        # 본문
        parts.append("## 📄 자동 생성된 문서 본문\n")
        parts.append(document.content)
        parts.append("\n")
        
        # 체크포인트
        parts.append("## ✅ 제출용 체크포인트\n")
        for checkpoint in document.checkpoints:
            parts.append(f"- {checkpoint}")
        parts.append("\n")
        
        return "\n".join(parts)
    
    def save_to_file(self, document: GeneratedDocument, filepath: str, format_type: str = "text"):
        """
        파일로 저장
        
        Args:
            document: 생성된 문서
            filepath: 저장 경로
            format_type: "text" 또는 "markdown"
        """
        if format_type == "markdown":
            content = self.format_markdown(document)
        else:
            content = self.format(document)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
