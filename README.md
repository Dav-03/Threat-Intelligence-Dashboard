# Threat Intelligence Dashboard
 
A full-stack security platform that ingests threat data from public feeds (AlienVault OTX, VirusTotal, Shodan), processes IoC, and visualizes them on a real-time dashboard.

 
## Tools Used
 
| Layer | Technology |
|---|---|
| Frontend | React 19, Vite, Tailwind CSS, Recharts, Leaflet, Faker |
| Backend API | FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Workers | Python, APScheduler |
| Infrastructure | Docker, Kubernetes, Terraform |
| CI/CD | GitHub Actions, ArgoCD |
 
## To Get Started
 
### Prerequisites
 
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Node.js v20+](https://nodejs.org)
- [Python 3.11+](https://www.python.org)
- [Git](https://git-scm.com)
### Install
 
```bash
git clone https://github.com/your-username/threat-intel-dashboard.git
cd threat-intel-dashboard
```
 
### Environment Variables
 
Create a `.env` file inside the `api/` folder:
 
```bash
cp api/.env.example api/.env
```
 
Fill in the values:
 
```
DATABASE_URL=postgresql://threatuser:threatpass@localhost:5432/threatdb
REDIS_URL=redis://localhost:6379
VIRUSTOTAL_API_KEY=yourKey
OTX_API_KEY=yourKey
```
 
**How to get API keys (both free):**
- VirusTotal: [virustotal.com](https://www.virustotal.com) → Sign up → Profile → API Key
- AlienVault OTX: [otx.alienvault.com](https://otx.alienvault.com) → Sign up → Settings → API Key
### Run locally
 
```bash
docker compose up --build
```
 
This starts all five services:
 
| Service | URL |
|---|---|
| React dashboard | http://localhost:5173 |
| FastAPI + Swagger docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |
 
### Database setup
 
With Docker running, open a second terminal and run:
 
```bash
cd api
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head
python seed.py
```
 
This applies all database migrations and seeds 100 fake IOC records for local development.
 
## Database Schema
 
| Table | Description |
|---|---|
| `iocs` | Indicators of compromise: IPs, domains, file hashes |
| `feeds` | Raw Shodan data: Ports, services, exposed infrastructure |
| `alerts` | Generated alerts linked to IOCs through a foreign key |
| `users` | Dashboard user accounts with hashed passwords |
 
## Development Notes
- You must be in the `api/` directory with the virtual environment activated when trying to run Alembic migrations 
- The seed.py script populates the IoC table with randomized data from the Faker library which is used for building the frontend before the feed collector is working
- Windows environment was used for this project
