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
