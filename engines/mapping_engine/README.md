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
