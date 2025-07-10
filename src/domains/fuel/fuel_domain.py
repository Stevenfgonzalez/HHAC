"""
Fuel Domain Implementation

Specializes in nutrition, resources, energy inputs, sustainable consumption,
dietary patterns, resource availability, and energy optimization.
"""

from typing import Dict, Any, List
from datetime import datetime
from ..base_domain import (
    BaseDomain, DomainType, DomainResponse, DomainMetrics, 
    ConsensusLevel
)


class FuelDomain(BaseDomain):
    """
    Fuel Domain - Nutrition and Resources
    
    Focuses on:
    - Nutrition and dietary needs
    - Resource availability and management
    - Energy inputs and optimization
    - Sustainable consumption patterns
    - Hydration and fueling strategies
    - Resource planning and allocation
    """
    
    def __init__(self):
        super().__init__(DomainType.FUEL)
        self.nutrition_threshold = 0.6
        self.resource_threshold = 0.5
        self.hydration_threshold = 0.7
        
    def _initialize_domain(self) -> None:
        """Initialize fuel domain specific configurations"""
        self.nutrition_indicators = {
            "hunger": ["hungry", "starving", "appetite", "food", "eat"],
            "nutrition": ["protein", "vitamins", "nutrients", "healthy", "balanced"],
            "energy_food": ["energy", "fuel", "sustaining", "nourishing"],
            "dehydration": ["thirsty", "dehydrated", "water", "drink", "hydrate"],
            "cravings": ["crave", "want", "need", "desire", "taste"]
        }
        
        self.resource_indicators = {
            "financial": ["money", "cost", "budget", "expensive", "afford"],
            "time": ["time", "schedule", "busy", "rushed", "deadline"],
            "energy": ["energy", "tired", "drained", "exhausted", "fatigue"],
            "materials": ["supplies", "materials", "resources", "equipment", "tools"]
        }
    
    async def evaluate_input(self, user_input: str, context: Dict[str, Any]) -> DomainResponse:
        """Evaluate user input from nutrition and resource perspective"""
        input_lower = user_input.lower()
        
        # Analyze nutrition needs
        nutrition_need = self._assess_nutrition_need(input_lower, context)
        
        # Analyze resource availability
        resource_availability = self._assess_resource_availability(input_lower, context)
        
        # Analyze hydration needs
        hydration_need = self._assess_hydration_need(input_lower, context)
        
        # Analyze energy optimization
        energy_optimization = self._assess_energy_optimization(input_lower, context)
        
        # Generate recommendation
        recommendation = self._generate_fuel_recommendation(
            nutrition_need, resource_availability, hydration_need, energy_optimization, context
        )
        
        # Determine consensus level
        consensus_level = self._determine_consensus_level(
            nutrition_need, resource_availability, hydration_need, energy_optimization
        )
        
        # Generate alternatives
        alternatives = self._generate_alternatives(
            nutrition_need, resource_availability, hydration_need, energy_optimization, context
        )
        
        # Check for safety concerns
        safety_concerns = self.get_safety_concerns(recommendation, context)
        
        # Calculate confidence
        confidence = self._calculate_confidence(nutrition_need, resource_availability, hydration_need, energy_optimization)
        
        metrics = DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=confidence,
            urgency_level=max(nutrition_need, resource_availability, hydration_need, energy_optimization),
            impact_score=0.6,  # Fuel domain has moderate impact on overall wellbeing
            data_quality=0.9,
            timestamp=datetime.now(),
            metadata={
                "nutrition_need": nutrition_need,
                "resource_availability": resource_availability,
                "hydration_need": hydration_need,
                "energy_optimization": energy_optimization,
                "fuel_indicators_detected": self._extract_fuel_indicators(input_lower)
            }
        )
        
        return DomainResponse(
            domain_type=self.domain_type,
            recommendation=recommendation,
            reasoning=self._generate_reasoning(nutrition_need, resource_availability, hydration_need, energy_optimization),
            consensus_level=consensus_level,
            metrics=metrics,
            alternatives=alternatives,
            safety_concerns=safety_concerns,
            confidence=confidence,
            timestamp=datetime.now()
        )
    
    async def evaluate_recommendation(self, recommendation: str, context: Dict[str, Any]) -> ConsensusLevel:
        """Evaluate a recommendation from fuel perspective"""
        rec_lower = recommendation.lower()
        
        # Check if recommendation addresses fuel needs
        addresses_nutrition = any(word in rec_lower for word in ["eat", "food", "nutrition", "meal"])
        addresses_hydration = any(word in rec_lower for word in ["drink", "water", "hydrate", "fluid"])
        addresses_resources = any(word in rec_lower for word in ["resource", "budget", "time", "energy"])
        
        # Get current fuel state
        current_nutrition = context.get("nutrition_need", 0.5)
        current_hydration = context.get("hydration_need", 0.5)
        current_resources = context.get("resource_availability", 0.5)
        
        # Evaluate alignment
        if addresses_nutrition and current_nutrition > 0.6:
            return ConsensusLevel.AGREEMENT
        elif addresses_hydration and current_hydration > 0.7:
            return ConsensusLevel.AGREEMENT
        elif addresses_resources and current_resources < 0.4:
            return ConsensusLevel.AGREEMENT
        else:
            return ConsensusLevel.NEUTRAL
    
    def get_domain_metrics(self, context: Dict[str, Any]) -> DomainMetrics:
        """Get current fuel domain metrics"""
        nutrition_need = context.get("nutrition_need", 0.5)
        hydration_need = context.get("hydration_need", 0.5)
        resource_availability = context.get("resource_availability", 0.5)
        
        return DomainMetrics(
            domain_type=self.domain_type,
            confidence_score=0.8,
            urgency_level=max(nutrition_need, hydration_need, 1 - resource_availability),
            impact_score=0.6,
            data_quality=0.9,
            timestamp=datetime.now(),
            metadata={
                "nutrition_need": nutrition_need,
                "hydration_need": hydration_need,
                "resource_availability": resource_availability
            }
        )
    
    def get_safety_concerns(self, recommendation: str, context: Dict[str, Any]) -> List[str]:
        """Identify safety concerns from fuel perspective"""
        concerns = []
        rec_lower = recommendation.lower()
        
        # Check for extreme dietary recommendations
        extreme_diet_keywords = ["fast", "starve", "extreme diet", "no food"]
        if any(word in rec_lower for word in extreme_diet_keywords):
            concerns.append("Extreme dietary restriction may be harmful")
        
        # Check for resource depletion
        if context.get("resource_availability", 0.5) < 0.2:
            concerns.append("Very low resource availability - may cause stress")
        
        return concerns
    
    def _process_context_update(self, context: Dict[str, Any]) -> None:
        """Process context updates specific to fuel domain"""
        pass
    
    def get_domain_description(self) -> str:
        """Get description of fuel domain focus"""
        return "Nutrition, resources, energy inputs, and sustainable consumption patterns"
    
    def _assess_nutrition_need(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess nutrition needs from input and context"""
        nutrition_score = 0.0
        
        # Check for hunger indicators
        hunger_count = sum(1 for word in self.nutrition_indicators["hunger"] 
                          if word in input_text)
        nutrition_score += hunger_count * 0.2
        
        # Check for nutrition indicators
        nutrition_count = sum(1 for word in self.nutrition_indicators["nutrition"] 
                             if word in input_text)
        nutrition_score += nutrition_count * 0.15
        
        # Consider context
        if context.get("nutrition_need"):
            nutrition_score = (nutrition_score + context["nutrition_need"]) / 2
        
        return min(nutrition_score, 1.0)
    
    def _assess_resource_availability(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess resource availability from input and context"""
        resource_score = 0.5  # Base score
        
        # Check for resource constraints
        for resource_type, keywords in self.resource_indicators.items():
            constraint_count = sum(1 for word in keywords if word in input_text)
            resource_score -= constraint_count * 0.1
        
        # Consider context
        if context.get("resource_availability"):
            resource_score = (resource_score + context["resource_availability"]) / 2
        
        return max(resource_score, 0.0)
    
    def _assess_hydration_need(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess hydration needs from input and context"""
        hydration_score = 0.0
        
        # Check for dehydration indicators
        dehydration_count = sum(1 for word in self.nutrition_indicators["dehydration"] 
                               if word in input_text)
        hydration_score += dehydration_count * 0.25
        
        # Consider context
        if context.get("hydration_need"):
            hydration_score = (hydration_score + context["hydration_need"]) / 2
        
        return min(hydration_score, 1.0)
    
    def _assess_energy_optimization(self, input_text: str, context: Dict[str, Any]) -> float:
        """Assess energy optimization needs from input and context"""
        energy_score = 0.0
        
        # Check for energy food indicators
        energy_count = sum(1 for word in self.nutrition_indicators["energy_food"] 
                          if word in input_text)
        energy_score += energy_count * 0.15
        
        # Consider context
        if context.get("energy_optimization"):
            energy_score = (energy_score + context["energy_optimization"]) / 2
        
        return min(energy_score, 1.0)
    
    def _generate_fuel_recommendation(self, nutrition_need: float, resource_availability: float,
                                    hydration_need: float, energy_optimization: float,
                                    context: Dict[str, Any]) -> str:
        """Generate fuel-focused recommendation"""
        if hydration_need > 0.7:
            return "Prioritize hydration - drink water or electrolyte-rich fluids"
        elif nutrition_need > 0.6:
            return "Consider having a balanced meal or nutritious snack"
        elif resource_availability < 0.3:
            return "Focus on resource conservation and efficient use of available resources"
        elif energy_optimization > 0.5:
            return "Consider energy-rich foods to support your current activities"
        else:
            return "Your fuel and resource needs appear balanced"
    
    def _determine_consensus_level(self, nutrition_need: float, resource_availability: float,
                                 hydration_need: float, energy_optimization: float) -> ConsensusLevel:
        """Determine consensus level based on fuel metrics"""
        max_metric = max(nutrition_need, hydration_need, energy_optimization, 1 - resource_availability)
        
        if max_metric > 0.8:
            return ConsensusLevel.STRONG_AGREEMENT
        elif max_metric > 0.6:
            return ConsensusLevel.AGREEMENT
        elif max_metric > 0.4:
            return ConsensusLevel.NEUTRAL
        else:
            return ConsensusLevel.NEUTRAL
    
    def _generate_alternatives(self, nutrition_need: float, resource_availability: float,
                             hydration_need: float, energy_optimization: float,
                             context: Dict[str, Any]) -> List[str]:
        """Generate alternative recommendations"""
        alternatives = []
        
        if hydration_need > 0.6:
            alternatives.append("Have a glass of water")
            alternatives.append("Try herbal tea or electrolyte drink")
        
        if nutrition_need > 0.5:
            alternatives.append("Have a protein-rich snack")
            alternatives.append("Consider a balanced meal")
        
        if resource_availability < 0.4:
            alternatives.append("Prioritize essential resource use")
            alternatives.append("Look for cost-effective alternatives")
        
        if energy_optimization > 0.5:
            alternatives.append("Include complex carbohydrates in your meal")
            alternatives.append("Consider energy-boosting foods")
        
        return alternatives
    
    def _generate_reasoning(self, nutrition_need: float, resource_availability: float,
                          hydration_need: float, energy_optimization: float) -> str:
        """Generate reasoning for the recommendation"""
        reasons = []
        
        if hydration_need > 0.6:
            reasons.append(f"Hydration need detected ({hydration_need:.1%})")
        if nutrition_need > 0.5:
            reasons.append(f"Nutrition need identified ({nutrition_need:.1%})")
        if resource_availability < 0.4:
            reasons.append(f"Resource constraint detected ({resource_availability:.1%})")
        if energy_optimization > 0.5:
            reasons.append(f"Energy optimization needed ({energy_optimization:.1%})")
        
        if reasons:
            return f"Fuel domain analysis: {'; '.join(reasons)}"
        else:
            return "Fuel domain analysis: Fuel and resource needs appear balanced"
    
    def _calculate_confidence(self, nutrition_need: float, resource_availability: float,
                            hydration_need: float, energy_optimization: float) -> float:
        """Calculate confidence in the assessment"""
        indicator_count = sum([
            1 if nutrition_need > 0.5 else 0,
            1 if hydration_need > 0.6 else 0,
            1 if resource_availability < 0.4 else 0,
            1 if energy_optimization > 0.5 else 0
        ])
        
        return min(0.5 + (indicator_count * 0.12), 1.0)
    
    def _extract_fuel_indicators(self, input_text: str) -> List[str]:
        """Extract relevant fuel indicators from input"""
        indicators = []
        for category, words in self.nutrition_indicators.items():
            for word in words:
                if word in input_text:
                    indicators.append(word)
        
        for category, words in self.resource_indicators.items():
            for word in words:
                if word in input_text:
                    indicators.append(word)
        
        return indicators 