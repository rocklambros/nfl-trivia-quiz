# Deployment & Operations Guide

**Version**: 1.0 (MVP)
**Target Audience**: DevOps engineers, system administrators
**Last Updated**: November 5, 2025

## Table of Contents
1. [Production Readiness Checklist](#production-readiness-checklist)
2. [Deployment Options](#deployment-options)
3. [Environment Configuration](#environment-configuration)
4. [WSGI Server Setup](#wsgi-server-setup)
5. [Reverse Proxy Configuration](#reverse-proxy-configuration)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)
9. [Scaling Strategies](#scaling-strategies)
10. [Troubleshooting](#troubleshooting)

---

## Production Readiness Checklist

### Pre-Deployment
- [ ] SECRET_KEY generated and stored securely
- [ ] Debug mode disabled (`FLASK_DEBUG=False`)
- [ ] Environment variables configured
- [ ] SSL/TLS certificates obtained
- [ ] WSGI server selected and configured
- [ ] Reverse proxy configured (Nginx/Apache)
- [ ] Firewall rules configured
- [ ] Logging configured
- [ ] Monitoring tools setup
- [ ] Backup strategy defined

### Security Checklist
- [ ] `SESSION_COOKIE_SECURE=True` enabled
- [ ] HTTPS enforced (no HTTP fallback)
- [ ] Security headers configured
- [ ] CORS policies defined (if needed)
- [ ] Rate limiting implemented
- [ ] Input validation tested
- [ ] Error pages don't expose internals
- [ ] Dependencies up to date

### Performance Checklist
- [ ] Static assets served efficiently
- [ ] Caching strategy implemented
- [ ] Database connection pooling (if added)
- [ ] Load testing completed
- [ ] CDN configured (optional)

---

## Deployment Options

### Option 1: Platform as a Service (PaaS)

#### Heroku
**Best for**: Quick deployment, MVP hosting

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or visit: https://devcenter.heroku.com/articles/heroku-cli

# Login and create app
heroku login
heroku create nfl-trivia-quiz

# Add Procfile
echo "web: gunicorn app:app" > Procfile

# Add runtime
echo "python-3.11.0" > runtime.txt

# Deploy
git push heroku main

# Set environment variables
heroku config:set SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set SESSION_COOKIE_SECURE=True
```

**Cost**: Free tier available, scales automatically

#### Railway.app
**Best for**: Modern PaaS, simple deployment

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and init
railway login
railway init

# Deploy
railway up

# Set environment variables
railway variables set SECRET_KEY=<generated-key>
```

**Cost**: $5/month starter, automatic scaling

#### Render
**Best for**: Free tier, easy setup

1. Connect GitHub repository
2. Create Web Service
3. Set environment: Python 3
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add environment variables

**Cost**: Free tier available (spins down after inactivity)

---

### Option 2: Virtual Private Server (VPS)

#### DigitalOcean Droplet / AWS EC2 / Linode

**Best for**: Full control, custom configuration

##### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application user
sudo useradd -m -s /bin/bash nflquiz
sudo su - nflquiz
```

##### Step 2: Application Setup
```bash
# Clone repository
cd /home/nflquiz
git clone https://github.com/rocklambros/nfl-trivia-quiz.git
cd nfl-trivia-quiz

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Test application
gunicorn --bind 0.0.0.0:8000 app:app
```

##### Step 3: Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/nflquiz.service
```

```ini
[Unit]
Description=NFL Trivia Quiz Application
After=network.target

[Service]
User=nflquiz
Group=nflquiz
WorkingDirectory=/home/nflquiz/nfl-trivia-quiz
Environment="PATH=/home/nflquiz/nfl-trivia-quiz/venv/bin"
Environment="SECRET_KEY=<your-secret-key>"
Environment="SESSION_COOKIE_SECURE=True"
ExecStart=/home/nflquiz/nfl-trivia-quiz/venv/bin/gunicorn --workers 3 --bind unix:nflquiz.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable nflquiz
sudo systemctl start nflquiz
sudo systemctl status nflquiz
```

**Cost**: $5-20/month depending on provider and specs

---

### Option 3: Container Deployment (Docker)

**Best for**: Consistent environments, Kubernetes deployment

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app:app"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - SESSION_COOKIE_SECURE=True
      - FLASK_ENV=production
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

#### Build and Run
```bash
# Build image
docker build -t nfl-trivia-quiz:latest .

# Run container
docker run -d -p 8000:8000 \
  -e SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))') \
  -e SESSION_COOKIE_SECURE=True \
  --name nflquiz \
  nfl-trivia-quiz:latest

# Or use Docker Compose
docker-compose up -d
```

**Cost**: Depends on hosting platform (AWS ECS, Azure Container Instances, etc.)

---

## Environment Configuration

### Production Environment Variables

Create `.env.production`:
```bash
# Application
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=8000

# Security
SECRET_KEY=<generated-64-char-hex-key>
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/nflquiz/app.log
```

### Generate Secure SECRET_KEY
```bash
python3 -c 'import secrets; print(secrets.token_hex(32))'
```

**Store securely**:
- Use environment variables (not in code)
- Use secrets management (AWS Secrets Manager, HashiCorp Vault)
- Never commit to version control

### Load Environment Variables
```python
# app.py
import os
from dotenv import load_dotenv

# Load .env file (development)
load_dotenv()

# Production: use actual environment variables
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True',
    # ... other config
)
```

---

## WSGI Server Setup

### Option 1: Gunicorn (Recommended)

**Installation**:
```bash
pip install gunicorn
```

**Basic Configuration**:
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

**Production Configuration** (`gunicorn_config.py`):
```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '/var/log/nflquiz/access.log'
errorlog = '/var/log/nflquiz/error.log'
loglevel = 'info'

# Process naming
proc_name = 'nfl-trivia-quiz'

# Server mechanics
daemon = False
pidfile = '/var/run/nflquiz.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if not using reverse proxy)
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'
```

**Run with config**:
```bash
gunicorn -c gunicorn_config.py app:app
```

---

### Option 2: uWSGI

**Installation**:
```bash
pip install uwsgi
```

**Configuration** (`uwsgi.ini`):
```ini
[uwsgi]
module = app:app
master = true
processes = 4
threads = 2
socket = /tmp/nflquiz.sock
chmod-socket = 660
vacuum = true
die-on-term = true
logto = /var/log/nflquiz/uwsgi.log
```

**Run**:
```bash
uwsgi --ini uwsgi.ini
```

---

## Reverse Proxy Configuration

### Nginx (Recommended)

**Configuration** (`/etc/nginx/sites-available/nflquiz`):
```nginx
upstream nflquiz_app {
    server unix:/tmp/nflquiz.sock fail_timeout=0;
}

server {
    listen 80;
    server_name nflquiz.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name nflquiz.example.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/nflquiz.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nflquiz.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Logging
    access_log /var/log/nginx/nflquiz_access.log;
    error_log /var/log/nginx/nflquiz_error.log;

    # Static files
    location /static {
        alias /home/nflquiz/nfl-trivia-quiz/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Application
    location / {
        proxy_pass http://nflquiz_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "OK";
        add_header Content-Type text/plain;
    }
}
```

**Enable site**:
```bash
sudo ln -s /etc/nginx/sites-available/nflquiz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache (Alternative)

**Configuration** (`/etc/apache2/sites-available/nflquiz.conf`):
```apache
<VirtualHost *:80>
    ServerName nflquiz.example.com
    Redirect permanent / https://nflquiz.example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName nflquiz.example.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/nflquiz.example.com/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/nflquiz.example.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/nflquiz.example.com/chain.pem

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "DENY"

    # Static files
    Alias /static /home/nflquiz/nfl-trivia-quiz/static
    <Directory /home/nflquiz/nfl-trivia-quiz/static>
        Require all granted
    </Directory>

    # Proxy to Gunicorn
    ProxyPreserveHost On
    ProxyPass /static !
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

---

## SSL/TLS Setup

### Let's Encrypt (Free SSL)

**Install Certbot**:
```bash
sudo apt install certbot python3-certbot-nginx
```

**Obtain Certificate**:
```bash
sudo certbot --nginx -d nflquiz.example.com
```

**Auto-Renewal**:
```bash
# Test renewal
sudo certbot renew --dry-run

# Cron job (already added by certbot)
0 0,12 * * * root certbot renew --quiet
```

---

## Monitoring & Logging

### Application Logging

**Configuration** (`app.py`):
```python
import logging
from logging.handlers import RotatingFileHandler

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure logging
handler = RotatingFileHandler(
    'logs/nflquiz.log',
    maxBytes=10000000,  # 10MB
    backupCount=10
)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
```

### System Monitoring

#### Prometheus + Grafana
```python
# Install prometheus-flask-exporter
pip install prometheus-flask-exporter

# Add to app.py
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
```

#### Application Monitoring Tools
- **New Relic**: Full-stack monitoring
- **Datadog**: Infrastructure and application monitoring
- **Sentry**: Error tracking and performance monitoring

### Health Checks

**Add health endpoint** (`app.py`):
```python
@app.route('/health')
def health():
    """Health check endpoint for load balancers"""
    return {'status': 'healthy', 'timestamp': time.time()}, 200
```

---

## Backup & Recovery

### MVP Scope (No Database)
- Backup application code (git repository)
- Backup configuration files
- Backup SSL certificates
- Backup logs (optional)

### Future (With Database)
```bash
# PostgreSQL backup
pg_dump nflquiz > backup_$(date +%Y%m%d).sql

# Automated backups
0 2 * * * pg_dump nflquiz | gzip > /backups/nflquiz_$(date +\%Y\%m\%d).sql.gz
```

---

## Scaling Strategies

### Vertical Scaling
- Increase CPU/RAM on server
- Optimize worker count
- Increase database connections (when added)

### Horizontal Scaling
- Load balancer (Nginx, HAProxy, AWS ELB)
- Multiple application servers
- Session store (Redis for shared sessions)
- Database replication (when added)

### Example Load Balancer Config
```nginx
upstream nflquiz_cluster {
    least_conn;
    server app1.internal:8000 weight=1;
    server app2.internal:8000 weight=1;
    server app3.internal:8000 weight=1;
}

server {
    listen 443 ssl;
    server_name nflquiz.example.com;

    location / {
        proxy_pass http://nflquiz_cluster;
        # ... other config
    }
}
```

---

## Troubleshooting

### Application Won't Start
```bash
# Check logs
sudo journalctl -u nflquiz -n 50 --no-pager

# Check Gunicorn
gunicorn --check-config app:app

# Test Python syntax
python3 -m py_compile app.py
```

### High Memory Usage
```bash
# Check process memory
ps aux | grep gunicorn

# Reduce workers
gunicorn --workers 2 app:app

# Monitor with htop
htop
```

### Slow Response Times
```bash
# Check Nginx access log
tail -f /var/log/nginx/nflquiz_access.log

# Profile application
pip install flask-profiler
# Add profiling to app
```

---

## Maintenance Tasks

### Regular Tasks
- [ ] Weekly: Review logs for errors
- [ ] Weekly: Check SSL certificate expiry
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review security advisories
- [ ] Quarterly: Load testing
- [ ] Annually: SSL certificate renewal (automated with Let's Encrypt)

### Update Procedure
```bash
# 1. Backup current version
git tag -a v1.0.0 -m "Production backup"

# 2. Pull updates
git pull origin main

# 3. Update dependencies
pip install -r requirements.txt

# 4. Test locally
python3 app.py

# 5. Restart service
sudo systemctl restart nflquiz

# 6. Monitor logs
sudo journalctl -u nflquiz -f
```

---

## Support & Resources

- **Documentation**: See README.md, DEVELOPER_GUIDE.md, API_REFERENCE.md
- **GitHub Issues**: https://github.com/rocklambros/nfl-trivia-quiz/issues
- **Flask Deployment**: https://flask.palletsprojects.com/en/2.3.x/deploying/
- **Gunicorn Docs**: https://docs.gunicorn.org/

---

**Document Version**: 1.0
**Last Updated**: November 5, 2025
**Maintained By**: Operations Team
