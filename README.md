# My-Skill

Personal collection of AI agent skills.

## Skills in this repo

| Skill | Description |
|---|---|
| `write-user-manual` | Write end-user / admin manuals (คู่มือการใช้งานระบบ) as Markdown, JSON (per-paragraph i18n th/en), Word/PDF, or HTML |
| `project-tree` | สร้างผังโครงสร้างโปรเจกต์ (directory tree) พร้อมคำอธิบายสั้นๆ ของแต่ละโฟลเดอร์/ไฟล์ |

## Global skills (all projects)

Installed under `~/.agents/skills/` (universal — shared by Amp, Cline, Codex, Cursor, etc.), `~/.devin/skills/` and `~/.config/devin/skills/`:

| Skill | Description |
|---|---|
| `agent-browser` | Browser automation CLI — navigate pages, fill forms, take screenshots, extract data |
| `brainstorming` | Sharpen ideas before any creative work — features, components, planning |
| `checklist-design` | Design audit / critique grounded in Checklist Design's published checklists |
| `clean-code` | Refactor working code per Robert C. Martin's Clean Code principles |
| `design-taste-frontend` | Anti-slop frontend skill — professional company/landing pages ([Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)) |
| `find-skills` | Discover and install agent skills ("how do I do X") |
| `frontend-design` | Distinctive, high-quality frontend interfaces — landing pages, dashboards, components |
| `grill-me` | A relentless interview to sharpen a plan or design |
| `human-ux-design` | Frontend interfaces indistinguishable from human-crafted design |
| `implementing-plans` | Execute an approved implementation plan task-by-task |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present a visual HTML report |
| `kb-article` | Draft knowledge base articles from resolved issues or common questions |
| `test-driven-development` | TDD — write failing tests before implementation code |
| `write-user-manual` | End-user / admin manuals as MD / JSON / Word / PDF / HTML |
| `writing-plans` | Turn specs / requirements into a multi-step implementation plan |

## Project-level skills

Per-project skills under `<project>/.devin/skills/`, `<project>/.agents/skills/` and `<project>/.qoder/skills/`. Skills already described in the global table are listed by name only.

### spintruck-erp (Odoo 18 ERP)

- `odoo-skill` — Odoo 18 CE development reference (models, views, XML, OWL, QWeb, security)
- `odoo18-report-skill` — Create / customize / debug QWeb PDF reports in Odoo 18
- `prompt-engineer` — วิเคราะห์และปรับปรุง prompt ให้ชัดเจน ประหยัด token
- `playwright-best-practices` — Playwright tests: POM, CI/CD, flaky-test fixes, auth, visual testing
- `docx` — Create / read / edit Word documents (.docx)
- `xlsx` — Create / edit / fix spreadsheets (.xlsx, .csv)
- `pdf` — Read, merge, split, fill, OCR PDF files
- `agent-browser`, `project-tree`, `skill-creator` (.qoder — create/improve skills)

### 27engineer (Odoo 17 FX Project)

- `odoo-17` — Odoo 17 dev best practices: model inheritance, view overrides, security
- `odoo-fx-project` — FX Project domain logic: models, calculations, state flow, permissions
- `odoo-fx-project-reports` — Fix/improve FX Project QWeb PDF reports (totals, table alignment)
- `odoo-cogmenu-export` — Custom export actions in the Odoo 17 cog menu + binary downloads
- `fix-odoo-xml` — Fix Odoo 17 XML view warnings and layout issues
- `debug-and-test` — Debug + test workflow
- `tdd` — Test-driven development (red-green-refactor)
- `agent-browser`, `brainstorming`, `find-skills`, `pdf`, `prompt-engineer`, `xlsx`, `skill-creator` (.qoder)

### cnx-exchange-1 (ElysiaJS / Next.js)

- `elysiajs` — Build backends with ElysiaJS (type-safe Bun framework)
- `elysiajs-performance-review` — Audit ElysiaJS code for performance issues
- `elysiajs-security` — Audit ElysiaJS code for security vulnerabilities
- `nextjs-performance` — Next.js optimization: Core Web Vitals, caching, streaming, bundles
- `nextjs-security-audit` — Full-codebase security audit for Next.js (App/Pages Router)
- `ui-ux-design-guide` — UI/UX design guidelines
- `docx`

### cnx-web-chat (Hono / Vite / React)

- `hono-jsx` — Server-rendered UI for Hono apps with hono/jsx (pages, layouts, forms)
- `vercel-react-best-practices` — React/Next.js performance guidelines from Vercel Engineering
- `vite` — Vite config, plugin API, SSR, Rolldown migration
- `api-security-best-practices` — Secure API design: authn/authz, validation, rate limiting
- `design-taste-frontend`, `project-tree`, `ui-ux-design-guide`

### tourism

- `fullstack` — Full-stack guidance: React + Strapi v5 CMS + PostgreSQL
- `impeccable` — Design/redesign/critique/polish frontend work
- `api-security-best-practices`, `docx`, `agent-browser`, `project-tree`, `react-performance-optimization`, `ui-ux-design-guide`

### wald (FastAPI backend)

- `blackbox-web-pentest` — Black-box (URL-only) security testing against a web app
- `fastapi` — FastAPI best practices: Pydantic models, dependencies, streaming
- `fastapi-performance` — Diagnose/fix FastAPI perf: slow endpoints, latency, event-loop stalls
- `high-end-visual-design` — High-end agency design: fonts, spacing, shadows, animations
- `agent-browser`, `api-security-best-practices`, `find-skills`, `project-tree`, `react-performance-optimization`, `ui-ux-design-guide`, `xlsx`

### mx-ai / mx-front (React + Strapi)

- `react-performance-optimization` — Fix slow React apps: re-renders, bundles, janky lists
- `agent-browser`, `project-tree`, `ui-ux-design-guide`

### mockup

- `mockup` (.windsurf — mockup generation)
- `frontend-design`, `human-ux-design`

### Others

- `wald-branch` — `ui-ux-design-guide`
- `Documents` — `xlsx`

## Devin Desktop built-in skills

Shipped with Devin Desktop (`/usr/share/devin-desktop/.../sessions/skills/`):

`act-on-feedback`, `code-review`, `commit`, `create-draft-pr`, `create-pr`, `fix-ci`, `generate-run-commands`, `merge`, `sync`, `sync-upstream`, `troubleshoot`, `update-pr`, `update-skills`

Plus built-in agent skills: `devin-cli` (Devin CLI docs), `declarative-repo-setup` (environment.yaml), `upload-secrets` (Devin Cloud secrets)

## Notes

- Skill files downloaded but not installed live in `~/Downloads/` (odoo-mockup, qoder-odoo-skill, skills-main collection, etc.)
- Package-bundled skills (e.g. `fastapi` inside site-packages/venvs, Playwright internals) are shipped with their packages, not installed agent skills
