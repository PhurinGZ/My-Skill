# My-Skill

Personal collection of self-owned AI agent skills — only skills with no upstream source are vendored here. Skills installed from external repos (anthropics/skills, vercel-labs, obra/superpowers, etc.) can always be re-installed with `npx skills add`, so they are not kept in this repo.

## Skills

**Installed at** — **Global**: `~/.agents/skills/`, `~/.devin/skills/` (every project) · **Project**: `<project>/.devin/skills/`, `.agents/skills/`, `.qoder/skills/`, `.windsurf/skills/`

| Skill | Installed at | Description |
|---|---|---|
| `blackbox-web-pentest` | Project | Black-box (URL-only) security testing against a web app — 5 depth levels |
| `debug-and-test` | Project | Debug + test workflow |
| `elysiajs-performance-review` | Project | Audit ElysiaJS code for performance issues |
| `elysiajs-security` | Project | Audit ElysiaJS code for security vulnerabilities |
| `fastapi-performance` | Project | Diagnose/fix FastAPI perf: slow endpoints, latency, event-loop stalls |
| `fix-odoo-xml` | Project | Fix Odoo XML view warnings and layout issues |
| `fullstack` | Project | Full-stack guidance: React + Strapi v5 CMS + PostgreSQL |
| `human-ux-design` | Global + Project | Frontend interfaces indistinguishable from human-crafted design |
| `kb-article` | Global | Draft knowledge base articles from resolved issues or common questions |
| `mockup` | Project | Mockup generation |
| `nextjs-security-audit` | Project | Full-codebase security audit for Next.js (App/Pages Router) |
| `odoo-17` | Project | Odoo 17 dev best practices: model inheritance, view overrides, security |
| `odoo-cogmenu-export` | Project | Custom export actions in the Odoo cog menu + binary downloads |
| `odoo-fx-project` | Project | FX Project domain logic: models, calculations, state flow, permissions |
| `odoo-fx-project-reports` | Project | Fix/improve FX Project QWeb PDF reports (totals, table alignment) |
| `odoo18-report-skill` | Project | Create / customize / debug QWeb PDF reports in Odoo 18 |
| `project-tree` | Project | Project/directory tree generator พร้อมคำอธิบายแต่ละโฟลเดอร์ |
| `prompt-engineer` | Project | วิเคราะห์และปรับปรุง prompt ให้ชัดเจน ประหยัด token |
| `react-performance-optimization` | Project | Fix slow React apps: re-renders, bundles, janky lists |
| `ui-ux-design-guide` | Project | UI/UX design guidelines |
| `write-user-manual` | Global | End-user / admin manuals as MD / JSON / Word / PDF / HTML |

## Installed but not vendored (has upstream owner)

Re-installable via `npx skills add` / their source repo:

| Skill | Source |
|---|---|
| `agent-browser` | vercel-labs/agent-browser |
| `api-security-best-practices` | sickn33/antigravity-awesome-skills |
| `brainstorming`, `implementing-plans`, `writing-plans`, `test-driven-development`, `grill-me`, `improve-codebase-architecture` | obra/superpowers |
| `checklist-design` | Checklist Design (MIT) |
| `clean-code` | jackjin1997/ClawForge |
| `design-taste-frontend`, `high-end-visual-design` | Leonxlnx/taste-skill |
| `docx`, `pdf`, `xlsx`, `frontend-design`, `skill-creator` | anthropics/skills |
| `elysiajs` | elysiajs/skills |
| `fastapi` | fastapi/fastapi |
| `find-skills` | vercel-labs/skills |
| `hono-jsx` | honojs/skills |
| `impeccable` | pbakaus/impeccable |
| `nextjs-performance` | giuseppe-trisciuoglio/developer-kit |
| `odoo-skill` | qoder-odoo-skill |
| `playwright-best-practices` | currents-dev/playwright-best-practices-skill |
| `tdd` | mattpocock/skills |
| `vercel-react-best-practices` | vercel-labs/agent-skills |
| `vite` | antfu/skills |

## Devin Desktop built-in skills

Shipped with Devin Desktop — part of the app, not vendored:

`act-on-feedback`, `code-review`, `commit`, `create-draft-pr`, `create-pr`, `fix-ci`, `generate-run-commands`, `merge`, `sync`, `sync-upstream`, `troubleshoot`, `update-pr`, `update-skills`, plus `devin-cli`, `declarative-repo-setup`, `upload-secrets`
