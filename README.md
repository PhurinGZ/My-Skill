# My-Skill

Personal collection of AI agent skills — every installed skill on the machine is vendored in this repo.

## Skills

**Installed at** — **Global**: `~/.agents/skills/`, `~/.devin/skills/`, `~/.config/devin/skills/` (available in every project) · **Project**: `<project>/.devin/skills/`, `.agents/skills/`, `.qoder/skills/`, `.windsurf/skills/`

| Skill | Installed at | Description |
|---|---|---|
| `agent-browser` | Global + Project | Browser automation CLI — navigate pages, fill forms, take screenshots, extract data |
| `api-security-best-practices` | Project | Secure API design: authn/authz, input validation, rate limiting |
| `blackbox-web-pentest` | Project | Black-box (URL-only) security testing against a web app |
| `brainstorming` | Global + Project | Sharpen ideas before any creative work — features, components, planning |
| `checklist-design` | Global | Design audit / critique grounded in Checklist Design's published checklists |
| `clean-code` | Global | Refactor working code per Robert C. Martin's Clean Code principles |
| `debug-and-test` | Project | Debug + test workflow |
| `design-taste-frontend` | Global + Project | Anti-slop frontend skill — professional company/landing pages ([Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)) |
| `docx` | Project | Create / read / edit Word documents (.docx) |
| `elysiajs` | Project | Build backends with ElysiaJS (type-safe Bun framework) |
| `elysiajs-performance-review` | Project | Audit ElysiaJS code for performance issues |
| `elysiajs-security` | Project | Audit ElysiaJS code for security vulnerabilities |
| `fastapi` | Project | FastAPI best practices: Pydantic models, dependencies, streaming |
| `fastapi-performance` | Project | Diagnose/fix FastAPI perf: slow endpoints, latency, event-loop stalls |
| `find-skills` | Global + Project | Discover and install agent skills ("how do I do X") |
| `fix-odoo-xml` | Project | Fix Odoo XML view warnings and layout issues |
| `frontend-design` | Global + Project | Distinctive, high-quality frontend interfaces — landing pages, dashboards, components |
| `fullstack` | Project | Full-stack guidance: React + Strapi v5 CMS + PostgreSQL |
| `grill-me` | Global | A relentless interview to sharpen a plan or design |
| `high-end-visual-design` | Project | High-end agency design: fonts, spacing, shadows, animations |
| `hono-jsx` | Project | Server-rendered UI for Hono apps with hono/jsx (pages, layouts, forms) |
| `human-ux-design` | Global + Project | Frontend interfaces indistinguishable from human-crafted design |
| `impeccable` | Project | Design / redesign / critique / polish frontend work |
| `implementing-plans` | Global | Execute an approved implementation plan task-by-task |
| `improve-codebase-architecture` | Global | Scan a codebase for deepening opportunities, present a visual HTML report |
| `kb-article` | Global | Draft knowledge base articles from resolved issues or common questions |
| `mockup` | Project | Mockup generation |
| `nextjs-performance` | Project | Next.js optimization: Core Web Vitals, caching, streaming, bundles |
| `nextjs-security-audit` | Project | Full-codebase security audit for Next.js (App/Pages Router) |
| `odoo-17` | Project | Odoo 17 dev best practices: model inheritance, view overrides, security |
| `odoo-cogmenu-export` | Project | Custom export actions in the Odoo cog menu + binary downloads |
| `odoo-fx-project` | Project | FX Project domain logic: models, calculations, state flow, permissions |
| `odoo-fx-project-reports` | Project | Fix/improve FX Project QWeb PDF reports (totals, table alignment) |
| `odoo-skill` | Project | Odoo 18 CE development reference (models, views, XML, OWL, QWeb, security) |
| `odoo18-report-skill` | Project | Create / customize / debug QWeb PDF reports in Odoo 18 |
| `pdf` | Project | Read, merge, split, fill, OCR PDF files |
| `playwright-best-practices` | Project | Playwright tests: POM, CI/CD, flaky-test fixes, auth, visual testing |
| `project-tree` | Project | Project/directory tree generator พร้อมคำอธิบายแต่ละโฟลเดอร์ |
| `prompt-engineer` | Project | วิเคราะห์และปรับปรุง prompt ให้ชัดเจน ประหยัด token |
| `react-performance-optimization` | Project | Fix slow React apps: re-renders, bundles, janky lists |
| `skill-creator` | Project | Create new skills, modify and improve existing skills |
| `tdd` | Project | Test-driven development (red-green-refactor) |
| `test-driven-development` | Global | TDD — write failing tests before implementation code |
| `ui-ux-design-guide` | Project | UI/UX design guidelines |
| `vercel-react-best-practices` | Project | React/Next.js performance guidelines from Vercel Engineering |
| `vite` | Project | Vite config, plugin API, SSR, Rolldown migration |
| `write-user-manual` | Global | End-user / admin manuals as MD / JSON / Word / PDF / HTML |
| `writing-plans` | Global | Turn specs / requirements into a multi-step implementation plan |
| `xlsx` | Project | Create / edit / fix spreadsheets (.xlsx, .csv) |

## Devin Desktop built-in skills

Shipped with Devin Desktop (`/usr/share/devin-desktop/.../sessions/skills/`) — part of the app, not vendored here:

`act-on-feedback`, `code-review`, `commit`, `create-draft-pr`, `create-pr`, `fix-ci`, `generate-run-commands`, `merge`, `sync`, `sync-upstream`, `troubleshoot`, `update-pr`, `update-skills`

Plus built-in agent skills: `devin-cli` (Devin CLI docs), `declarative-repo-setup` (environment.yaml), `upload-secrets` (Devin Cloud secrets)

## Notes

- Skill files downloaded but not installed live in `~/Downloads/` (odoo-mockup, qoder-odoo-skill, skills-main collection, etc.)
- Package-bundled skills (e.g. `fastapi` inside site-packages/venvs, Playwright internals) are shipped with their packages, not installed agent skills
