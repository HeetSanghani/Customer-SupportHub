# 06 — Production Environment Strategy

- Template: `supporthub/backend/.env.production.example`
- Database URL: Uses container service names (`db:5432`, `mysql:3306`, `redis:6379`).
- Secrets Injection: Environment variables injected at container runtime; zero hardcoded secrets in built images.
