# Deployment Patterns

## Railway (Recommended for solo/small teams)

1. Provision a **PostgreSQL** plugin — Railway injects `DATABASE_URL` automatically
2. Create a **Strapi service** from your `backend/` directory
3. Set env vars (see checklist below)
4. Set `DATABASE_URL` from Railway's Postgres plugin reference variable
5. Build: `npm run build`, Start: `npm run start`

For the React frontend: deploy to **Vercel** or **Netlify** — set `VITE_STRAPI_URL` to your Railway Strapi public URL.

**Railway tips:**
- Use Railway's private networking for Strapi ↔ Postgres (zero egress cost)
- Set `NODE_ENV=production` — Strapi disables admin registration in production
- Enable Railway's health checks on `/api/health` (Strapi v5 built-in)

---

## Render

Similar to Railway. Use Render's managed PostgreSQL:

```yaml
# render.yaml
services:
  - type: web
    name: strapi
    env: node
    buildCommand: cd backend && npm install && npm run build
    startCommand: cd backend && npm run start
    healthCheckPath: /api/health
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: strapi-db
          property: connectionString

databases:
  - name: strapi-db
    plan: starter
```

---

## VPS (Ubuntu 22.04 + PM2 + Nginx + SSL)

### 1. Install dependencies

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs postgresql nginx certbot python3-certbot-nginx
npm install -g pm2
```

### 2. Database setup

```bash
sudo -u postgres psql
CREATE DATABASE strapi;
CREATE USER strapi WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE strapi TO strapi;
\q
```

### 3. Build & start Strapi

```bash
cd /var/www/backend
npm install && npm run build

# ecosystem.config.js
module.exports = {
  apps: [{
    name: "strapi",
    script: "npm",
    args: "start",
    cwd: "/var/www/backend",
    env: { NODE_ENV: "production" }
  }]
};

pm2 start ecosystem.config.js
pm2 save && pm2 startup
```

### 4. Nginx config

```nginx
server {
  listen 80;
  server_name api.yourdomain.com;

  location / {
    proxy_pass http://localhost:1337;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;
    client_max_body_size 100M;  # for file uploads
  }
}

server {
  listen 80;
  server_name yourdomain.com;

  location / {
    root /var/www/frontend/dist;
    try_files $uri $uri/ /index.html;
  }
}
```

### 5. SSL with Certbot

```bash
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
sudo systemctl reload nginx
```

---

## Docker Compose (Production)

```yaml
# docker-compose.prod.yml
services:
  postgres:
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_DB: ${DATABASE_NAME}
      POSTGRES_USER: ${DATABASE_USERNAME}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DATABASE_USERNAME}"]
      interval: 10s
      retries: 5

  strapi:
    image: yourregistry/strapi:latest
    restart: always
    env_file: .env.production
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - uploads:/app/public/uploads   # persist media uploads

  nginx:
    image: nginx:alpine
    restart: always
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./frontend/dist:/var/www/html:ro
      - certbot-certs:/etc/letsencrypt:ro

volumes:
  pgdata:
  uploads:
  certbot-certs:
```

---

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-strapi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: cd backend && npm ci && npm run build
      - name: Deploy to Railway
        run: npx @railway/cli up --service strapi
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: cd frontend && npm ci && npm run build
        env:
          VITE_STRAPI_URL: ${{ secrets.VITE_STRAPI_URL }}
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: frontend
```

---

## Environment Variables Checklist (Production Strapi)

| Variable | How to generate |
|---|---|
| `NODE_ENV` | `production` |
| `HOST` | `0.0.0.0` |
| `PORT` | `1337` |
| `DATABASE_URL` | From Postgres service, or use individual `DATABASE_*` vars |
| `APP_KEYS` | `openssl rand -base64 32` × 4, comma-separated |
| `API_TOKEN_SALT` | `openssl rand -base64 32` |
| `ADMIN_JWT_SECRET` | `openssl rand -base64 32` |
| `JWT_SECRET` | `openssl rand -base64 32` |
| `TRANSFER_TOKEN_SALT` | `openssl rand -base64 32` |
| `STRAPI_ADMIN_EMAIL` | seed admin email |
| `STRAPI_ADMIN_PASSWORD` | seed admin password (min 8 chars, 1 upper, 1 number) |

---

## Backups

### Automated PostgreSQL backup script

```bash
#!/bin/bash
# backup-db.sh — run via cron: 0 2 * * * /path/to/backup-db.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/postgres"
mkdir -p "$BACKUP_DIR"

pg_dump -U strapi -h localhost strapi | gzip > "$BACKUP_DIR/strapi_$TIMESTAMP.sql.gz"

# Keep last 30 days only
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete

# Optional: sync to S3
# aws s3 cp "$BACKUP_DIR/strapi_$TIMESTAMP.sql.gz" s3://your-bucket/db-backups/
```

### Media upload backup

Strapi stores uploads in `public/uploads/`. Sync to object storage in production:

```bash
# Option 1: Use Strapi's AWS S3 or Cloudinary upload provider
npm install @strapi/provider-upload-aws-s3

# config/plugins.ts
export default ({ env }) => ({
  upload: {
    config: {
      provider: "aws-s3",
      providerOptions: {
        s3Options: {
          region: env("AWS_REGION"),
          params: { Bucket: env("AWS_BUCKET") },
        },
      },
    },
  },
});
```

---

## Health Check & Monitoring

Strapi v5 exposes `GET /api/health` → `{ status: "UP" }`.

Use with uptime monitors (Better Uptime, UptimeRobot) and container health checks.

```bash
# Quick sanity check after deploy
curl https://api.yourdomain.com/api/health
# Expected: {"status":"UP"}
```
