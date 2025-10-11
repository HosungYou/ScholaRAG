# Deployment Guide

## Option 1: Local Deployment (Easiest)

Perfect for individual researchers or testing.

### Prerequisites
- Python 3.9+
- 8GB+ RAM recommended
- Anthropic API key

### Steps

```bash
# 1. Clone repository
git clone https://github.com/HosungYou/researcherRAG.git
cd researcherRAG/01_literature_review_rag

# 2. Run setup script
./setup.sh

# 3. Add API key
nano .env
# Add: ANTHROPIC_API_KEY=your_key_here

# 4. Test the system
python test_system.py

# 5. Run application
python app.py
```

Open browser: http://localhost:7860

---

## Option 2: Hugging Face Spaces (Public Demo)

Perfect for sharing with colleagues or workshop participants.

### Prerequisites
- Hugging Face account
- Anthropic API key

### Steps

#### A. Via Web Interface (No Command Line)

1. **Create Space**
   - Go to: https://huggingface.co/new-space
   - Name: `researcherrag-demo`
   - License: MIT
   - SDK: Gradio
   - Hardware: CPU basic (free)

2. **Upload Files**
   - Upload all files from `01_literature_review_rag/`
   - Make sure to include:
     - `app.py`
     - `requirements.txt`
     - `backend/` folder with all modules

3. **Add Secrets**
   - Go to Space Settings → Repository secrets
   - Add secret:
     - Name: `ANTHROPIC_API_KEY`
     - Value: `your-api-key-here`

4. **Create .env file**
   - In Space, create new file `.env`
   - Add (using the secret):
     ```
     ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
     ```

5. **Wait for Build**
   - HF Spaces will automatically build
   - Takes 5-10 minutes first time
   - Watch logs for errors

6. **Access Your Demo**
   - URL: `https://huggingface.co/spaces/your-username/researcherrag-demo`
   - Share this URL with anyone!

#### B. Via Git (Advanced)

```bash
# 1. Create space and clone
git clone https://huggingface.co/spaces/your-username/researcherrag-demo
cd researcherrag-demo

# 2. Copy files
cp -r ../researcherRAG/01_literature_review_rag/* .

# 3. Commit and push
git add .
git commit -m "Deploy Literature Review RAG"
git push
```

### Configuration for HF Spaces

Create `README.md` in root (HF Spaces header):

```yaml
---
title: ResearcherRAG Literature Review
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# ResearcherRAG: Literature Review Assistant

AI-powered literature synthesis for researchers.

[Documentation](https://github.com/HosungYou/researcherRAG)
```

---

## Option 3: University/Lab Server

Perfect for research teams with shared access.

### Prerequisites
- Linux server with sudo access
- 16GB+ RAM recommended
- Docker (optional but recommended)

### Method A: Direct Installation

```bash
# On server
ssh user@your-server.edu

# Clone repository
git clone https://github.com/HosungYou/researcherRAG.git
cd researcherRAG/01_literature_review_rag

# Run setup
./setup.sh

# Add API key
nano .env

# Run with nohup (keeps running after logout)
nohup python app.py > app.log 2>&1 &

# Check logs
tail -f app.log
```

Access: `http://your-server.edu:7860`

### Method B: Docker (Recommended)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 7860

