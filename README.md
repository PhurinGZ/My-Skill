# My-Skill

Personal collection of self-owned AI agent skills. Only skills without an upstream source are vendored here. Skills installed from external repositories (such as `anthropics/skills`, `vercel-labs`, and `obra/superpowers`) can be re-installed with `npx skills add`, so they are not duplicated in this repository.

## Repository structure

Skills are grouped by their primary use case under `skills/<category>/<skill-name>/`. Each skill keeps its own `SKILL.md` and any supporting files (references, scripts, assets, agents, and examples) together.

```text
skills/
├── ai-and-prompting/
│   └── prompt-engineer/
├── backend-and-fullstack/
│   ├── fastapi-performance/
│   └── fullstack/
├── developer-tools/
│   └── project-tree/
├── documentation-and-writing/
│   ├── kb-article/
│   └── write-user-manual/
├── frontend-and-ui-ux/
│   ├── human-ux-design/
│   ├── react-performance-optimization/
│   └── ui-ux-design-guide/
├── odoo-and-erp/
│   ├── fix-odoo-xml/
│   ├── mockup/
│   ├── odoo-17/
│   ├── odoo-cogmenu-export/
│   ├── odoo-fx-project/
│   ├── odoo-fx-project-reports/
│   └── odoo18-report-skill/
├── security/
│   ├── blackbox-web-pentest/
│   └── nextjs-security-audit/
└── testing-and-debugging/
    └── debug-and-test/
```

## Skills catalog

**Installed at** — **Global**: `~/.agents/skills/`, `~/.devin/skills/` (available across projects) · **Project**: `<project>/.devin/skills/`, `.agents/skills/`, `.qoder/skills/`, `.windsurf/skills/`

### Security

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `blackbox-web-pentest` | `skills/security/blackbox-web-pentest` | Project | Black-box (URL-only) security testing against a web app — 5 depth levels |
| `nextjs-security-audit` | `skills/security/nextjs-security-audit` | Project | Full-codebase security audit for Next.js App Router and Pages Router |

### Testing and debugging

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `debug-and-test` | `skills/testing-and-debugging/debug-and-test` | Project | Systematic debugging, error analysis, and test-case development |

### Backend and full-stack development

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `fastapi-performance` | `skills/backend-and-fullstack/fastapi-performance` | Project | Diagnose and fix FastAPI performance problems |
| `fullstack-react-strapi` | `skills/backend-and-fullstack/fullstack` | Project | Full-stack guidance for React, Strapi v5, and PostgreSQL |

### Frontend and UI/UX

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `human-ux-design` | `skills/frontend-and-ui-ux/human-ux-design` | Global + Project | Design, build, and review high-quality frontend interfaces |
| `react-performance-optimization` | `skills/frontend-and-ui-ux/react-performance-optimization` | Project | Diagnose and improve React rendering, bundles, and loading performance |
| `ui-ux-design-guide` | `skills/frontend-and-ui-ux/ui-ux-design-guide` | Project | UI/UX design guidance for web and mobile products |

### Odoo and ERP

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `fix-odoo-xml` | `skills/odoo-and-erp/fix-odoo-xml` | Project | Fix Odoo 17 XML view warnings and layout issues |
| `mockup` | `skills/odoo-and-erp/mockup` | Project | Create interactive Odoo-style HTML mockups and ERP prototypes |
| `odoo-17` | `skills/odoo-and-erp/odoo-17` | Project | Odoo 17 development patterns, models, views, and security |
| `odoo-cogmenu-export` | `skills/odoo-and-erp/odoo-cogmenu-export` | Project | Add custom export and download actions to the Odoo cog menu |
| `odoo-fx-project-domain` | `skills/odoo-and-erp/odoo-fx-project` | Project | FX Project domain logic, calculations, state flow, and permissions |
| `odoo-fx-project-reports` | `skills/odoo-and-erp/odoo-fx-project-reports` | Project | Fix and improve FX Project QWeb PDF reports |
| `odoo18-report` | `skills/odoo-and-erp/odoo18-report-skill` | Project | Create, customize, and debug Odoo 18 QWeb PDF reports |

### Documentation and writing

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `kb-article` | `skills/documentation-and-writing/kb-article` | Global | Draft knowledge base articles from resolved issues or common questions |
| `write-user-manual` | `skills/documentation-and-writing/write-user-manual` | Global | Write end-user and admin manuals in Markdown, JSON, Word, PDF, or HTML |

### Developer tools

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `project-tree` | `skills/developer-tools/project-tree` | Project | Generate project and directory trees with explanations |

### AI and prompting

| Skill ID | Directory | Scope | Description |
|---|---|---|---|
| `prompt-engineer` | `skills/ai-and-prompting/prompt-engineer` | Project | Analyze and improve prompts for clarity, efficiency, and accuracy |

## Using the skills CLI

The repository uses the supported category layout, so skills can still be discovered by the Skills CLI.

```bash
# List skills available in this repository
npx skills add PhurinGZ/My-Skill --list

# Install one skill by its Skill ID
npx skills add PhurinGZ/My-Skill --skill fastapi-performance
```

## Installed but not vendored (has upstream owner)

Re-installable via `npx skills add` / their source repository:

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
| `elysiajs-performance-review`, `elysiajs-security` | (removed — has owner) |
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

`act-on-feedback`, `code-review`, `commit`, `create-draft-pr`, `create-pr`, `fix-ci`, `generate-run-commands`, `merge`, `sync`, `sync-upstream`, `troubleshoot`, `update-pr`, `update-skills`, plus `devin-cli`, `declarative-repo-setup`, `upload-secrets`.
