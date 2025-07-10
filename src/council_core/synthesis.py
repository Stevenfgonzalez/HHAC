"""
Recommendation Synthesizer

Combines all domain responses into a final holistic recommendation.
Handles the synthesis of multiple perspectives into actionable advice.
"""

from typing import Dict, Any, List
from datetime import datetime

from ..domains.base_domain import DomainResponse
from .consensus import ConsensusResult


class RecommendationSynthesizer:
    """
    Recommendation Synthesizer - Holistic Integration
    
    Combines insights from all seven domains into a final recommendation
    that honors the complexity of human wellbeing while providing
    actionable guidance.
    """
    
    def __init__(self):
        """Initialize the synthesizer"""
        self.synthesis_templates = {
            "strong_agreement": self._synthesize_strong_agreement,
            "agreement": self._synthesize_agreement,
            "neutral": self._synthesize_neutral,
            "disagreement": self._synthesize_disagreement,
            "strong_disagreement": self._synthesize_strong_disagreement,
            "safety_block": self._synthesize_safety_block
        }
        
        self.domain_priorities = {
            "safety": 1,      # Highest priority
            "mind": 2,        # High priority
            "body": 3,        # High priority
            "purpose": 4,     # Medium-high priority
            "belong": 5,      # Medium priority
            "rest": 6,        # Medium priority
            "fuel": 7         # Medium priority
        }
    
    async def synthesize_recommendation(self, domain_responses: Dict[str, DomainResponse],
                                      consensus_result: ConsensusResult,
                                      context: Any) -> Any:
        """
        Synthesize a final recommendation from all domain responses.
        
        Args:
            domain_responses: Responses from all seven domains
            consensus_result: Result from consensus evaluation
            context: User context
            
        Returns:
            Synthesized recommendation
        """
        # Get the appropriate synthesis method
        synthesis_method = self.synthesis_templates.get(
            consensus_result.overall_consensus, 
            self._synthesize_neutral
        )
        
        # Synthesize the recommendation
        recommendation = await synthesis_method(domain_responses, consensus_result, context)
        
        return recommendation
    
    async def _synthesize_strong_agreement(self, domain_responses: Dict[str, DomainResponse],
                                         consensus_result: ConsensusResult,
                                         context: Any) -> Any:
        """Synthesize when there's strong agreement across domains"""
        # Find the strongest recommendations
        strong_recommendations = []
        for domain_name, response in domain_responses.items():
            if response.consensus_level.value in ["strong_agreement", "agreement"]:
                strong_recommendations.append((domain_name, response))
        
        # Sort by domain priority
        strong_recommendations.sort(key=lambda x: self.domain_priorities.get(x[0], 10))
        
        # Combine recommendations
        if len(strong_recommendations) >= 3:
            primary_rec = strong_recommendations[0][1].recommendation
            supporting_insights = [f"{name}: {resp.reasoning}" 
                                 for name, resp in strong_recommendations[1:3]]
            
            return {
                "recommendation": primary_rec,
                "reasoning": f"Strong council agreement. {'; '.join(supporting_insights)}",
                "alternatives": self._collect_alternatives(domain_responses),
                "consensus_level": "strong_agreement",
                "domain_insights": self._extract_domain_insights(domain_responses),
                "safety_concerns": self._collect_safety_concerns(domain_responses),
                "confidence": consensus_result.confidence,
                "timestamp": datetime.now()
            }
        else:
            return await self._synthesize_agreement(domain_responses, consensus_result, context)
    
    async def _synthesize_agreement(self, domain_responses: Dict[str, DomainResponse],
                                  consensus_result: ConsensusResult,
                                  context: Any) -> Any:
        """Synthesize when there's general agreement across domains"""
        # Find agreeing domains
        agreeing_domains = []
        for domain_name, response in domain_responses.items():
            if response.consensus_level.value in ["strong_agreement", "agreement"]:
                agreeing_domains.append((domain_name, response))
        
        # Sort by priority
        agreeing_domains.sort(key=lambda x: self.domain_priorities.get(x[0], 10))
        
        if agreeing_domains:
            primary_rec = agreeing_domains[0][1].recommendation
            supporting_insights = [f"{name}: {resp.reasoning}" 
                                 for name, resp in agreeing_domains[1:]]
            
            return {
                "recommendation": primary_rec,
                "reasoning": f"Council agreement. {'; '.join(supporting_insights)}",
                "alternatives": self._collect_alternatives(domain_responses),
                "consensus_level": "agreement",
                "domain_insights": self._extract_domain_insights(domain_responses),
                "safety_concerns": self._collect_safety_concerns(domain_responses),
                "confidence": consensus_result.confidence,
                "timestamp": datetime.now()
            }
        else:
            return await self._synthesize_neutral(domain_responses, consensus_result, context)
    
    async def _synthesize_neutral(self, domain_responses: Dict[str, DomainResponse],
                                consensus_result: ConsensusResult,
                                context: Any) -> Any:
        """Synthesize when domains are neutral or mixed"""
        # Find the most relevant recommendation
        relevant_domains = []
        for domain_name, response in domain_responses.items():
            if response.confidence > 0.6:  # Higher confidence domains
                relevant_domains.append((domain_name, response))
        
        # Sort by priority and confidence
        relevant_domains.sort(key=lambda x: (
            self.domain_priorities.get(x[0], 10), 
            -x[1].confidence
        ))
        
        if relevant_domains:
            primary_rec = relevant_domains[0][1].recommendation
            insights = [f"{name}: {resp.reasoning}" 
                       for name, resp in relevant_domains[:2]]
            
            return {
                "recommendation": primary_rec,
                "reasoning": f"Mixed council response. {'; '.join(insights)}",
                "alternatives": self._collect_alternatives(domain_responses),
                "consensus_level": "neutral",
                "domain_insights": self._extract_domain_insights(domain_responses),
                "safety_concerns": self._collect_safety_concerns(domain_responses),
                "confidence": consensus_result.confidence,
                "timestamp": datetime.now()
            }
        else:
            return {
                "recommendation": "Consider your current needs and choose what feels right for you",
                "reasoning": "Council domains are neutral - trust your judgment",
                "alternatives": self._collect_alternatives(domain_responses),
                "consensus_level": "neutral",
                "domain_insights": self._extract_domain_insights(domain_responses),
                "safety_concerns": self._collect_safety_concerns(domain_responses),
                "confidence": consensus_result.confidence,
                "timestamp": datetime.now()
            }
    
    async def _synthesize_disagreement(self, domain_responses: Dict[str, DomainResponse],
                                     consensus_result: ConsensusResult,
                                     context: Any) -> Any:
        """Synthesize when there's disagreement between domains"""
        # Present multiple perspectives
        perspectives = []
        for domain_name, response in domain_responses.items():
            if response.consensus_level.value in ["agreement", "strong_agreement"]:
                perspectives.append(f"{domain_name}: {response.recommendation}")
        
        if perspectives:
            return {
                "recommendation": f"Multiple perspectives: {'; '.join(perspectives[:2])}",
                "reasoning": "Council domains have different views - consider all perspectives",
                "alternatives": self._collect_alternatives(domain_responses),
                "consensus_level": "disagreement",
                "domain_insights": self._extract_domain_insights(domain_responses),
                "safety_concerns": self._collect_safety_concerns(domain_responses),
                "confidence": consensus_result.confidence,
                "timestamp": datetime.now()
            }
        else:
            return await self._synthesize_strong_disagreement(domain_responses, consensus_result, context)
    
    async def _synthesize_strong_disagreement(self, domain_responses: Dict[str, DomainResponse],
                                            consensus_result: ConsensusResult,
                                            context: Any) -> Any:
        """Synthesize when there's strong disagreement between domains"""
        return {
            "recommendation": "I'm seeing conflicting needs between your domains that I'm not equipped to balance. Here's what each domain is signaling...",
            "reasoning": "Strong disagreement detected - presenting all perspectives for your consideration",
            "alternatives": self._collect_alternatives(domain_responses),
            "consensus_level": "strong_disagreement",
            "domain_insights": self._extract_domain_insights(domain_responses),
            "safety_concerns": self._collect_safety_concerns(domain_responses),
            "confidence": consensus_result.confidence,
            "timestamp": datetime.now()
        }
    
    async def _synthesize_safety_block(self, domain_responses: Dict[str, DomainResponse],
                                     consensus_result: ConsensusResult,
                                     context: Any) -> Any:
        """Synthesize when safety domain has blocked the recommendation"""
        safety_response = domain_responses.get("safety")
        
        return {
            "recommendation": safety_response.recommendation if safety_response else "Safety concern detected",
            "reasoning": "SAFETY BLOCK: Safety domain has blocked this recommendation",
            "alternatives": safety_response.alternatives if safety_response else [],
            "consensus_level": "safety_block",
            "domain_insights": {"safety": safety_response.reasoning if safety_response else "Safety concern"},
            "safety_concerns": safety_response.safety_concerns if safety_response else ["Safety protocol triggered"],
            "confidence": safety_response.confidence if safety_response else 0.9,
            "timestamp": datetime.now()
        }
    
    def _collect_alternatives(self, domain_responses: Dict[str, DomainResponse]) -> List[str]:
        """Collect alternative recommendations from all domains"""
        alternatives = []
        for response in domain_responses.values():
            alternatives.extend(response.alternatives)
        
        # Remove duplicates and limit
        unique_alternatives = list(set(alternatives))
        return unique_alternatives[:5]  # Limit to 5 alternatives
    
    def _extract_domain_insights(self, domain_responses: Dict[str, DomainResponse]) -> Dict[str, str]:
        """Extract key insights from each domain"""
        insights = {}
        for domain_name, response in domain_responses.items():
            insights[domain_name] = response.reasoning
        
        return insights
    
    def _collect_safety_concerns(self, domain_responses: Dict[str, DomainResponse]) -> List[str]:
        """Collect safety concerns from all domains"""
        concerns = []
        for response in domain_responses.values():
            concerns.extend(response.safety_concerns)
        
        # Remove duplicates
        unique_concerns = list(set(concerns))
        return unique_concerns 