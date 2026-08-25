# 03 — Frontend Container Specifications

- **Dockerfile**: `supporthub/frontend/Dockerfile`
- **Multi-Stage Build**:
  - Stage 1: `node:20-alpine`, `npm ci`, `npm run build` generates static assets in `dist/`.
  - Stage 2: `nginx:alpine` serves static SPA bundle on port `80`.
