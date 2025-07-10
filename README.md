# HHAC (Healing Hand AI Council) - Seven Domain Cross-Regulation System

## Problem Statement
Current AI optimizes single metrics causing imbalanced, harmful outcomes. Humans need holistic decision-making that considers all aspects of wellbeing simultaneously. Traditional systems create dependency; we need technology that empowers human wisdom.

## Solution Overview
HHAC uses seven specialized AI domains that must reach consensus through a council core before any recommendation. This prevents tunnel-vision optimization by ensuring every suggestion considers the whole human experience. Unlike single-focus AI, HHAC thinks like a healthy human - balancing competing needs to support genuine thriving.

## The Seven Domains

### 🧠 Mind
- Cognitive health, learning, mental clarity, emotional processing
- Decision-making patterns, stress management, cognitive load assessment

### 💪 Body  
- Physical health, movement, medical needs, pain management
- Energy levels, physical comfort, movement patterns, health metrics

### ⚡ Fuel
- Nutrition, resources, energy inputs, sustainable consumption
- Dietary patterns, resource availability, energy optimization

### 😴 Rest
- Sleep, recovery, restoration, processing time
- Sleep quality, recovery needs, downtime requirements

### 🤝 Belong
- Connection, relationships, community, shared purpose
- Social needs, relationship health, community engagement

### 🛡️ Safety
- Physical/emotional security, stability, boundaries
- Risk assessment, security needs, boundary maintenance

### 🎯 Purpose
- Meaning, goals, contribution, legacy building
- Goal alignment, meaning-making, contribution patterns

## Cross-Regulation Mechanism
Each specialized AI domain operates autonomously while continuously sharing data with all other domains through the council core. Before any recommendation reaches the user, it must pass a consensus protocol where each domain evaluates the suggestion against its specialized metrics.

The council core synthesizes these evaluations, weighing them against personalized user patterns, but maintains Safety as a protected class - no recommendation can compromise safety protocols without explicit, informed user override.

## Data Dignity Commitment
- All user inputs remain encrypted and owned by the user
- The Great Input grows collective wisdom through patterns, never individual data exposure
- Users can delete their data entirely, export their personal insights, or contribute anonymized patterns
- No data monetization. No surveillance. Your pain is not our product.

## Failure Mode Transparency
When HHAC cannot reach consensus or detects potential harm patterns, it defaults to transparency: "I'm seeing conflicting needs between your domains that I'm not equipped to balance. Here's what each domain is signaling…" The system admits limitations rather than forcing solutions.

## Key Differentiator
This is not an optimization engine. It's a wisdom system that honors human complexity.

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- PostgreSQL (for data storage)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd hhac-system

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/init_db.py

# Run tests
python -m pytest tests/
```

### Running the System
```bash
# Start the backend API
python src/main.py

# Start the frontend (in another terminal)
npm run dev
```

## Architecture

```
hhac-system/
├── src/
│   ├── domains/           # Seven specialized AI domains
│   │   ├── mind/         # Cognitive and emotional processing
│   │   ├── body/         # Physical health and movement
│   │   ├── fuel/         # Nutrition and resources
│   │   ├── rest/         # Sleep and recovery
│   │   ├── belong/       # Relationships and community
│   │   ├── safety/       # Security and boundaries
│   │   └── purpose/      # Meaning and goals
│   ├── council_core/     # Consensus and synthesis engine
│   ├── data_privacy/     # Encryption and data dignity
│   ├── api/             # REST API endpoints
│   └── utils/           # Shared utilities
├── tests/               # Test suite
├── docs/               # Documentation
└── config/             # Configuration files
```

## Example Usage

```python
from hhac.council_core import HHACCouncil
from hhac.domains import UserContext

# Initialize the council
council = HHACCouncil()

# Create user context
context = UserContext(
    user_id="user123",
    current_state={
        "energy_level": 0.3,
        "stress_level": 0.8,
        "sleep_debt": 6,
        "work_deadline": "2024-01-15"
    }
)

# Get holistic recommendation
recommendation = council.get_recommendation(
    user_input="I'm exhausted but need to finish this project",
    context=context
)

print(recommendation)
# Output: "I notice you're running on a 3-day sleep deficit. Three balanced options: 
# (A) 20-minute power nap then focused work, 
# (B) Communicate delay to team and rest fully, 
# (C) Fuel with protein and work for 1 hour max. What serves you best right now?"
```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Patent Status
HHAC Patent Pending - Thee Phoenix Project LLC

---

**Building Human-Centered AI That Listens** 