"""
Safety Domain Implementation

Specializes in physical/emotional security, stability, boundaries,
risk assessment, security needs, and boundary maintenance.
This domain has special privileges and can block recommendations.
"""

from typing import Dict, Any, List
from datetime import datetime
from ..base_domain import (
    BaseDomain, DomainType, DomainResponse, DomainMetrics, 
    ConsensusLevel
)


class SafetyDomain(BaseDomain):
    """
    Safety Domain - Security and Boundaries (Protected Class)
    
    Focuses on:
    - Physical and emotional security
    - Risk assessment and harm prevention
    - Boundary maintenance and respect
    - Stability and safety protocols
    - Emergency response and crisis management
    - Protection from exploitation or harm
    
    This domain has special privileges and can block recommendations
    that compromise safety protocols without explicit user override.
    """
    
    def __init__(self):
        super().__init__(DomainType.SAFETY)
        self.risk_threshold = 0.6
        self.crisis_threshold = 0.8
        self.boundary_threshold = 0.5
        
    def _initialize_domain(self) -> None:
        """Initialize safety domain specific configurations"""
        self.safety_indicators = {
            "physical_threat": ["hurt", "harm", "danger", "attack", "violence", "abuse"],
            "emotional_threat": ["manipulate", "control", "pressure", "coerce", "threaten"],
            "crisis": ["suicide", "self-harm", "emergency", "crisis", "desperate"],
            "boundary_violation": ["push", "force", "insist", "demand", "pressure"],
            "exploitation": ["exploit", "use", "manipulate", "take advantage", "trick"],
            "instability": ["unstable", "volatile", "dangerous", "risky", "unsafe"]
        }
        
        self.protection_patterns = {
            "self_harm": ["kill myself", "end it all", "don't want to live", "better off dead"],
            "harm_others": ["hurt them", "attack", "revenge", "get back at"],
            "substance_abuse": ["drink too much", "drugs", "overdose", "substance"],
            "financial_risk": ["gamble", "loan", "debt", "financial risk"],
            "relationship_danger": ["abusive", "controlling", "manipulative partner"]
        }
        
        # Safety protocols that cannot be overridden without explicit consent
        self.protected_protocols = [
            "self_harm_prevention",
            "crisis_intervention", 
            "boundary_protection",
            "exploitation_prevention",
            "emergency_response"
        ]
    
    async def evaluate_input(self, user_input: str, context: Dict[str, Any]) -> DomainResponse:
        """Evaluate user input from safety and security perspective"""
        input_lower = user_input.lower()
        
        # Analyze risk level
        risk_level = self._assess_risk_level(input_lower, context)
        
        # Analyze crisis indicators
        crisis_level = self._assess_crisis_level(input_lower, context)
        
        # Analyze boundary concerns
        boundary_concern = self._assess_boundary_concern(input_lower, context)
        
        # Analyze stability
        stability_level = self._assess_stability_level(input_lower, context)
        
        # Generate recommendation
        recommendation = self._generate_safety_recommendation(
            risk_level, crisis_level, boundary_concern, stability_level, context
        )
        
        # Determine consensus level (Safety can block)
        consensus_level = self._determine_consensus_level(
            risk_level, crisis_level, boundary_concern, stability_level
        )
        
        # Generate alternatives
        alternatives = self._generate_alternatives(
            risk_level, crisis_level, boundary_concern, stability_level, context
        )
        
        # Check for safety concerns (critical for this domain)
        safety_concerns = self.get_safety_concerns(recommendation, context)
        
        # Calculate confidence
        confidence = self._calculate_confidence(risk_level, crisis_level, boundary_concern, stability_level)
        
        metrics = DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=confidence,
            urgency_level=max(risk_level, crisis_level, boundary_concern, 1 - stability_level),
            impact_score=1.0,  # Safety domain has maximum impact - can block everything
            data_quality=0.95,
            timestamp=datetime.now(),
            metadata={
                "risk_level": risk_level,
                "crisis_level": crisis_level,
                "boundary_concern": boundary_concern,
                "stability_level": stability_level,
                "protection_patterns_detected": self._detect_protection_patterns(input_lower)
            }
        )
        
        return DomainResponse(
            domain_type=self.domain_type,
            recommendation=recommendation,
            reasoning=self._generate_reasoning(risk_level, crisis_level, boundary_concern, stability_level),
            consensus_level=consensus_level,
            metrics=metrics,
            alternatives=alternatives,
            safety_concerns=safety_concerns,
            confidence=confidence,
            timestamp=datetime.now()
        )
    
    async def evaluate_recommendation(self, recommendation: str, context: Dict[str, Any]) -> ConsensusLevel:
        """Evaluate a recommendation from safety perspective (can block)"""
        rec_lower = recommendation.lower()
        
        # Check for safety violations
        if self._has_safety_violation(rec_lower, context):
            return ConsensusLevel.SAFETY_BLOCK
        
        # Check if recommendation addresses safety needs
        addresses_risk = any(word in rec_lower for word in ["safe", "secure", "protect", "risk"])
        addresses_crisis = any(word in rec_lower for word in ["crisis", "emergency", "help", "support"])
        addresses_boundary = any(word in rec_lower for word in ["boundary", "respect", "consent", "choice"])
        
        # Get current safety state
        current_risk = context.get("risk_level", 0.0)
        current_crisis = context.get("crisis_level", 0.0)
        current_boundary = context.get("boundary_concern", 0.0)
        
        # Evaluate alignment
        if addresses_crisis and current_crisis > 0.6:
            return ConsensusLevel.STRONG_AGREEMENT
        elif addresses_risk and current_risk > 0.5:
            return ConsensusLevel.AGREEMENT
        elif addresses_boundary and current_boundary > 0.4:
            return ConsensusLevel.AGREEMENT
        elif self._increases_risk(rec_lower, context):
            return ConsensusLevel.STRONG_DISAGREEMENT
        else:
            return ConsensusLevel.NEUTRAL
    
    def get_domain_metrics(self, context: Dict[str, Any]) -> DomainMetrics:
        """Get current safety domain metrics"""
        risk_level = context.get("risk_level", 0.0)
        crisis_level = context.get("crisis_level", 0.0)
        boundary_concern = context.get("boundary_concern", 0.0)
        stability_level = context.get("stability_level", 1.0)
        
        return DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=0.9,
            urgency_level=max(risk_level, crisis_level, boundary_concern, 1 - stability_level),
            impact_score=1.0,
            data_quality=0.95,
            timestamp=datetime.now(),
            metadata={
                "risk_level": risk_level,
                "crisis_level": crisis_level,
                "boundary_concern": boundary_concern,
                "stability_level": stability_level
            }
        )
    
    def get_safety_concerns(self, recommendation: str, context: Dict[str, Any]) -> List[str]:
        """Identify safety concerns (critical for this domain)"""
        concerns = []
        rec_lower = recommendation.lower()
        
        # Check for crisis indicators
        if context.get("crisis_level", 0) > 0.7:
            concerns.append("CRISIS: Immediate intervention may be required")
        
        # Check for self-harm risk
        if context.get("self_harm_risk", 0) > 0.6:
            concerns.append("SELF-HARM RISK: Professional mental health support needed")
        
        # Check for harm to others
        if context.get("harm_others_risk", 0) > 0.6:
            concerns.append("HARM TO OTHERS RISK: Safety intervention required")
        
        # Check for exploitation risk
        if context.get("exploitation_risk", 0) > 0.7:
            concerns.append("EXPLOITATION RISK: Recommendation may enable harm")
        
        # Check for boundary violations
        if context.get("boundary_violation", 0) > 0.5:
            concerns.append("BOUNDARY VIOLATION: Recommendation may disrespect autonomy")
        
        # Check for dangerous activities
        dangerous_activities = ["driving while impaired", "substance abuse", "reckless behavior"]
        if any(activity in rec_lower for activity in dangerous_activities):
            concerns.append("DANGEROUS ACTIVITY: Recommendation may cause harm")
        
        return concerns
    
    def _process_context_update(self, context: Dict[str, Any]) -> None:
        """Process context updates specific to safety domain"""
        # Update internal safety state based on context changes
        pass
    
    def get_domain_description(self) -> str:
        """Get description of safety domain focus"""
        return "Physical/emotional security, risk assessment, boundary protection, and harm prevention (Protected Class)"
    
    def _assess_risk_level(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess overall risk level from input and context"""
        risk_score = 0.0
        
        # Check for physical threats
        physical_count = sum(1 for word in self.safety_indicators["physical_threat"] 
                            if word in input_text)
        risk_score += physical_count * 0.2
        
        # Check for emotional threats
        emotional_count = sum(1 for word in self.safety_indicators["emotional_threat"] 
                             if word in input_text)
        risk_score += emotional_count * 0.15
        
        # Check for exploitation
        exploitation_count = sum(1 for word in self.safety_indicators["exploitation"] 
                                if word in input_text)
        risk_score += exploitation_count * 0.25
        
        # Check for instability
        instability_count = sum(1 for word in self.safety_indicators["instability"] 
                               if word in input_text)
        risk_score += instability_count * 0.2
        
        # Consider context
        if context.get("risk_level"):
            risk_score = (risk_score + context["risk_level"]) / 2
        
        return min(risk_score, 1.0)
    
    def _assess_crisis_level(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess crisis level from input and context"""
        crisis_score = 0.0
        
        # Check for crisis indicators
        crisis_count = sum(1 for word in self.safety_indicators["crisis"] 
                          if word in input_text)
        crisis_score += crisis_count * 0.3
        
        # Check for protection patterns
        for pattern, keywords in self.protection_patterns.items():
            pattern_count = sum(1 for word in keywords if word in input_text)
            crisis_score += pattern_count * 0.25
        
        # Consider context
        if context.get("crisis_level"):
            crisis_score = (crisis_score + context["crisis_level"]) / 2
        
        return min(crisis_score, 1.0)
    
    def _assess_boundary_concern(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess boundary concerns from input and context"""
        boundary_score = 0.0
        
        # Check for boundary violations
        boundary_count = sum(1 for word in self.safety_indicators["boundary_violation"] 
                            if word in input_text)
        boundary_score += boundary_count * 0.2
        
        # Consider context
        if context.get("boundary_concern"):
            boundary_score = (boundary_score + context["boundary_concern"]) / 2
        
        return min(boundary_score, 1.0)
    
    def _assess_stability_level(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess stability level from input and context"""
        stability_score = 1.0  # Start with full stability
        
        # Check for instability indicators
        instability_count = sum(1 for word in self.safety_indicators["instability"] 
                               if word in input_text)
        stability_score -= instability_count * 0.15
        
        # Consider context
        if context.get("stability_level"):
            stability_score = (stability_score + context["stability_level"]) / 2
        
        return max(stability_score, 0.0)
    
    def _generate_safety_recommendation(self, risk_level: float, crisis_level: float,
                                      boundary_concern: float, stability_level: float,
                                      context: Dict[str, Any]) -> str:
        """Generate safety-focused recommendation"""
        if crisis_level > 0.8:
            return "CRISIS: Please contact emergency services or a crisis hotline immediately"
        elif crisis_level > 0.6:
            return "Consider reaching out to a mental health professional or crisis support"
        elif risk_level > 0.7:
            return "Focus on safety first - avoid any activities that could cause harm"
        elif boundary_concern > 0.6:
            return "Respect your boundaries and don't feel pressured to do anything unsafe"
        elif stability_level < 0.4:
            return "Prioritize creating a safe, stable environment before making decisions"
        else:
            return "Your safety appears secure for current activities"
    
    def _determine_consensus_level(self, risk_level: float, crisis_level: float,
                                 boundary_concern: float, stability_level: float) -> ConsensusLevel:
        """Determine consensus level based on safety metrics"""
        max_metric = max(risk_level, crisis_level, boundary_concern, 1 - stability_level)
        
        if crisis_level > 0.7:
            return ConsensusLevel.SAFETY_BLOCK
        elif max_metric > 0.8:
            return ConsensusLevel.STRONG_AGREEMENT
        elif max_metric > 0.6:
            return ConsensusLevel.AGREEMENT
        elif max_metric > 0.4:
            return ConsensusLevel.NEUTRAL
        else:
            return ConsensusLevel.NEUTRAL
    
    def _generate_alternatives(self, risk_level: float, crisis_level: float,
                             boundary_concern: float, stability_level: float,
                             context: Dict[str, Any]) -> List[str]:
        """Generate alternative safety recommendations"""
        alternatives = []
        
        if crisis_level > 0.6:
            alternatives.append("Contact National Suicide Prevention Lifeline: 988")
            alternatives.append("Reach out to a trusted friend or family member")
        
        if risk_level > 0.6:
            alternatives.append("Remove yourself from potentially dangerous situations")
            alternatives.append("Create a safety plan with trusted individuals")
        
        if boundary_concern > 0.5:
            alternatives.append("Practice saying 'no' to requests that feel unsafe")
            alternatives.append("Set clear boundaries with others")
        
        if stability_level < 0.5:
            alternatives.append("Focus on creating a safe, predictable routine")
            alternatives.append("Avoid major life changes until stability improves")
        
        return alternatives
    
    def _generate_reasoning(self, risk_level: float, crisis_level: float,
                          boundary_concern: float, stability_level: float) -> str:
        """Generate reasoning for the recommendation"""
        reasons = []
        
        if crisis_level > 0.6:
            reasons.append(f"CRISIS DETECTED ({crisis_level:.1%})")
        if risk_level > 0.6:
            reasons.append(f"Safety risk identified ({risk_level:.1%})")
        if boundary_concern > 0.5:
            reasons.append(f"Boundary concern detected ({boundary_concern:.1%})")
        if stability_level < 0.5:
            reasons.append(f"Instability detected ({stability_level:.1%})")
        
        if reasons:
            return f"SAFETY ALERT: {'; '.join(reasons)}"
        else:
            return "Safety domain analysis: No immediate safety concerns detected"
    
    def _calculate_confidence(self, risk_level: float, crisis_level: float,
                            boundary_concern: float, stability_level: float) -> float:
        """Calculate confidence in the safety assessment"""
        # Higher confidence when safety indicators are clear
        indicator_count = sum([
            1 if crisis_level > 0.6 else 0,
            1 if risk_level > 0.6 else 0,
            1 if boundary_concern > 0.5 else 0,
            1 if stability_level < 0.5 else 0
        ])
        
        return min(0.6 + (indicator_count * 0.1), 1.0)
    
    def _detect_protection_patterns(self, input_text: str) -> List[str]:
        """Detect protection patterns in input"""
        detected = []
        for pattern, keywords in self.protection_patterns.items():
            if any(word in input_text for word in keywords):
                detected.append(pattern)
        return detected
    
    def _has_safety_violation(self, recommendation: str, context: Dict[str, Any]) -> bool:
        """Check if recommendation violates safety protocols"""
        rec_lower = recommendation.lower()
        
        # Check for crisis indicators
        if context.get("crisis_level", 0) > 0.7:
            return True
        
        # Check for dangerous recommendations
        dangerous_keywords = ["ignore safety", "take risk", "dangerous", "harmful"]
        if any(word in rec_lower for word in dangerous_keywords):
            return True
        
        return False
    
    def _increases_risk(self, recommendation: str, context: Dict[str, Any]) -> bool:
        """Check if recommendation increases risk"""
        rec_lower = recommendation.lower()
        
        risk_increasing_keywords = ["ignore", "risk", "dangerous", "harmful", "unsafe"]
        return any(word in rec_lower for word in risk_increasing_keywords) 