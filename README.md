# DevOps Practice

DevOps learning repository: infrastructure configs, automation scripts, and tooling examples.

Applications have been moved to separate repositories for cleaner CI/CD and independent deployment.

## Structure

```
My-Devops-Practice/
├── infra/       infrastructure configs (Docker, Compose, Ansible)
└── tools/       bash scripts for administration
```

## Related Projects

Each application lives in its own repository:

| Repository | Stack | Description |
|-----------|-------|-------------|
| [wordbook](https://github.com/khalikov-ibragim/wordbook) | Node.js, PostgreSQL, LibreTranslate, Cloudflare | PWA dictionary (EN↔RU) with offline support |
| [site_the_sales](https://github.com/khalikov-ibragim/site_the_sales) | FastAPI, PostgreSQL, Nginx | E-commerce store |
| [chat-messenger](https://github.com/khalikov-ibragim/chat-messenger) | Socket.IO, Redis, PostgreSQL | Real-time chat |
| [file-gallery](https://github.com/khalikov-ibragim/file-gallery) | MinIO S3, PostgreSQL | File storage gallery |
| [api-parser](https://github.com/khalikov-ibragim/api-parser) | Python, requests | API to CSV parser |

## Infrastructure (infra/)

- `docker/` — Dockerfile examples
- `docker-compose/` — Compose file examples
- `ansible/` — playbooks (growing)

## Scripts (tools/)

- `backup.sh` — simple backup script with rotation
- `Nginx_Logs.sh` — nginx log analysis

## Roadmap

- [ ] CI/CD (GitHub Actions): image build on push, deployment
- [ ] Fill `infra/ansible` with first playbooks
- [ ] Monitoring (Prometheus + Grafana)
