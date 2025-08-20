#!/usr/bin/env python3
"""
Program Mapping Engine for PrimeTime BD Intel

Uses AI analysis to map job postings to specific defense programs.
Provides confidence scoring and reasoning for each mapping.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import openai
import yaml
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import load_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProgramMappingEngine:
    """AI-powered engine for mapping jobs to defense programs."""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the mapping engine with configuration."""
        self.settings = load_settings(config_path)
        self.programs_dict = self._load_programs_dictionary()
        self.openai_client = self._setup_openai()
        
    def _load_programs_dictionary(self) -> Dict:
        """Load the programs dictionary from config."""
        try:
            with open("config/programs_dictionary.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("Programs dictionary not found")
            return {}
            
    def _setup_openai(self) -> openai.OpenAI:
        """Setup OpenAI client with API key."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        return openai.OpenAI(api_key=api_key)
        
    def map_job_to_programs(self, job_data: Dict) -> Dict:
        """Map a single job to relevant defense programs."""
        try:
            # Prepare prompt for AI analysis
            prompt = self._create_mapping_prompt(job_data)
            
            # Get AI response
            response = self.openai_client.chat.completions.create(
                model=self.settings["apis"]["openai"]["model"],
                messages=[
                    {"role": "system", "content": "You are an expert in defense industry programs and job analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.settings["apis"]["openai"]["max_tokens"],
                temperature=self.settings["apis"]["openai"]["temperature"]
            )
            
            # Parse AI response
            ai_analysis = response.choices[0].message.content
            mapping_result = self._parse_ai_response(ai_analysis, job_data)
            
            return mapping_result
            
        except Exception as e:
            logger.error(f"Error mapping job {job_data.get('job_id', 'unknown')}: {e}")
            return self._create_fallback_mapping(job_data)
    
    def _create_mapping_prompt(self, job_data: Dict) -> str:
        """Create the prompt for AI analysis."""
        programs_info = "\n".join([
            f"- {code}: {details['full_name']} ({details['prime_contractor']})"
            for code, details in self.programs_dict.items()
        ])
        
        prompt = f"""
        Analyze this job posting and map it to relevant defense programs.
        
        Job Details:
        - Title: {job_data.get('title', 'N/A')}
        - Company: {job_data.get('company', 'N/A')}
        - Location: {job_data.get('location', 'N/A')}
        - Clearance: {job_data.get('clearance_level', 'N/A')}
        - Description: {job_data.get('description', 'N/A')}
        
        Available Programs:
        {programs_info}
        
        Please provide:
        1. List of relevant programs (program codes)
        2. Confidence score (0.0-1.0)
        3. Reasoning for the mapping
        4. Key keywords that support the mapping
        
        Format your response as JSON:
        {{
            "mapped_programs": ["PROGRAM1", "PROGRAM2"],
            "confidence_score": 0.85,
            "reasoning": "Explanation here",
            "keywords_found": ["keyword1", "keyword2"]
        }}
        """
        return prompt
    
    def _parse_ai_response(self, ai_response: str, job_data: Dict) -> Dict:
        """Parse the AI response and extract mapping information."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                
                return {
                    "job_id": job_data.get("job_id"),
                    "mapped_programs": parsed.get("mapped_programs", []),
                    "confidence_score": parsed.get("confidence_score", 0.0),
                    "reasoning": parsed.get("reasoning", ""),
                    "keywords_found": parsed.get("keywords_found", []),
                    "mapped_at": datetime.now().isoformat(),
                    "source": "ai_analysis"
                }
        except Exception as e:
            logger.warning(f"Failed to parse AI response: {e}")
        
        # Fallback to keyword-based mapping
        return self._keyword_based_mapping(job_data)
    
    def _keyword_based_mapping(self, job_data: Dict) -> Dict:
        """Fallback mapping based on keyword matching."""
        job_text = f"{job_data.get('title', '')} {job_data.get('description', '')}".lower()
        mapped_programs = []
        keywords_found = []
        
        for program_code, program_details in self.programs_dict.items():
            # Check program name and acronyms
            program_terms = [program_details['full_name'].lower()] + \
                           [acronym.lower() for acronym in program_details.get('acronyms', [])] + \
                           [code_name.lower() for code_name in program_details.get('code_names', [])]
            
            # Check key skills
            program_skills = [skill.lower() for skill in program_details.get('key_skills', [])]
            
            # Calculate match score
            match_score = 0
            matched_keywords = []
            
            for term in program_terms:
                if term in job_text:
                    match_score += 0.3
                    matched_keywords.append(term)
            
            for skill in program_skills:
                if skill in job_text:
                    match_score += 0.2
                    matched_keywords.append(skill)
            
            # Check company match
            if program_details.get('prime_contractor', '').lower() in job_data.get('company', '').lower():
                match_score += 0.4
            
            if match_score >= self.settings["program_mapping"]["keyword_match_threshold"]:
                mapped_programs.append(program_code)
                keywords_found.extend(matched_keywords)
        
        return {
            "job_id": job_data.get("job_id"),
            "mapped_programs": mapped_programs,
            "confidence_score": min(0.7, len(mapped_programs) * 0.2),
            "reasoning": f"Keyword-based mapping using terms: {', '.join(set(keywords_found))}",
            "keywords_found": list(set(keywords_found)),
            "mapped_at": datetime.now().isoformat(),
            "source": "keyword_matching"
        }
    
    def _create_fallback_mapping(self, job_data: Dict) -> Dict:
        """Create a fallback mapping when AI analysis fails."""
        return {
            "job_id": job_data.get("job_id"),
            "mapped_programs": [],
            "confidence_score": 0.0,
            "reasoning": "Failed to analyze job posting",
            "keywords_found": [],
            "mapped_at": datetime.now().isoformat(),
            "source": "fallback"
        }
    
    def process_jobs_batch(self, jobs_file: str, output_file: str) -> None:
        """Process a batch of jobs and save mapping results."""
        try:
            # Load jobs
            with open(jobs_file, "r") as f:
                jobs = json.load(f)
            
            logger.info(f"Processing {len(jobs)} jobs for program mapping")
            
            # Process each job
            mapping_results = []
            for job in jobs:
                result = self.map_job_to_programs(job)
                mapping_results.append(result)
                
                # Log progress
                if len(mapping_results) % 10 == 0:
                    logger.info(f"Processed {len(mapping_results)}/{len(jobs)} jobs")
            
            # Save results
            with open(output_file, "w") as f:
                json.dump(mapping_results, f, indent=2)
            
            logger.info(f"Program mapping completed. Results saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error processing jobs batch: {e}")
            raise

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Map jobs to defense programs")
    parser.add_argument("--input", "-i", required=True, help="Input jobs JSON file")
    parser.add_argument("--output", "-o", required=True, help="Output mapping JSON file")
    parser.add_argument("--config", "-c", default="config/settings.yaml", help="Configuration file")
    
    args = parser.parse_args()
    
    try:
        # Initialize engine
        engine = ProgramMappingEngine(args.config)
        
        # Process jobs
        engine.process_jobs_batch(args.input, args.output)
        
        print(f"Program mapping completed successfully!")
        print(f"Results saved to: {args.output}")
        
    except Exception as e:
        logger.error(f"Program mapping failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
