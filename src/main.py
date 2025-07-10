"""
HHAC Main Application

Demonstrates the Healing Hand AI Council system in action.
This is the main entry point for the HHAC system.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

# Import the council and domain classes
from council_core.council import HHACCouncil, UserContext


async def main():
    """Main demonstration of the HHAC system"""
    print("🧠💪⚡😴🤝🛡️🎯")
    print("HHAC (Healing Hand AI Council) - Seven Domain Cross-Regulation System")
    print("=" * 70)
    
    # Initialize the council
    print("\nInitializing HHAC Council...")
    council = HHACCouncil()
    
    # Create user context (example from problem statement)
    context = UserContext(
        user_id="user123",
        current_state={
            "energy_level": 0.3,      # Very low energy
            "stress_level": 0.8,      # High stress
            "sleep_debt": 6,          # 6 hours of sleep debt
            "work_deadline": "2024-01-15",  # Work deadline
            "cognitive_load": 0.7,    # High cognitive load
            "mental_fatigue": 0.8,    # High mental fatigue
            "pain_level": 0.2,        # Low pain
            "movement_level": 0.3,    # Low movement
            "nutrition_need": 0.6,    # Moderate nutrition need
            "hydration_need": 0.5,    # Moderate hydration need
            "resource_availability": 0.4,  # Limited resources
            "risk_level": 0.1,        # Low safety risk
            "crisis_level": 0.0,      # No crisis
            "boundary_concern": 0.2,  # Low boundary concern
            "stability_level": 0.6    # Moderate stability
        },
        preferences={
            "work_style": "focused",
            "rest_preference": "short_breaks",
            "communication_style": "direct"
        },
        history=[],
        timestamp=datetime.now()
    )
    
    # Example user input from problem statement
    user_input = "I'm exhausted but need to finish this project"
    
    print(f"\nUser Input: '{user_input}'")
    print(f"Current State: Energy={context.current_state['energy_level']:.1%}, "
          f"Stress={context.current_state['stress_level']:.1%}, "
          f"Sleep Debt={context.current_state['sleep_debt']} hours")
    
    print("\n" + "="*70)
    print("COUNCIL EVALUATION IN PROGRESS...")
    print("="*70)
    
    # Get recommendation through the council
    try:
        recommendation = await council.get_recommendation(user_input, context)
        
        print("\n🎯 FINAL COUNCIL RECOMMENDATION:")
        print("-" * 50)
        print(f"Recommendation: {recommendation.recommendation}")
        print(f"Reasoning: {recommendation.reasoning}")
        print(f"Consensus Level: {recommendation.consensus_level}")
        print(f"Confidence: {recommendation.confidence:.1%}")
        
        if recommendation.alternatives:
            print(f"\n🔄 Alternative Options:")
            for i, alt in enumerate(recommendation.alternatives, 1):
                print(f"  {i}. {alt}")
        
        if recommendation.safety_concerns:
            print(f"\n⚠️  Safety Concerns:")
            for concern in recommendation.safety_concerns:
                print(f"  • {concern}")
        
        print(f"\n🧠 Domain Insights:")
        for domain, insight in recommendation.domain_insights.items():
            print(f"  {domain.upper()}: {insight}")
        
    except Exception as e:
        print(f"Error in council evaluation: {e}")
        import traceback
        traceback.print_exc()
    
    # Show council status
    print("\n" + "="*70)
    print("COUNCIL STATUS:")
    print("-" * 50)
    status = council.get_council_status()
    print(f"Session Count: {status['session_count']}")
    print(f"Council Version: {status['council_version']}")
    print(f"Last Consensus: {status['last_consensus_time']}")
    
    print(f"\nDomain Status:")
    for domain_name, domain_info in status['domains'].items():
        print(f"  {domain_name.upper()}: {domain_info['description']}")


def run_example():
    """Run the example demonstration"""
    print("Starting HHAC System Demonstration...")
    print("This demonstrates the example from the problem statement:")
    print("User: 'I'm exhausted but need to finish this project'")
    print("Expected: Three balanced options considering all domains")
    print()
    
    # Run the async main function
    asyncio.run(main())


if __name__ == "__main__":
    run_example() 