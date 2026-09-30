# Stage 1: Build Next.js Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
# Ensure public directory exists even if not committed with files
RUN mkdir -p /app/frontend/public
RUN npm run build

# Stage 2: Production Unified Full-Stack Runner
FROM python:3.12-slim AS runner

WORKDIR /app

# Install Node.js runtime and curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy Backend Application & Database
COPY backend ./backend
ENV PYTHONPATH=/app/backend

# Pre-create frontend directory
RUN mkdir -p /app/frontend/public

# Copy Built Next.js Frontend Assets
COPY --from=frontend-builder /app/frontend/package*.json ./frontend/
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public* ./frontend/public/
COPY --from=frontend-builder /app/frontend/node_modules ./frontend/node_modules
COPY --from=frontend-builder /app/frontend/next.config.mjs ./frontend/

# Copy Entrypoint
COPY entrypoint.sh ./entrypoint.sh
RUN sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh

# Default port for Render (Render dynamically sets $PORT)
ENV PORT=10000
EXPOSE 10000

CMD ["/bin/sh", "/app/entrypoint.sh"]
