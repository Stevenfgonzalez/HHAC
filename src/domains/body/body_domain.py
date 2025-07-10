"""
Body Domain Implementation

Specializes in physical health, movement, medical needs, pain management,
energy levels, physical comfort, movement patterns, and health metrics.
"""

from typing import Dict, Any, List
from datetime import datetime
from ..base_domain import (
    BaseDomain, DomainType, DomainResponse, DomainMetrics, 
    ConsensusLevel
)


class BodyDomain(BaseDomain):
    """
    Body Domain - Physical Health and Movement
    
    Focuses on:
    - Physical health and medical needs
    - Movement and exercise patterns
    - Pain management and physical comfort
    - Energy levels and physical fatigue
    - Posture and ergonomics
    - Physical recovery and healing
    """
    
    def __init__(self):
        super().__init__(DomainType.BODY)
        self.energy_threshold = 0.3
        self.pain_threshold = 0.6
        self.movement_threshold = 0.2
        
    def _initialize_domain(self) -> None:
        """Initialize body domain specific configurations"""
        self.physical_indicators = {
            "pain": ["pain", "ache", "sore", "hurt", "discomfort", "tension"],
            "fatigue": ["tired", "exhausted", "drained", "weak", "heavy"],
            "energy": ["energetic", "strong", "vital", "powerful", "active"],
            "movement": ["exercise", "workout", "walk", "run", "stretch", "move"],
            "posture": ["sit", "stand", "hunch", "slouch", "ergonomic"],
            "medical": ["sick", "ill", "injury", "symptom", "doctor", "medical"]
        }
        
        self.body_systems = {
            "musculoskeletal": ["muscle", "bone", "joint", "back", "neck", "shoulder"],
            "cardiovascular": ["heart", "blood", "circulation", "breath", "chest"],
            "digestive": ["stomach", "digest", "nausea", "appetite", "gut"],
            "nervous": ["nervous", "tremor", "numbness", "tingling", "headache"]
        }
    
    async def evaluate_input(self, user_input: str, context: Dict[str, Any]) -> DomainResponse:
        """Evaluate user input from physical health perspective"""
        input_lower = user_input.lower()
        
        # Analyze physical energy
        energy_level = self._assess_energy_level(input_lower, context)
        
        # Analyze pain indicators
        pain_level = self._assess_pain_level(input_lower, context)
        
        # Analyze movement needs
        movement_need = self._assess_movement_need(input_lower, context)
        
        # Analyze medical concerns
        medical_concern = self._assess_medical_concern(input_lower, context)
        
        # Generate recommendation
        recommendation = self._generate_body_recommendation(
            energy_level, pain_level, movement_need, medical_concern, context
        )
        
        # Determine consensus level
        consensus_level = self._determine_consensus_level(
            energy_level, pain_level, movement_need, medical_concern
        )
        
        # Generate alternatives
        alternatives = self._generate_alternatives(
            energy_level, pain_level, movement_need, medical_concern, context
        )
        
        # Check for safety concerns
        safety_concerns = self.get_safety_concerns(recommendation, context)
        
        # Calculate confidence
        confidence = self._calculate_confidence(energy_level, pain_level, movement_need, medical_concern)
        
        metrics = DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=confidence,
            urgency_level=max(energy_level, pain_level, movement_need, medical_concern),
            impact_score=0.7,  # Body domain has significant impact on overall wellbeing
            data_quality=0.9,
            timestamp=datetime.now(),
            metadata={
                "energy_level": energy_level,
                "pain_level": pain_level,
                "movement_need": movement_need,
                "medical_concern": medical_concern,
                "body_systems_affected": self._identify_affected_systems(input_lower)
            }
        )
        
        return DomainResponse(
            domain_type=self.domain_type,
            recommendation=recommendation,
            reasoning=self._generate_reasoning(energy_level, pain_level, movement_need, medical_concern),
            consensus_level=consensus_level,
            metrics=metrics,
            alternatives=alternatives,
            safety_concerns=safety_concerns,
            confidence=confidence,
            timestamp=datetime.now()
        )
    
    async def evaluate_recommendation(self, recommendation: str, context: Dict[str, Any]) -> ConsensusLevel:
        """Evaluate a recommendation from physical perspective"""
        rec_lower = recommendation.lower()
        
        # Check if recommendation addresses physical needs
        addresses_energy = any(word in rec_lower for word in ["rest", "sleep", "energy", "recovery"])
        addresses_pain = any(word in rec_lower for word in ["pain", "comfort", "relief", "stretch"])
        addresses_movement = any(word in rec_lower for word in ["move", "exercise", "walk", "stretch"])
        addresses_medical = any(word in rec_lower for word in ["doctor", "medical", "health", "symptom"])
        
        # Get current body state
        current_energy = context.get("energy_level", 0.5)
        current_pain = context.get("pain_level", 0.0)
        current_movement = context.get("movement_level", 0.5)
        
        # Evaluate alignment
        if addresses_energy and current_energy < 0.3:
            return ConsensusLevel.AGREEMENT
        elif addresses_pain and current_pain > 0.5:
            return ConsensusLevel.AGREEMENT
        elif addresses_movement and current_movement < 0.3:
            return ConsensusLevel.AGREEMENT
        elif addresses_medical and current_pain > 0.7:
            return ConsensusLevel.STRONG_AGREEMENT
        elif "work" in rec_lower and current_energy < 0.2:
            return ConsensusLevel.DISAGREEMENT
        else:
            return ConsensusLevel.NEUTRAL
    
    def get_domain_metrics(self, context: Dict[str, Any]) -> DomainMetrics:
        """Get current body domain metrics"""
        energy_level = context.get("energy_level", 0.5)
        pain_level = context.get("pain_level", 0.0)
        movement_level = context.get("movement_level", 0.5)
        
        return DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=0.8,
            urgency_level=max(1 - energy_level, pain_level, 1 - movement_level),
            impact_score=0.7,
            data_quality=0.9,
            timestamp=datetime.now(),
            metadata={
                "energy_level": energy_level,
                "pain_level": pain_level,
                "movement_level": movement_level
            }
        )
    
    def get_safety_concerns(self, recommendation: str, context: Dict[str, Any]) -> List[str]:
        """Identify safety concerns from physical perspective"""
        concerns = []
        rec_lower = recommendation.lower()
        
        # Check for severe pain that needs medical attention
        if context.get("pain_level", 0) > 0.8:
            concerns.append("Severe pain detected - may require medical attention")
        
        # Check for dangerous physical activities
        dangerous_activities = ["heavy lifting", "intense exercise", "strenuous activity"]
        if any(activity in rec_lower for activity in dangerous_activities):
            if context.get("energy_level", 0.5) < 0.3:
                concerns.append("Low energy level - strenuous activity may be dangerous")
            if context.get("pain_level", 0) > 0.5:
                concerns.append("Pain present - strenuous activity may cause injury")
        
        # Check for medical emergency indicators
        emergency_indicators = ["chest pain", "difficulty breathing", "severe injury", "bleeding"]
        if any(indicator in rec_lower for indicator in emergency_indicators):
            concerns.append("Potential medical emergency indicators detected")
        
        return concerns
    
    def _process_context_update(self, context: Dict[str, Any]) -> None:
        """Process context updates specific to body domain"""
        # Update internal state based on context changes
        pass
    
    def get_domain_description(self) -> str:
        """Get description of body domain focus"""
        return "Physical health, movement, medical needs, pain management, and energy levels"
    
    def _assess_energy_level(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess physical energy level from input and context"""
        energy_score = 0.5  # Base score
        
        # Check for fatigue indicators
        fatigue_count = sum(1 for word in self.physical_indicators["fatigue"] 
                           if word in input_text)
        energy_score -= fatigue_count * 0.15
        
        # Check for energy indicators
        energy_count = sum(1 for word in self.physical_indicators["energy"] 
                          if word in input_text)
        energy_score += energy_count * 0.1
        
        # Consider context
        if context.get("energy_level"):
            energy_score = (energy_score + context["energy_level"]) / 2
        
        return max(energy_score, 0.0)
    
    def _assess_pain_level(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess pain level from input and context"""
        pain_score = 0.0
        
        # Check for pain indicators
        pain_count = sum(1 for word in self.physical_indicators["pain"] 
                        if word in input_text)
        pain_score += pain_count * 0.2
        
        # Consider context
        if context.get("pain_level"):
            pain_score = (pain_score + context["pain_level"]) / 2
        
        return min(pain_score, 1.0)
    
    def _assess_movement_need(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess movement needs from input and context"""
        movement_score = 0.0
        
        # Check for movement indicators
        movement_count = sum(1 for word in self.physical_indicators["movement"] 
                            if word in input_text)
        movement_score += movement_count * 0.15
        
        # Check for posture indicators
        posture_count = sum(1 for word in self.physical_indicators["posture"] 
                           if word in input_text)
        movement_score += posture_count * 0.1
        
        # Consider context
        if context.get("movement_level"):
            movement_score = (movement_score + context["movement_level"]) / 2
        
        return min(movement_score, 1.0)
    
    def _assess_medical_concern(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess medical concerns from input and context"""
        medical_score = 0.0
        
        # Check for medical indicators
        medical_count = sum(1 for word in self.physical_indicators["medical"] 
                           if word in input_text)
        medical_score += medical_count * 0.25
        
        # Check for body system indicators
        for system, keywords in self.body_systems.items():
            system_count = sum(1 for word in keywords if word in input_text)
            medical_score += system_count * 0.1
        
        # Consider context
        if context.get("medical_concern"):
            medical_score = (medical_score + context["medical_concern"]) / 2
        
        return min(medical_score, 1.0)
    
    def _generate_body_recommendation(self, energy_level: float, pain_level: float,
                                    movement_need: float, medical_concern: float,
                                    context: Dict[str, Any]) -> str:
        """Generate body-focused recommendation"""
        if medical_concern > 0.7:
            return "Consider consulting a healthcare professional about your symptoms"
        elif pain_level > 0.6:
            return "Focus on pain management and physical comfort before continuing"
        elif energy_level < 0.3:
            return "Prioritize physical rest and recovery to restore energy"
        elif movement_need > 0.6:
            return "Consider gentle movement or stretching to improve physical comfort"
        else:
            return "Your physical state appears balanced for current activities"
    
    def _determine_consensus_level(self, energy_level: float, pain_level: float,
                                 movement_need: float, medical_concern: float) -> ConsensusLevel:
        """Determine consensus level based on body metrics"""
        max_metric = max(1 - energy_level, pain_level, movement_need, medical_concern)
        
        if max_metric > 0.8:
            return ConsensusLevel.STRONG_AGREEMENT
        elif max_metric > 0.6:
            return ConsensusLevel.AGREEMENT
        elif max_metric > 0.4:
            return ConsensusLevel.NEUTRAL
        else:
            return ConsensusLevel.NEUTRAL
    
    def _generate_alternatives(self, energy_level: float, pain_level: float,
                             movement_need: float, medical_concern: float,
                             context: Dict[str, Any]) -> List[str]:
        """Generate alternative recommendations"""
        alternatives = []
        
        if energy_level < 0.4:
            alternatives.append("Take a 10-minute rest break")
            alternatives.append("Hydrate and have a light snack")
        
        if pain_level > 0.5:
            alternatives.append("Try gentle stretching exercises")
            alternatives.append("Apply heat or cold therapy")
        
        if movement_need > 0.5:
            alternatives.append("Take a short walk")
            alternatives.append("Do some light stretching")
        
        if medical_concern > 0.6:
            alternatives.append("Monitor symptoms closely")
            alternatives.append("Consider telemedicine consultation")
        
        return alternatives
    
    def _generate_reasoning(self, energy_level: float, pain_level: float,
                          movement_need: float, medical_concern: float) -> str:
        """Generate reasoning for the recommendation"""
        reasons = []
        
        if energy_level < 0.4:
            reasons.append(f"Low energy level ({energy_level:.1%})")
        if pain_level > 0.5:
            reasons.append(f"Pain detected ({pain_level:.1%})")
        if movement_need > 0.5:
            reasons.append(f"Movement need identified ({movement_need:.1%})")
        if medical_concern > 0.6:
            reasons.append(f"Medical concern detected ({medical_concern:.1%})")
        
        if reasons:
            return f"Body domain analysis: {'; '.join(reasons)}"
        else:
            return "Body domain analysis: Physical state appears balanced"
    
    def _calculate_confidence(self, energy_level: float, pain_level: float,
                            movement_need: float, medical_concern: float) -> float:
        """Calculate confidence in the assessment"""
        # Higher confidence when indicators are clear
        indicator_count = sum([
            1 if energy_level < 0.4 else 0,
            1 if pain_level > 0.5 else 0,
            1 if movement_need > 0.5 else 0,
            1 if medical_concern > 0.6 else 0
        ])
        
        return min(0.5 + (indicator_count * 0.12), 1.0)
    
    def _identify_affected_systems(self, input_text: str) -> List[str]:
        """Identify which body systems are mentioned"""
        affected = []
        for system, keywords in self.body_systems.items():
            if any(word in input_text for word in keywords):
                affected.append(system)
        return affected 