# Run
CMD ["python", "app.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  researcherrag:
    build: .
    container_name: researcherrag-lit-review
    ports:
      - "7860:7860"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

Deploy:

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Setting up Nginx (Public Access)

```nginx
# /etc/nginx/sites-available/researcherrag
server {
    listen 80;
    server_name researcherrag.your-university.edu;

    location / {
        proxy_pass http://localhost:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/researcherrag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Option 4: Cloud Platforms

### AWS EC2

1. Launch EC2 instance (t3.medium or larger)
2. SSH into instance
3. Follow "University Server" instructions above
4. Configure security group to allow port 7860

### Google Cloud Run

Create `cloudbuild.yaml`:

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/researcherrag', '.']
images:
  - 'gcr.io/$PROJECT_ID/researcherrag'
```

Deploy:

```bash
gcloud run deploy researcherrag \
  --image gcr.io/PROJECT_ID/researcherrag \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your-key
```

---

## Configuration Options

### Environment Variables

All configurable via `.env`:

```bash
# LLM Configuration
ANTHROPIC_API_KEY=your_key
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.3

# Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# Gradio Settings
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=False  # Set to True for temporary public URL
```

### Using Different LLM Providers

#### OpenAI

```bash
# In .env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
LLM_MODEL=gpt-4-turbo-preview
```

#### Local Model (Ollama)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3

# Update backend/core/rag_graph.py:
# Replace get_llm() function with:
from langchain_community.llms import Ollama

def get_llm():
    return Ollama(model="llama3")
```

---

## Monitoring & Maintenance

### Check System Health

```bash
# Local
python test_system.py

# Docker
docker-compose exec researcherrag python test_system.py
```

### View Logs

```bash
# Local with nohup
tail -f app.log

# Docker
docker-compose logs -f researcherrag

# Gradio built-in logs
# Check terminal output when running app.py
```

### Database Backup

```bash
# Backup ChromaDB
tar -czf vector_db_backup_$(date +%Y%m%d).tar.gz data/vector_db

# Restore
tar -xzf vector_db_backup_YYYYMMDD.tar.gz
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Reinstall dependencies (if requirements changed)
pip install -r requirements.txt

# Restart
# For nohup:
pkill -f app.py
nohup python app.py > app.log 2>&1 &

# For Docker:
docker-compose down
docker-compose build
docker-compose up -d
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :7860

# Kill process
kill -9 PID

# Or change port in .env
GRADIO_SERVER_PORT=7861
```

### Out of Memory

```bash
# Reduce chunk size
CHUNK_SIZE=500

# Or upgrade instance
# AWS: t3.medium → t3.large
# HF Spaces: CPU basic → CPU upgrade ($9/month)
```

### Slow Performance

1. **Use GPU** (HF Spaces: upgrade to T4 GPU)
2. **Reduce documents**: Query fewer papers
3. **Optimize retrieval**: Lower `TOP_K_RESULTS`

### API Rate Limits

```bash
# Add delay between requests
# Edit backend/core/rag_graph.py
import time
time.sleep(1)  # Add after LLM calls
```

---

## Security Best Practices

### For Public Deployment

1. **Environment Variables**: Never commit `.env` to Git
2. **API Keys**: Use secrets management (HF Spaces secrets, AWS Secrets Manager)
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Authentication**: Add basic auth for Gradio

Example basic auth:

```python
# In app.py
demo.launch(
    auth=("username", "password"),  # Add this line
    server_name="0.0.0.0",
    server_port=7860
)
```

### For Sensitive Data

1. **Use local deployment** (not cloud)
2. **Enable firewall** (restrict access to campus network)
3. **Use VPN** for remote access
4. **Encrypt data at rest**

---

## Cost Estimation

### Local Deployment
- Infrastructure: $0 (use own computer)
- API costs: ~$5-10/month (light use)

### HF Spaces
- CPU Basic: Free
- CPU Upgrade: $9/month (more RAM)
- API costs: ~$10-20/month (moderate use)

### AWS EC2
- t3.medium: ~$30/month
- API costs: ~$20-50/month (heavy use)
- **Total**: ~$50-80/month

### University Server
- Infrastructure: Usually free
- API costs: ~$50-100/month (team use)

---

## Getting Help

- **Documentation**: [Main docs](https://github.com/HosungYou/researcherRAG)
- **Issues**: [Report bugs](https://github.com/HosungYou/researcherRAG/issues)
- **Examples**: See `docs/` folder

---

**Choose the deployment method that fits your needs and budget!**

For workshops: HF Spaces (easy to share)
For personal use: Local (free, private)
For teams: University server (shared access)
