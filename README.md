# PrimeTime BD Intel System

A comprehensive Business Development Intelligence platform for the defense and aerospace industry, designed to automate job posting analysis, program mapping, and BD playbook generation.

## 🎯 Overview

PrimeTime BD Intel is an automated system that:
- **Scrapes** job postings from major defense contractors and staffing agencies
- **Maps** jobs to specific defense programs using AI analysis
- **Builds** organization charts from job posting patterns
- **Generates** comprehensive BD playbooks for target opportunities
- **Scores** programs based on opportunity potential

## 🏗️ Architecture

```
primetime-bd-intel/
│
├── /docs/                 # Strategy PDFs, past performance, playbooks
├── /n8n_workflows/        # JSON workflow files from Skool & custom scrapers
├── /scrapers/             # Apify/Puppeteer or Python Scrapy spiders
├── /pipelines/            # Modular automation engines
├── /config/               # Central config files
├── /data/                 # Local cache or sync to Postgres
├── /prompts/              # Reusable system prompts
├── /outputs/              # Final deliverables
└── /tests/                # Pytest or n8n test runs
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL 13+
- Redis 6+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/primetime-bd-intel.git
   cd primetime-bd-intel
   ```

2. **Set up environment**
   ```bash
   cp config/n8n.env .env
   # Edit .env with your API keys and configuration
   ```

3. **Start the stack**
   ```bash
   docker-compose up -d
   ```

4. **Access the system**
   - N8N Workflows: http://localhost:5678
   - Grafana Dashboard: http://localhost:3000
   - PostgreSQL: localhost:5432

## 📊 Core Components

### 1. Scraper Engine
- **ClearedJobs Scraper**: Extracts jobs from ClearedJobs.com
- **Apex Systems Spider**: Python Scrapy spider for Apex Systems
- **Insight Global Spider**: Scrapes Insight Global job postings
- **N8N Workflows**: Automated scraping workflows

### 2. Program Mapping Engine
- **AI Analysis**: Uses GPT-4 to map jobs to defense programs
- **Confidence Scoring**: Rates mapping accuracy
- **Program Dictionary**: Comprehensive program reference data

### 3. Organization Chart Engine
- **Relationship Inference**: Builds org charts from job patterns
- **Hierarchy Detection**: Identifies reporting relationships
- **Contact Mapping**: Maps key decision makers

### 4. Playbook Engine
- **BD Strategy Generation**: Creates comprehensive playbooks
- **Opportunity Analysis**: Identifies key opportunities
- **Action Planning**: Generates actionable next steps

### 5. Scoring Engine
- **Program Scoring**: Rates opportunity potential
- **Risk Assessment**: Evaluates competitive landscape
- **Resource Planning**: Estimates resource requirements

## 🔧 Configuration

### Programs Dictionary
Edit `config/programs_dictionary.json` to add new defense programs:
```json
{
  "PROGRAM_CODE": {
    "full_name": "Program Full Name",
    "acronyms": ["PROGRAM", "CODE"],
    "code_names": ["Code Name"],
    "prime_contractor": "Prime Contractor",
    "contract_value": "1.0B",
    "clearance_levels": ["TS/SCI", "TS"],
    "locations": ["State1", "State2"],
    "key_skills": ["skill1", "skill2"]
  }
}
```

### Settings
Configure the system in `config/settings.yaml`:
- API endpoints and keys
- Scraping parameters
- Quality thresholds
- Notification settings

## 📈 Usage Examples

### Running Scrapers

```bash
# Run Python scrapers
cd scrapers
scrapy crawl apex_systems -o data/jobs_raw/apex_systems.json
scrapy crawl insight_global -o data/jobs_raw/insight_global.json

# Import N8N workflows
# Navigate to http://localhost:5678
# Import workflows from n8n_workflows/
```

### Program Mapping

```bash
# Run program mapping engine
python pipelines/mapping_engine/map_jobs_to_programs.py

# Check results
python pipelines/scoring_engine/score_programs.py
```

### Generate Playbooks

```bash
# Generate BD playbook for specific company/program
python pipelines/playbook_engine/build_humint_playbook.py \
  --company "Northrop Grumman" \
  --program "GBSD" \
  --output "outputs/playbooks/ng_gbsd_playbook.md"
```

## 📊 Data Flow

1. **Collection**: Scrapers collect job postings from multiple sources
2. **Normalization**: Raw data is cleaned and standardized
3. **Mapping**: AI maps jobs to specific defense programs
4. **Enrichment**: Organization charts and intelligence are built
5. **Analysis**: Programs are scored and opportunities identified
6. **Output**: BD playbooks and call sheets are generated

## 🔍 Key Features

### Intelligent Program Mapping
- Uses GPT-4 to analyze job descriptions
- Maps to specific defense programs (GBSD, NGAD, F-35, etc.)
- Provides confidence scores and reasoning

### Automated BD Intelligence
- Builds organization charts from job patterns
- Identifies key decision makers
- Tracks hiring trends and program activity

### Comprehensive Playbooks
- Data-driven opportunity analysis
- Specific action plans and timelines
- Risk assessment and mitigation strategies

### Real-time Monitoring
- Automated job scraping every 6 hours
- Program mapping every 2 hours
- Email notifications for new opportunities

## 🛡️ Security

- Respects robots.txt and rate limiting
- Secure API key management
- Encrypted data storage
- Audit logging of all activities

## 📝 API Documentation

### Job Data Format
```json
{
  "job_id": "unique_identifier",
  "title": "Job Title",
  "company": "Company Name",
  "location": "Location",
  "clearance_level": "TS/SCI",
  "description": "Job description",
  "url": "Job posting URL",
  "posted_date": "2024-01-01T00:00:00Z",
  "source": "Data source",
  "scraped_at": "2024-01-01T00:00:00Z"
}
```

### Program Mapping Output
```json
{
  "job_id": "unique_identifier",
  "mapped_programs": ["GBSD", "B-21"],
  "confidence_score": 0.95,
  "reasoning": "Explanation of mapping",
  "keywords_found": ["ICBM", "nuclear", "strategic"]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in `/docs/`
- Review the configuration examples

## 🔄 Roadmap

- [ ] Additional job board integrations
- [ ] Advanced AI analysis capabilities
- [ ] Real-time dashboard
- [ ] Mobile application
- [ ] API for external integrations
- [ ] Advanced reporting and analytics

---

**PrimeTime BD Intel** - Transforming job postings into actionable BD intelligence.
