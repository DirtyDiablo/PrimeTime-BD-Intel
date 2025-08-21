# Program Scoring Engine

**Purpose:**  
Score and rank programs (0–100) to prioritize BD. Factors: Hiring demand, Pain level, Contract size, Prime TS past performance fit, Competitive intensity.

**Setup Needs:**  
- **config/**: scoring_weights.yaml (weights for each factor).  
- **data/**: 
  - programs_metrics (funding, job counts, churn indicators)
- **prompts/**: report formatting prompts.  
- **outputs/**: Program Priority Dashboard (CSV, Airtable sync).
