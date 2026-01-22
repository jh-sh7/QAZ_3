"""
LLM 추상화 레이어
LLM 교체가 가능하도록 인터페이스 정의
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LLMProvider(ABC):
    """LLM 제공자 추상 클래스"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        텍스트 생성
        
        Args:
            prompt: 프롬프트
            **kwargs: 추가 파라미터 (temperature, max_tokens 등)
        
        Returns:
            생성된 텍스트
        """
        pass


class MockLLMProvider(LLMProvider):
    """
    테스트용 Mock LLM 제공자
    실제 LLM API 없이도 동작하도록 구현
    """
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Mock 응답 생성"""
        # 실제 구현에서는 LLM API를 호출
        # 여기서는 간단한 템플릿 기반 응답 생성
        
        if "서론" in prompt or "도입" in prompt:
            return """본 문서는 [주제]에 대해 체계적으로 분석하고 논의하기 위해 작성되었다. 
현대 사회에서 [주제]는 중요한 의미를 갖고 있으며, 이에 대한 깊이 있는 이해가 필요하다. 
이 글에서는 [주제]의 배경, 주요 내용, 그리고 향후 전망을 다룬다."""
        
        elif "본론" in prompt or "분석" in prompt:
            return """[주제]에 대한 분석을 시작하자면, 먼저 핵심 개념을 명확히 정의할 필요가 있다. 
[주제]는 다음과 같은 특징을 가진다: 첫째, [특징1]. 둘째, [특징2]. 셋째, [특징3]. 
이러한 특징들은 서로 밀접하게 연관되어 있으며, 종합적으로 이해해야 한다. 
또한, [주제]와 관련된 다양한 관점들이 존재한다. 한 관점에서는 [관점1]을 강조하는 반면, 
다른 관점에서는 [관점2]를 중시한다. 이러한 다양한 접근 방식은 [주제]의 복잡성을 보여준다."""
        
        elif "결론" in prompt:
            return """이상의 논의를 통해 [주제]에 대한 종합적인 이해를 도모할 수 있었다. 
주요 내용을 요약하면 다음과 같다: [요약1], [요약2], [요약3]. 
앞으로 [주제]는 더욱 발전할 것으로 예상되며, 지속적인 관심과 연구가 필요하다."""
        
        else:
            return f"[주제]에 대한 내용: {prompt[:100]}... (실제 LLM 연동 시 더 상세한 내용이 생성됩니다.)"


class OpenAIProvider(LLMProvider):
    """OpenAI API 제공자"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """OpenAI API를 통한 텍스트 생성"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 전문적인 문서 작성 보조 AI입니다. 논리적이고 체계적인 문서를 작성합니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("openai 패키지가 설치되지 않았습니다. pip install openai")
        except Exception as e:
            raise Exception(f"OpenAI API 호출 실패: {str(e)}")


def get_llm_provider(provider_type: str = "mock", **kwargs) -> LLMProvider:
    """
    LLM 제공자 팩토리 함수
    
    Args:
        provider_type: "mock" 또는 "openai"
        **kwargs: 제공자별 설정
    
    Returns:
        LLMProvider 인스턴스
    
    주의: 요금 방지를 위해 기본값은 항상 'mock'입니다.
    """
    # 안전장치: 요금 방지를 위해 항상 mock 사용
    # OpenAI를 사용하려면 명시적으로 provider_type='openai'를 전달하고
    # 환경 변수 OPENAI_API_KEY가 설정되어 있어야 합니다.
    
    # 환경 변수 확인: OPENAI_API_KEY가 없으면 강제로 mock 사용
    import os
    if provider_type == "openai" and not os.getenv("OPENAI_API_KEY"):
        print("경고: OPENAI_API_KEY가 설정되지 않았습니다. Mock Provider를 사용합니다.")
        return MockLLMProvider()
    
    if provider_type == "mock":
        return MockLLMProvider()
    elif provider_type == "openai":
        # 추가 안전장치: API 키 확인
        api_key = kwargs.get('api_key') or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("경고: OpenAI API 키가 없습니다. Mock Provider를 사용합니다.")
            return MockLLMProvider()
        return OpenAIProvider(**kwargs)
    else:
        # 알 수 없는 타입은 mock으로 폴백
        print(f"경고: 알 수 없는 provider_type '{provider_type}'. Mock Provider를 사용합니다.")
        return MockLLMProvider()
