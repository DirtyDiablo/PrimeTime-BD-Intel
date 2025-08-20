#!/usr/bin/env python3
"""
Insight Global Job Scraper
Scrapes job postings from Insight Global website for positions requiring security clearances.
"""

import scrapy
import json
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import logging

class InsightGlobalSpider(scrapy.Spider):
    name = 'insight_global'
    allowed_domains = ['insightglobal.com', 'jobs.insightglobal.com']
    
    # Start URLs for different clearance levels
    start_urls = [
        'https://jobs.insightglobal.com/search?keywords=clearance',
        'https://jobs.insightglobal.com/search?keywords=TS%2FSCI',
        'https://jobs.insightglobal.com/search?keywords=Top%20Secret',
        'https://jobs.insightglobal.com/search?keywords=Secret',
        'https://jobs.insightglobal.com/search?keywords=DoD',
        'https://jobs.insightglobal.com/search?keywords=defense',
        'https://jobs.insightglobal.com/search?keywords=military',
        'https://jobs.insightglobal.com/search?keywords=government',
    ]
    
    # Custom settings for this spider
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'FEEDS': {
            'data/jobs_raw/insight_global_%(time)s.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 2,
                'overwrite': False
            }
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(InsightGlobalSpider, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.scraped_count = 0
        self.clearance_keywords = [
            'TS/SCI', 'Top Secret/SCI', 'Top Secret SCI',
            'TS', 'Top Secret',
            'Secret', 'SECRET',
            'Confidential', 'CONFIDENTIAL',
            'DoD', 'Department of Defense',
            'Clearance', 'CLEARANCE',
            'Security Clearance', 'SECURITY CLEARANCE',
            'Government Clearance', 'GOVERNMENT CLEARANCE'
        ]
        
    def parse(self, response):
        """Parse the job search results page."""
        self.logger.info(f"Parsing search results: {response.url}")
        
        # Extract job listing links
        job_links = response.css('a[href*="/job/"]::attr(href)').getall()
        
        for link in job_links:
            full_url = urljoin(response.url, link)
            if self._is_job_detail_page(full_url):
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_job_detail,
                    meta={'source_url': response.url}
                )
        
        # Follow pagination
        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=urljoin(response.url, next_page),
                callback=self.parse
            )
    
    def parse_job_detail(self, response):
        """Parse individual job detail page."""
        self.logger.info(f"Parsing job detail: {response.url}")
        
        try:
            # Extract job information
            job_data = {
                'job_id': self._extract_job_id(response),
                'title': self._extract_title(response),
                'company': 'Insight Global',
                'location': self._extract_location(response),
                'clearance_level': self._extract_clearance(response),
                'description': self._extract_description(response),
                'url': response.url,
                'posted_date': self._extract_posted_date(response),
                'source': 'Insight Global',
                'scraped_at': datetime.now().isoformat(),
                'raw_data': self._extract_raw_data(response)
            }
            
            # Only yield if clearance level is found
            if job_data['clearance_level']:
                self.scraped_count += 1
                self.logger.info(f"Scraped job {self.scraped_count}: {job_data['title']}")
                yield job_data
            else:
                self.logger.debug(f"No clearance found for job: {job_data['title']}")
                
        except Exception as e:
            self.logger.error(f"Error parsing job detail {response.url}: {str(e)}")
    
    def _extract_job_id(self, response):
        """Extract job ID from URL or page content."""
        # Try to extract from URL first
        url_path = urlparse(response.url).path
        job_id_match = re.search(r'/job/(\d+)', url_path)
        if job_id_match:
            return f"insight_{job_id_match.group(1)}"
        
        # Try to extract from page content
        job_id_element = response.css('[data-job-id]::attr(data-job-id)').get()
        if job_id_element:
            return f"insight_{job_id_element}"
        
        # Fallback to URL hash
        return f"insight_{hash(response.url) % 1000000}"
    
    def _extract_title(self, response):
        """Extract job title."""
        title_selectors = [
            'h1.job-title::text',
            '.job-header h1::text',
            '[data-testid="job-title"]::text',
            'h1::text',
            '.title::text',
            '.job-details h1::text'
        ]
        
        for selector in title_selectors:
            title = response.css(selector).get()
            if title:
                return title.strip()
        
        return None
    
    def _extract_location(self, response):
        """Extract job location."""
        location_selectors = [
            '.job-location::text',
            '.location::text',
            '[data-testid="location"]::text',
            '.job-details .location::text',
            '.job-info .location::text'
        ]
        
        for selector in location_selectors:
            location = response.css(selector).get()
            if location:
                return location.strip()
        
        return None
    
    def _extract_clearance(self, response):
        """Extract clearance level from job description."""
        description = self._extract_description(response)
        if not description:
            return None
        
        # Look for clearance keywords in description
        description_upper = description.upper()
        for keyword in self.clearance_keywords:
            if keyword.upper() in description_upper:
                return keyword
        
        return None
    
    def _extract_description(self, response):
        """Extract job description."""
        description_selectors = [
            '.job-description',
            '.job-details .description',
            '[data-testid="job-description"]',
            '.description',
            '.job-content',
            '.job-details .content'
        ]
        
        for selector in description_selectors:
            description_elements = response.css(selector)
            if description_elements:
                # Get all text content
                description_text = ' '.join(description_elements.css('::text').getall())
                if description_text.strip():
                    return description_text.strip()
        
        return None
    
    def _extract_posted_date(self, response):
        """Extract job posted date."""
        date_selectors = [
            '.posted-date::text',
            '.job-date::text',
            '[data-testid="posted-date"]::text',
            '.date::text',
            '.job-info .date::text'
        ]
        
        for selector in date_selectors:
            date_text = response.css(selector).get()
            if date_text:
                return date_text.strip()
        
        return None
    
    def _extract_raw_data(self, response):
        """Extract raw HTML data for backup."""
        return {
            'html': response.text,
            'url': response.url,
            'headers': dict(response.headers)
        }
    
    def _is_job_detail_page(self, url):
        """Check if URL is a job detail page."""
        job_patterns = [
            r'/job/\d+',
            r'/jobs/\d+',
            r'/careers/.*job',
            r'/position/'
        ]
        
        for pattern in job_patterns:
            if re.search(pattern, url):
                return True
        
        return False
    
    def closed(self, reason):
        """Called when spider is closed."""
        self.logger.info(f"Spider closed. Total jobs scraped: {self.scraped_count}")
        
        # Log summary
        if self.scraped_count > 0:
            self.logger.info(f"Successfully scraped {self.scraped_count} jobs from Insight Global")
        else:
            self.logger.warning("No jobs with clearance requirements found")

if __name__ == "__main__":
    # For testing the spider directly
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    
    process = CrawlerProcess(get_project_settings())
    process.crawl(InsightGlobalSpider)
    process.start()
