"""
Mind Domain Implementation

Specializes in cognitive health, learning, mental clarity, emotional processing,
decision-making patterns, stress management, and cognitive load assessment.
"""

import re
from typing import Dict, Any, List
from datetime import datetime
from ..base_domain import (
    BaseDomain, DomainType, DomainResponse, DomainMetrics, 
    ConsensusLevel
)


class MindDomain(BaseDomain):
    """
    Mind Domain - Cognitive and Emotional Processing
    
    Focuses on:
    - Cognitive health and mental clarity
    - Emotional processing and regulation
    - Learning patterns and knowledge acquisition
    - Decision-making processes
    - Stress management and cognitive load
    - Mental fatigue and burnout prevention
    """
    
    def __init__(self):
        super().__init__(DomainType.MIND)
        self.cognitive_load_threshold = 0.8
        self.stress_threshold = 0.7
        self.mental_fatigue_indicators = [
            "exhausted", "tired", "burnout", "overwhelmed", "stressed",
            "can't think", "brain fog", "mental fatigue", "drained"
        ]
        
    def _initialize_domain(self) -> None:
        """Initialize mind domain specific configurations"""
        self.emotional_keywords = {
            "stress": ["stressed", "anxious", "worried", "overwhelmed"],
            "fatigue": ["tired", "exhausted", "drained", "burnout"],
            "clarity": ["clear", "focused", "sharp", "alert"],
            "confusion": ["confused", "unclear", "foggy", "scattered"]
        }
        
        self.cognitive_indicators = {
            "high_load": ["complex", "difficult", "challenging", "complicated"],
            "low_load": ["simple", "easy", "straightforward", "basic"],
            "learning": ["learn", "study", "understand", "figure out"],
            "decision": ["decide", "choose", "determine", "figure out"]
        }
    
    async def evaluate_input(self, user_input: str, context: Dict[str, Any]) -> DomainResponse:
        """Evaluate user input from cognitive and emotional perspective"""
        input_lower = user_input.lower()
        
        # Analyze cognitive load
        cognitive_load = self._assess_cognitive_load(input_lower, context)
        
        # Analyze emotional state
        emotional_state = self._assess_emotional_state(input_lower, context)
        
        # Analyze mental fatigue
        fatigue_level = self._assess_mental_fatigue(input_lower, context)
        
        # Generate recommendation
        recommendation = self._generate_mind_recommendation(
            cognitive_load, emotional_state, fatigue_level, context
        )
        
        # Determine consensus level
        consensus_level = self._determine_consensus_level(
            cognitive_load, emotional_state, fatigue_level
        )
        
        # Generate alternatives
        alternatives = self._generate_alternatives(
            cognitive_load, emotional_state, fatigue_level, context
        )
        
        # Check for safety concerns
        safety_concerns = self.get_safety_concerns(recommendation, context)
        
        # Calculate confidence
        confidence = self._calculate_confidence(cognitive_load, emotional_state, fatigue_level)
        
        metrics = DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=confidence,
            urgency_level=max(cognitive_load, emotional_state, fatigue_level),
            impact_score=0.8,  # Mind domain has high impact on overall wellbeing
            data_quality=0.9,
            timestamp=datetime.now(),
            metadata={
                "cognitive_load": cognitive_load,
                "emotional_state": emotional_state,
                "fatigue_level": fatigue_level,
                "keywords_detected": self._extract_keywords(input_lower)
            }
        )
        
        return DomainResponse(
            domain_type=self.domain_type,
            recommendation=recommendation,
            reasoning=self._generate_reasoning(cognitive_load, emotional_state, fatigue_level),
            consensus_level=consensus_level,
            metrics=metrics,
            alternatives=alternatives,
            safety_concerns=safety_concerns,
            confidence=confidence,
            timestamp=datetime.now()
        )
    
    async def evaluate_recommendation(self, recommendation: str, context: Dict[str, Any]) -> ConsensusLevel:
        """Evaluate a recommendation from cognitive perspective"""
        rec_lower = recommendation.lower()
        
        # Check if recommendation addresses cognitive needs
        addresses_cognitive = any(word in rec_lower for word in ["think", "focus", "clarity", "mental"])
        addresses_emotional = any(word in rec_lower for word in ["stress", "calm", "relax", "emotional"])
        addresses_fatigue = any(word in rec_lower for word in ["rest", "break", "recovery", "sleep"])
        
        # Get current mind state
        current_load = context.get("cognitive_load", 0.5)
        current_stress = context.get("stress_level", 0.5)
        current_fatigue = context.get("mental_fatigue", 0.5)
        
        # Evaluate alignment
        if addresses_cognitive and current_load > 0.7:
            return ConsensusLevel.AGREEMENT
        elif addresses_emotional and current_stress > 0.6:
            return ConsensusLevel.AGREEMENT
        elif addresses_fatigue and current_fatigue > 0.6:
            return ConsensusLevel.AGREEMENT
        elif "work" in rec_lower and current_fatigue > 0.8:
            return ConsensusLevel.DISAGREEMENT
        else:
            return ConsensusLevel.NEUTRAL
    
    def get_domain_metrics(self, context: Dict[str, Any]) -> DomainMetrics:
        """Get current mind domain metrics"""
        cognitive_load = context.get("cognitive_load", 0.5)
        stress_level = context.get("stress_level", 0.5)
        mental_fatigue = context.get("mental_fatigue", 0.5)
        
        return DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=0.8,
            urgency_level=max(cognitive_load, stress_level, mental_fatigue),
            impact_score=0.8,
            data_quality=0.9,
            timestamp=datetime.now(),
            metadata={
                "cognitive_load": cognitive_load,
                "stress_level": stress_level,
                "mental_fatigue": mental_fatigue
            }
        )
    
    def get_safety_concerns(self, recommendation: str, context: Dict[str, Any]) -> List[str]:
        """Identify safety concerns from cognitive perspective"""
        concerns = []
        rec_lower = recommendation.lower()
        
        # Check for dangerous cognitive overload
        if context.get("cognitive_load", 0) > 0.9:
            concerns.append("Extreme cognitive overload detected")
        
        # Check for mental health crisis indicators
        crisis_indicators = ["harm myself", "suicide", "end it all", "can't go on"]
        if any(indicator in rec_lower for indicator in crisis_indicators):
            concerns.append("Potential mental health crisis indicators detected")
        
        # Check for burnout risk
        if context.get("mental_fatigue", 0) > 0.8 and "work" in rec_lower:
            concerns.append("High burnout risk - work recommendation may be harmful")
        
        return concerns
    
    def _process_context_update(self, context: Dict[str, Any]) -> None:
        """Process context updates specific to mind domain"""
        # Update internal state based on context changes
        pass
    
    def get_domain_description(self) -> str:
        """Get description of mind domain focus"""
        return "Cognitive health, emotional processing, mental clarity, learning, and decision-making patterns"
    
    def _assess_cognitive_load(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess cognitive load from input and context"""
        load_score = 0.5  # Base score
        
        # Check for high-load indicators
        high_load_count = sum(1 for word in self.cognitive_indicators["high_load"] 
                             if word in input_text)
        load_score += high_load_count * 0.1
        
        # Check for learning indicators
        learning_count = sum(1 for word in self.cognitive_indicators["learning"] 
                            if word in input_text)
        load_score += learning_count * 0.05
        
        # Consider context
        if context.get("cognitive_load"):
            load_score = (load_score + context["cognitive_load"]) / 2
        
        return min(load_score, 1.0)
    
    def _assess_emotional_state(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess emotional state from input and context"""
        stress_score = 0.0
        
        # Check for stress indicators
        stress_count = sum(1 for word in self.emotional_keywords["stress"] 
                          if word in input_text)
        stress_score += stress_count * 0.2
        
        # Check for fatigue indicators
        fatigue_count = sum(1 for word in self.emotional_keywords["fatigue"] 
                           if word in input_text)
        stress_score += fatigue_count * 0.15
        
        # Consider context
        if context.get("stress_level"):
            stress_score = (stress_score + context["stress_level"]) / 2
        
        return min(stress_score, 1.0)
    
    def _assess_mental_fatigue(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess mental fatigue from input and context"""
        fatigue_score = 0.0
        
        # Check for fatigue indicators
        for indicator in self.mental_fatigue_indicators:
            if indicator in input_text:
                fatigue_score += 0.2
        
        # Consider context
        if context.get("mental_fatigue"):
            fatigue_score = (fatigue_score + context["mental_fatigue"]) / 2
        
        return min(fatigue_score, 1.0)
    
    def _generate_mind_recommendation(self, cognitive_load: float, emotional_state: float, 
                                    fatigue_level: float, context: Dict[str, Any]) -> str:
        """Generate mind-focused recommendation"""
        if fatigue_level > 0.7:
            return "Consider taking a mental break to restore cognitive clarity"
        elif emotional_state > 0.6:
            return "Focus on stress management techniques before continuing"
        elif cognitive_load > 0.8:
            return "Break down complex tasks into smaller, manageable steps"
        else:
            return "Your cognitive state appears balanced for current activities"
    
    def _determine_consensus_level(self, cognitive_load: float, emotional_state: float, 
                                 fatigue_level: float) -> ConsensusLevel:
        """Determine consensus level based on mind metrics"""
        max_metric = max(cognitive_load, emotional_state, fatigue_level)
        
        if max_metric > 0.8:
            return ConsensusLevel.STRONG_AGREEMENT
        elif max_metric > 0.6:
            return ConsensusLevel.AGREEMENT
        elif max_metric > 0.4:
            return ConsensusLevel.NEUTRAL
        else:
            return ConsensusLevel.NEUTRAL
    
    def _generate_alternatives(self, cognitive_load: float, emotional_state: float,
                             fatigue_level: float, context: Dict[str, Any]) -> List[str]:
        """Generate alternative recommendations"""
        alternatives = []
        
        if fatigue_level > 0.6:
            alternatives.append("Take a 15-minute meditation break")
            alternatives.append("Switch to a less demanding task temporarily")
        
        if emotional_state > 0.5:
            alternatives.append("Practice deep breathing exercises")
            alternatives.append("Step away for a brief walk")
        
        if cognitive_load > 0.7:
            alternatives.append("Create a prioritized task list")
            alternatives.append("Ask for help or collaboration")
        
        return alternatives
    
    def _generate_reasoning(self, cognitive_load: float, emotional_state: float,
                          fatigue_level: float) -> str:
        """Generate reasoning for the recommendation"""
        reasons = []
        
        if fatigue_level > 0.6:
            reasons.append(f"Mental fatigue detected ({fatigue_level:.1%})")
        if emotional_state > 0.5:
            reasons.append(f"Elevated stress levels ({emotional_state:.1%})")
        if cognitive_load > 0.7:
            reasons.append(f"High cognitive load ({cognitive_load:.1%})")
        
        if reasons:
            return f"Mind domain analysis: {'; '.join(reasons)}"
        else:
            return "Mind domain analysis: Cognitive state appears balanced"
    
    def _calculate_confidence(self, cognitive_load: float, emotional_state: float,
                            fatigue_level: float) -> float:
        """Calculate confidence in the assessment"""
        # Higher confidence when indicators are clear
        indicator_count = sum([
            1 if cognitive_load > 0.6 else 0,
            1 if emotional_state > 0.5 else 0,
            1 if fatigue_level > 0.6 else 0
        ])
        
        return min(0.5 + (indicator_count * 0.15), 1.0)
    
    def _extract_keywords(self, input_text: str) -> List[str]:
        """Extract relevant keywords from input"""
        keywords = []
        for category, words in self.emotional_keywords.items():
            for word in words:
                if word in input_text:
                    keywords.append(word)
        
        for category, words in self.cognitive_indicators.items():
            for word in words:
                if word in input_text:
                    keywords.append(word)
        
        return keywords 