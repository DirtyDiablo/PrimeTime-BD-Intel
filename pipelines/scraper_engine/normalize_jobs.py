#!/usr/bin/env python3
"""
Job Data Normalization Script
Normalizes scraped job data into a consistent format for further processing.
"""

import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional
import argparse
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class JobNormalizer:
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.logger = logging.getLogger(__name__)
        self.clearance_patterns = {
            'TS/SCI': r'\b(?:TS/SCI|Top\s+Secret/SCI|Top\s+Secret\s+SCI)\b',
            'TS': r'\b(?:TS|Top\s+Secret)\b',
            'Secret': r'\b(?:Secret|SECRET)\b',
            'Confidential': r'\b(?:Confidential|CONFIDENTIAL)\b'
        }
        
    def normalize_job(self, job_data: Dict) -> Dict:
        """Normalize a single job record."""
        try:
            normalized = {
                'job_id': self._normalize_job_id(job_data.get('job_id', '')),
                'title': self._normalize_title(job_data.get('title', '')),
                'company': self._normalize_company(job_data.get('company', '')),
                'location': self._normalize_location(job_data.get('location', '')),
                'clearance_level': self._extract_clearance(job_data.get('description', '')),
                'description': self._clean_description(job_data.get('description', '')),
                'url': job_data.get('url', ''),
                'posted_date': self._normalize_date(job_data.get('posted_date', '')),
                'source': job_data.get('source', ''),
                'scraped_at': job_data.get('scraped_at', datetime.now().isoformat()),
                'normalized_at': datetime.now().isoformat()
            }
            
            return normalized
            
        except Exception as e:
            self.logger.error(f"Error normalizing job {job_data.get('job_id', 'unknown')}: {str(e)}")
            return None
    
    def _normalize_job_id(self, job_id: str) -> str:
        """Normalize job ID format."""
        if not job_id:
            return f"normalized_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Remove special characters and normalize
        normalized = re.sub(r'[^a-zA-Z0-9_-]', '_', job_id)
        return normalized.lower()
    
    def _normalize_title(self, title: str) -> str:
        """Normalize job title."""
        if not title:
            return ""
        
        # Remove extra whitespace and normalize
        normalized = re.sub(r'\s+', ' ', title.strip())
        return normalized
    
    def _normalize_company(self, company: str) -> str:
        """Normalize company name."""
        if not company:
            return ""
        
        # Standardize common company names
        company_mappings = {
            'apex systems': 'Apex Systems',
            'insight global': 'Insight Global',
            'clearancejobs': 'ClearedJobs',
            'clearedjobs.com': 'ClearedJobs'
        }
        
        normalized = company.strip().lower()
        return company_mappings.get(normalized, company.strip())
    
    def _normalize_location(self, location: str) -> str:
        """Normalize location format."""
        if not location:
            return ""
        
        # Remove extra whitespace and normalize
        normalized = re.sub(r'\s+', ' ', location.strip())
        
        # Standardize state abbreviations
        state_mappings = {
            'CA': 'California',
            'TX': 'Texas',
            'VA': 'Virginia',
            'MD': 'Maryland',
            'FL': 'Florida',
            'WA': 'Washington',
            'MO': 'Missouri',
            'CT': 'Connecticut',
            'UT': 'Utah',
            'CO': 'Colorado'
        }
        
        for abbr, full_name in state_mappings.items():
            normalized = re.sub(rf'\b{abbr}\b', full_name, normalized, flags=re.IGNORECASE)
        
        return normalized
    
    def _extract_clearance(self, description: str) -> Optional[str]:
        """Extract clearance level from description."""
        if not description:
            return None
        
        description_upper = description.upper()
        
        # Check for clearance patterns
        for clearance, pattern in self.clearance_patterns.items():
            if re.search(pattern, description_upper):
                return clearance
        
        return None
    
    def _clean_description(self, description: str) -> str:
        """Clean and normalize job description."""
        if not description:
            return ""
        
        # Remove HTML tags
        cleaned = re.sub(r'<[^>]+>', '', description)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove special characters that might cause issues
        cleaned = re.sub(r'[^\w\s\-.,!?()]', '', cleaned)
        
        return cleaned.strip()
    
    def _normalize_date(self, date_str: str) -> str:
        """Normalize date format."""
        if not date_str:
            return datetime.now().isoformat()
        
        try:
            # Try to parse various date formats
            date_formats = [
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%B %d, %Y',
                '%b %d, %Y'
            ]
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.isoformat()
                except ValueError:
                    continue
            
            # If no format matches, return current date
            return datetime.now().isoformat()
            
        except Exception:
            return datetime.now().isoformat()

def main():
    parser = argparse.ArgumentParser(description='Normalize scraped job data')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file path')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file path')
    parser.add_argument('--source', '-s', help='Source filter (optional)')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Initialize normalizer
    normalizer = JobNormalizer()
    
    try:
        # Load input data
        with open(args.input, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        
        logger.info(f"Loaded {len(jobs)} jobs from {args.input}")
        
        # Filter by source if specified
        if args.source:
            jobs = [job for job in jobs if job.get('source', '').lower() == args.source.lower()]
            logger.info(f"Filtered to {len(jobs)} jobs from source: {args.source}")
        
        # Normalize jobs
        normalized_jobs = []
        for job in jobs:
            normalized = normalizer.normalize_job(job)
            if normalized:
                normalized_jobs.append(normalized)
        
        logger.info(f"Normalized {len(normalized_jobs)} jobs")
        
        # Save normalized data
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(normalized_jobs, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved normalized data to {args.output}")
        
    except Exception as e:
        logger.error(f"Error processing jobs: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
