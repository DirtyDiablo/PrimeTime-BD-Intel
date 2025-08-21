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
