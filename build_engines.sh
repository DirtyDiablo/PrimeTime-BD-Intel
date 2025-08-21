#!/bin/bash

# Go into your repo root (assumes you're already in primetime-bd-intel)
cd "$(pwd)"

# Create the Engines folder
mkdir -p engines

# 1. Scraper Engine
mkdir -p engines/scraper_engine
cat <<EOF > engines/scraper_engine/README.md
# Scraper Engine

**Purpose:**  
Collect cleared staffing job postings daily from competitor sites, ClearanceJobs, LinkedIn, SAM.gov, FPDS, and USAspending. Normalize into a unified Jobs dataset.

**Setup Needs:**  
- **config/**: source URLs, API keys, scrape schedules, ATS selectors.  
- **data/**: 
  - /jobs_raw – raw scraped JSON
  - /jobs_clean – normalized postings
- **prompts/**: job field extraction & cleaning rules.  
- **outputs/**: jobs dataset CSV/JSON for downstream engines.
EOF

# 2. Program Mapping Engine
mkdir -p engines/mapping_engine
cat <<EOF > engines/mapping_engine/README.md
# Program Mapping Engine

**Purpose:**  
Match scraped jobs to DoD Programs (e.g. Sentinel GBSD, IBCS) and infer the Prime contractor. Enrich job postings with program_name + prime_contractor.

**Setup Needs:**  
- **config/**: 
  - program_keywords.json (Sentinel, GBSD, etc.)
  - primes_lookup.json (Program → Prime)
- **data/**: enriched_jobs/ with mapped jobs.  
- **prompts/**: semantic mapping + disambiguation prompts.  
- **outputs/**: Programs table with {program_name, prime, jobs_count, companies_hiring}.
EOF

# 3. Org Chart Reconstruction Engine
mkdir -p engines/org_engine
cat <<EOF > engines/org_engine/README.md
# Org Chart Reconstruction Engine

**Purpose:**  
Infer team structures & hierarchies for each program using job titles, levels, and locations. Output org charts of management → leads → ICs.

**Setup Needs:**  
- **config/**: role_hierarchy.json (mapping of titles → levels).  
- **data/**: 
  - org_inference_inputs (enriched jobs by program)
  - org_structures (tree/graph JSON)
- **prompts/**: org-structure inference prompts.  
- **outputs/**: visual/text org charts per program.
EOF

# 4. HUMINT Playbook Builder
mkdir -p engines/playbook_engine
cat <<EOF > engines/playbook_engine/README.md
# HUMINT Playbook Builder

**Purpose:**  
Turn BD data (hiring gaps, pain points, clearance shortages) into cold call scripts, email openers, and meeting briefs for business development.

**Setup Needs:**  
- **config/**: outreach_templates.json, playbook_format.yaml.  
- **data/**: 
  - hiring_trends (chronic openings, surge data)
  - clearance_mismatches
- **prompts/**: outreach copy generation prompts (calls, emails).  
- **outputs/**: Playbooks per program, ready-to-send call sheets.
EOF

# 5. Program Scoring Engine
mkdir -p engines/scoring_engine
cat <<EOF > engines/scoring_engine/README.md
# Program Scoring Engine

**Purpose:**  
Score and rank programs (0–100) to prioritize BD. Factors: Hiring demand, Pain level, Contract size, Prime TS past performance fit, Competitive intensity.

**Setup Needs:**  
- **config/**: scoring_weights.yaml (weights for each factor).  
- **data/**: 
  - programs_metrics (funding, job counts, churn indicators)
- **prompts/**: report formatting prompts.  
- **outputs/**: Program Priority Dashboard (CSV, Airtable sync).
EOF

echo "✅ Engines folder and submodule READMEs created."
