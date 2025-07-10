"""
Consensus Engine

Evaluates agreement between all domains and determines the final consensus level.
Handles the cross-regulation mechanism where all domains must reach consensus.
"""

from typing import Dict, Any, List
from datetime import datetime
from dataclasses import dataclass

from ..domains.base_domain import DomainResponse, ConsensusLevel


@dataclass
class ConsensusResult:
    """Result of consensus evaluation"""
    overall_consensus: str
    domain_agreement: Dict[str, str]
    conflict_resolution: List[str]
    confidence: float
    reasoning: str
    timestamp: datetime


class ConsensusEngine:
    """
    Consensus Engine - Cross-Regulation Mechanism
    
    Evaluates agreement between all seven domains and determines
    the final consensus level. Handles conflicts and ensures
    balanced decision-making.
    """
    
    def __init__(self):
        """Initialize the consensus engine"""
        self.consensus_weights = {
            "safety": 1.0,      # Safety has veto power
            "mind": 0.9,        # High weight for cognitive health
            "body": 0.8,        # High weight for physical health
            "purpose": 0.7,     # Medium-high weight for meaning
            "belong": 0.6,      # Medium weight for relationships
            "rest": 0.6,        # Medium weight for recovery
            "fuel": 0.5         # Medium weight for resources
        }
        
        self.consensus_thresholds = {
            "strong_agreement": 0.8,
            "agreement": 0.6,
            "neutral": 0.4,
            "disagreement": 0.2
        }
    
    async def evaluate_consensus(self, domain_responses: Dict[str, DomainResponse], 
                               context: Any) -> ConsensusResult:
        """
        Evaluate consensus between all domains.
        
        Args:
            domain_responses: Responses from all seven domains
            context: User context
            
        Returns:
            ConsensusResult with overall consensus and domain agreement
        """
        # Step 1: Check for safety blocks (highest priority)
        safety_response = domain_responses.get("safety")
        if safety_response and safety_response.consensus_level == ConsensusLevel.SAFETY_BLOCK:
            return self._handle_safety_consensus(safety_response)
        
        # Step 2: Calculate weighted consensus scores
        consensus_scores = self._calculate_consensus_scores(domain_responses)
        
        # Step 3: Identify conflicts and disagreements
        conflicts = self._identify_conflicts(domain_responses)
        
        # Step 4: Determine overall consensus level
        overall_consensus = self._determine_overall_consensus(consensus_scores, conflicts)
        
        # Step 5: Generate consensus reasoning
        reasoning = self._generate_consensus_reasoning(domain_responses, consensus_scores, conflicts)
        
        # Step 6: Calculate confidence
        confidence = self._calculate_consensus_confidence(consensus_scores, conflicts)
        
        return ConsensusResult(
            overall_consensus=overall_consensus,
            domain_agreement=self._get_domain_agreement(domain_responses),
            conflict_resolution=conflicts,
            confidence=confidence,
            reasoning=reasoning,
            timestamp=datetime.now()
        )
    
    def _handle_safety_consensus(self, safety_response: DomainResponse) -> ConsensusResult:
        """Handle safety block consensus - overrides everything else"""
        return ConsensusResult(
            overall_consensus="safety_block",
            domain_agreement={"safety": "block"},
            conflict_resolution=["Safety domain blocked recommendation"],
            confidence=safety_response.confidence,
            reasoning=f"SAFETY BLOCK: {safety_response.reasoning}",
            timestamp=datetime.now()
        )
    
    def _calculate_consensus_scores(self, domain_responses: Dict[str, DomainResponse]) -> Dict[str, float]:
        """Calculate weighted consensus scores for each domain"""
        scores = {}
        
        for domain_name, response in domain_responses.items():
            weight = self.consensus_weights.get(domain_name, 0.5)
            
            # Convert consensus level to numeric score
            consensus_score = self._consensus_level_to_score(response.consensus_level)
            
            # Apply domain weight
            weighted_score = consensus_score * weight
            
            scores[domain_name] = weighted_score
        
        return scores
    
    def _consensus_level_to_score(self, consensus_level: ConsensusLevel) -> float:
        """Convert consensus level to numeric score"""
        score_mapping = {
            ConsensusLevel.STRONG_AGREEMENT: 1.0,
            ConsensusLevel.AGREEMENT: 0.8,
            ConsensusLevel.NEUTRAL: 0.5,
            ConsensusLevel.DISAGREEMENT: 0.2,
            ConsensusLevel.STRONG_DISAGREEMENT: 0.0,
            ConsensusLevel.SAFETY_BLOCK: -1.0  # Special case
        }
        
        return score_mapping.get(consensus_level, 0.5)
    
    def _identify_conflicts(self, domain_responses: Dict[str, DomainResponse]) -> List[str]:
        """Identify conflicts and disagreements between domains"""
        conflicts = []
        
        # Check for strong disagreements
        strong_disagreements = []
        agreements = []
        
        for domain_name, response in domain_responses.items():
            if response.consensus_level == ConsensusLevel.STRONG_DISAGREEMENT:
                strong_disagreements.append(domain_name)
            elif response.consensus_level in [ConsensusLevel.STRONG_AGREEMENT, ConsensusLevel.AGREEMENT]:
                agreements.append(domain_name)
        
        # Report conflicts
        if strong_disagreements:
            conflicts.append(f"Strong disagreement from: {', '.join(strong_disagreements)}")
        
        if len(agreements) < 3:  # Need at least 3 domains in agreement
            conflicts.append("Insufficient domain agreement")
        
        # Check for domain-specific conflicts
        domain_conflicts = self._check_domain_conflicts(domain_responses)
        conflicts.extend(domain_conflicts)
        
        return conflicts
    
    def _check_domain_conflicts(self, domain_responses: Dict[str, DomainResponse]) -> List[str]:
        """Check for specific conflicts between domains"""
        conflicts = []
        
        # Mind vs Body conflicts (mental vs physical needs)
        mind_response = domain_responses.get("mind")
        body_response = domain_responses.get("body")
        
        if mind_response and body_response:
            if (mind_response.consensus_level == ConsensusLevel.AGREEMENT and 
                body_response.consensus_level == ConsensusLevel.DISAGREEMENT):
                conflicts.append("Mind-Body conflict: Mental needs vs physical limitations")
        
        # Rest vs Purpose conflicts (recovery vs achievement)
        rest_response = domain_responses.get("rest")
        purpose_response = domain_responses.get("purpose")
        
        if rest_response and purpose_response:
            if (rest_response.consensus_level == ConsensusLevel.AGREEMENT and 
                purpose_response.consensus_level == ConsensusLevel.DISAGREEMENT):
                conflicts.append("Rest-Purpose conflict: Recovery needs vs achievement goals")
        
        # Fuel vs Body conflicts (nutrition vs physical state)
        fuel_response = domain_responses.get("fuel")
        if fuel_response and body_response:
            if (fuel_response.consensus_level == ConsensusLevel.AGREEMENT and 
                body_response.consensus_level == ConsensusLevel.DISAGREEMENT):
                conflicts.append("Fuel-Body conflict: Nutritional needs vs physical state")
        
        return conflicts
    
    def _determine_overall_consensus(self, consensus_scores: Dict[str, float], 
                                   conflicts: List[str]) -> str:
        """Determine overall consensus level based on scores and conflicts"""
        if not consensus_scores:
            return "neutral"
        
        # Calculate average weighted score
        total_score = sum(consensus_scores.values())
        total_weight = sum(self.consensus_weights.get(domain, 0.5) 
                          for domain in consensus_scores.keys())
        
        if total_weight == 0:
            return "neutral"
        
        average_score = total_score / total_weight
        
        # Determine consensus level based on thresholds
        if average_score >= self.consensus_thresholds["strong_agreement"]:
            return "strong_agreement"
        elif average_score >= self.consensus_thresholds["agreement"]:
            return "agreement"
        elif average_score >= self.consensus_thresholds["neutral"]:
            return "neutral"
        elif average_score >= self.consensus_thresholds["disagreement"]:
            return "disagreement"
        else:
            return "strong_disagreement"
    
    def _get_domain_agreement(self, domain_responses: Dict[str, DomainResponse]) -> Dict[str, str]:
        """Get agreement status for each domain"""
        agreement = {}
        
        for domain_name, response in domain_responses.items():
            agreement[domain_name] = response.consensus_level.value
        
        return agreement
    
    def _generate_consensus_reasoning(self, domain_responses: Dict[str, DomainResponse],
                                    consensus_scores: Dict[str, float],
                                    conflicts: List[str]) -> str:
        """Generate reasoning for the consensus decision"""
        reasoning_parts = []
        
        # Count agreement levels
        agreement_counts = {
            "strong_agreement": 0,
            "agreement": 0,
            "neutral": 0,
            "disagreement": 0,
            "strong_disagreement": 0
        }
        
        for response in domain_responses.values():
            agreement_counts[response.consensus_level.value] += 1
        
        # Generate summary
        if agreement_counts["strong_agreement"] > 0:
            reasoning_parts.append(f"{agreement_counts['strong_agreement']} domains strongly agree")
        
        if agreement_counts["agreement"] > 0:
            reasoning_parts.append(f"{agreement_counts['agreement']} domains agree")
        
        if agreement_counts["disagreement"] > 0:
            reasoning_parts.append(f"{agreement_counts['disagreement']} domains disagree")
        
        if agreement_counts["strong_disagreement"] > 0:
            reasoning_parts.append(f"{agreement_counts['strong_disagreement']} domains strongly disagree")
        
        # Add conflict information
        if conflicts:
            reasoning_parts.append(f"Conflicts detected: {'; '.join(conflicts)}")
        
        if reasoning_parts:
            return f"Council consensus: {'; '.join(reasoning_parts)}"
        else:
            return "Council consensus: All domains neutral"
    
    def _calculate_consensus_confidence(self, consensus_scores: Dict[str, float],
                                      conflicts: List[str]) -> float:
        """Calculate confidence in the consensus decision"""
        if not consensus_scores:
            return 0.0
        
        # Base confidence on score variance
        scores = list(consensus_scores.values())
        avg_score = sum(scores) / len(scores)
        
        # Lower variance = higher confidence
        variance = sum((score - avg_score) ** 2 for score in scores) / len(scores)
        variance_penalty = min(variance * 2, 0.5)  # Cap penalty at 0.5
        
        # Conflict penalty
        conflict_penalty = len(conflicts) * 0.1
        
        # Base confidence
        base_confidence = 0.7
        
        # Apply penalties
        confidence = base_confidence - variance_penalty - conflict_penalty
        
        return max(confidence, 0.0) 