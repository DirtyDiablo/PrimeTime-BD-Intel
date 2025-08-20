# Scraper Engine Pipeline

The Scraper Engine is responsible for collecting job postings from various sources and normalizing them into a consistent format for further processing.

## Overview

This pipeline handles:
- Web scraping from multiple job boards
- Data normalization and cleaning
- Quality filtering and validation
- Storage in raw data format
- Integration with the broader PrimeTime BD Intel system

## Components

### 1. Job Scrapers
- **ClearedJobs Scraper**: Extracts jobs from ClearedJobs.com
- **Apex Systems Scraper**: Scrapes Apex Systems job postings
- **Insight Global Scraper**: Collects jobs from Insight Global
- **Custom N8N Workflows**: Automated scraping workflows

### 2. Data Normalization
- **normalize_jobs.py**: Standardizes job data format
- **clearance_extractor.py**: Extracts and validates clearance levels
- **location_parser.py**: Parses and standardizes location data

### 3. Quality Control
- **job_validator.py**: Validates job data quality
- **duplicate_detector.py**: Identifies and handles duplicate jobs
- **data_cleaner.py**: Cleans and sanitizes job data

## Usage

### Running Individual Scrapers

```bash
# Run Apex Systems scraper
cd scrapers
scrapy crawl apex_systems -o data/jobs_raw/apex_systems.json

# Run Insight Global scraper
scrapy crawl insight_global -o data/jobs_raw/insight_global.json
```

### Running N8N Workflows

```bash
# Start N8N server
n8n start

# Import workflows from n8n_workflows/
# Workflows will run automatically based on their schedules
```

### Data Normalization

```bash
# Normalize scraped data
python pipelines/scraper_engine/normalize_jobs.py

# Process specific source
python pipelines/scraper_engine/normalize_jobs.py --source clearedjobs
```

## Configuration

### Scraper Settings
- Rate limiting and delays
- User agent rotation
- Proxy configuration
- Retry logic

### Data Quality Thresholds
- Minimum confidence scores
- Required field validation
- Duplicate detection sensitivity

### Output Formats
- JSON for raw data
- CSV for analysis
- Database storage

## Data Flow

1. **Collection**: Scrapers collect raw job data
2. **Storage**: Raw data stored in `data/jobs_raw/`
3. **Normalization**: Data cleaned and standardized
4. **Validation**: Quality checks and filtering
5. **Enrichment**: Ready for program mapping

## Monitoring

- Scraper success/failure rates
- Data quality metrics
- Processing times
- Error logging and alerting

## Integration

The Scraper Engine feeds into:
- **Mapping Engine**: For program identification
- **Organization Engine**: For org chart building
- **Playbook Engine**: For BD playbook generation
- **Scoring Engine**: For opportunity scoring

## Error Handling

- Automatic retry on failures
- Graceful degradation
- Error logging and reporting
- Alert notifications

## Security

- Respects robots.txt
- Rate limiting to avoid overwhelming servers
- Secure storage of sensitive data
- Audit logging of all activities

