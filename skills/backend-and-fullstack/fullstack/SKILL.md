---
name: fullstack-react-strapi
author: PhurinGZ
description: Expert-level guidance for building full-stack applications with React.js (frontend), Strapi v5 CMS (backend/API), and PostgreSQL (database), using Tailwind CSS + shadcn/ui as the design system. Use this skill whenever the user mentions React + Strapi, asks to scaffold a full-stack project, wants to set up a CMS-backed React app, needs architecture advice for a headless CMS setup, asks about content types, API integration, auth, roles/permissions, file uploads, webhooks, i18n, caching, testing, or deployment for this stack. Trigger even if the user only mentions one part of the stack (e.g. "set up Strapi with Postgres", "React Query with Strapi", "deploy Strapi to Railway") — assume the full-stack context unless told otherwise. Also trigger for questions about Strapi plugins, middleware, lifecycle hooks, custom controllers, RBAC, or any Strapi-specific configuration.
---

# Full-Stack React + Strapi v5 + PostgreSQL Expert

You are an expert full-stack architect specializing in:
- **React.js** (Vite, hooks, context, React Query v5, Zustand)
- **Strapi v5** (Document Service, content types, plugins, custom routes, lifecycle hooks, RBAC, webhooks, i18n, media library)
- **PostgreSQL** (schema design, relations, Strapi-managed migrations)
- **Tailwind CSS + shadcn/ui** (component-driven UI, design tokens, cva)

Always produce production-grade, opinionated output. Skip beginner explanations unless asked.

---

## Project Architecture

### Recommended Monorepo Layout

```
project-root/
├── frontend/          # React app (Vite + TypeScript)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/         # shadcn/ui base components
│   │   │   └── [feature]/  # feature-specific components
│   │   ├── pages/          # Route-level components
│   │   ├── hooks/          # Custom React hooks (data fetching)
│   │   ├── lib/            # API client, utils, constants, queryClient
│   │   ├── stores/         # Zustand stores
│   │   └── types/          # TypeScript types (mirror Strapi schemas)
│   ├── tailwind.config.ts
│   └── vite.config.ts
├── backend/           # Strapi v5 app
│   ├── src/
│   │   ├── api/            # Content types (schema + controllers + routes + services)
│   │   ├── components/     # Strapi reusable field-group components
│   │   ├── extensions/     # Plugin overrides (users-permissions, etc.)
│   │   └── middlewares/    # Custom middlewares
│   ├── config/
│   │   ├── database.ts     # PostgreSQL config
│   │   ├── server.ts       # Host, port, proxy config
│   │   ├── plugins.ts      # Plugin registration + config
│   │   └── middlewares.ts  # Middleware stack
│   └── types/
│       └── generated/      # Auto-generated Strapi types
├── docker-compose.yml
└── .env.example
```

---

## Environment Setup

```bash
# .env.example (backend)
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=strapi
DATABASE_USERNAME=strapi
DATABASE_PASSWORD=strapi
DATABASE_SSL=false

APP_KEYS=key1,key2,key3,key4    # openssl rand -base64 32 × 4
API_TOKEN_SALT=                  # openssl rand -base64 32
ADMIN_JWT_SECRET=                # openssl rand -base64 32
JWT_SECRET=                      # openssl rand -base64 32
TRANSFER_TOKEN_SALT=             # openssl rand -base64 32

NODE_ENV=development
HOST=0.0.0.0
PORT=1337
```

```bash
# .env.example (frontend)
VITE_STRAPI_URL=http://localhost:1337
VITE_STRAPI_API_TOKEN=           # optional: public read-only token
```

---

## Strapi Setup

### PostgreSQL config (`backend/config/database.ts`)

```ts
export default ({ env }) => ({
  connection: {
    client: "postgres",
    connection: {
      host: env("DATABASE_HOST", "127.0.0.1"),
      port: env.int("DATABASE_PORT", 5432),
      database: env("DATABASE_NAME", "strapi"),
      user: env("DATABASE_USERNAME", "strapi"),
      password: env("DATABASE_PASSWORD", ""),
      ssl: env.bool("DATABASE_SSL", false)
        ? { rejectUnauthorized: env.bool("DATABASE_SSL_REJECT_UNAUTHORIZED", true) }
        : false,
    },
    pool: { min: 2, max: 10 },
    acquireConnectionTimeout: 60000,
  },
});
```

### Content Type Best Practices

- Define all relations explicitly — avoid implicit many-to-many unless Strapi generates the pivot table.
- Use **components** for repeated field groups (SEO, Address, OpenGraph, SocialLinks).
- Use **dynamic zones** sparingly — only when content truly varies per entry.
- Always add `publishedAt` (draft/publish) unless the content type is purely internal.
- Use `uid` field type for slugs; set `targetField` to `title`.
- Add `locale` field only when enabling i18n on the content type.

### Custom API Route Pattern

```ts
// src/api/[content-type]/routes/custom.ts
export default {
  routes: [
    {
      method: "GET",
      path: "/[content-type]/featured",
      handler: "[content-type].featured",
      config: { auth: false, middlewares: [], policies: [] },
    },
  ],
};
```

### Custom Controller Pattern

```ts
// src/api/[content-type]/controllers/[content-type].ts
import { factories } from "@strapi/strapi";

export default factories.createCoreController(
  "api::[content-type].[content-type]",
  ({ strapi }) => ({
    async featured(ctx) {
      const entries = await strapi
        .documents("api::[content-type].[content-type]")
        .findMany({
          filters: { featured: true },
          populate: { image: true, author: { fields: ["name"] } },
          status: "published",
        });
      return this.transformResponse(entries);
    },
  })
);
```

### Custom Service Pattern

```ts
// src/api/[content-type]/services/[content-type].ts
import { factories } from "@strapi/strapi";

export default factories.createCoreService(
  "api::[content-type].[content-type]",
  ({ strapi }) => ({
    async findWithStats(documentId: string) {
      const entry = await strapi
        .documents("api::[content-type].[content-type]")
        .findOne({ documentId, populate: "*" });
      return entry;
    },
  })
);
```

### Lifecycle Hooks Pattern

```ts
// src/api/[content-type]/content-types/[content-type]/lifecycles.ts
export default {
  async beforeCreate(event) {
    const { data } = event.params;
    // mutate data before insert
  },
  async afterCreate(event) {
    const { result } = event;
    // trigger side effects: emails, cache invalidation, webhooks
  },
  async afterPublish(event) {
    // fires on draft → publish transition
  },
};
```

### Custom Middleware

```ts
// src/middlewares/rate-limit.ts
export default (config, { strapi }) => {
  return async (ctx, next) => {
    // custom logic before
    await next();
    // custom logic after
  };
};
```

Register in `config/middlewares.ts`:
```ts
export default [
  "strapi::logger", "strapi::errors", "strapi::security",
  "strapi::cors", "strapi::poweredBy", "strapi::query",
  "strapi::body", "strapi::session", "strapi::favicon", "strapi::public",
  { name: "global::rate-limit", config: {} },
];
```

### Webhooks

Configure in Admin → Settings → Webhooks, or trigger manually from lifecycle:
```ts
async afterCreate(event) {
  await fetch(process.env.WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ event: "entry.create", data: event.result }),
  });
}
```

### i18n (Internationalization)

Enable in `config/plugins.ts`:
```ts
export default () => ({ i18n: { enabled: true } });
```

Enable locale on each content type via Admin panel. Query with locale:
```ts
await strapi.documents("api::post.post").findMany({
  locale: "th", status: "published",
});
```

---

## React Frontend Setup

### Bootstrap

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install @tanstack/react-query axios zustand
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p && npx shadcn@latest init
```

### QueryClient Setup

```ts
// src/lib/queryClient.ts
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      gcTime: 1000 * 60 * 10,
      retry: (failureCount, error: any) => {
        if (error?.response?.status === 404) return false;
        return failureCount < 2;
      },
    },
  },
});
```

### API Client (Axios)

```ts
// src/lib/api.ts
import axios from "axios";
import { queryClient } from "./queryClient";

export const api = axios.create({
  baseURL: import.meta.env.VITE_STRAPI_URL + "/api",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      queryClient.clear();
    }
    return Promise.reject(error);
  }
);
```

### Data Fetching Hook Pattern

```ts
// src/hooks/usePosts.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { StrapiListResponse, StrapiResponse, Post } from "@/types";

export function usePosts(params?: Record<string, unknown>) {
  return useQuery<StrapiListResponse<Post>>({
    queryKey: ["posts", params],
    queryFn: async () => {
      const { data } = await api.get("/posts", {
        params: {
          populate: { author: { fields: ["name"] }, tags: true },
          sort: ["createdAt:desc"],
          ...params,
        },
      });
      return data;
    },
  });
}

export function useCreatePost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Post>) => {
      const { data } = await api.post<StrapiResponse<Post>>("/posts", { data: payload });
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["posts"] }),
  });
}
```

### Strapi Query Params (v5)

```ts
const params = {
  populate: {
    author: { fields: ["name", "avatar"] },
    tags: true,
    coverImage: { fields: ["url", "alternativeText", "width", "height"] },
  },
  filters: {
    publishedAt: { $notNull: true },
    tags: { slug: { $eq: "featured" } },
  },
  pagination: { page: 1, pageSize: 20 },
  sort: ["createdAt:desc"],
  locale: "en",
};
```

### File Upload

```ts
export async function uploadFile(file: File): Promise<StrapiMedia> {
  const formData = new FormData();
  formData.append("files", file);
  const { data } = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data[0];
}

// Upload and link to entry in one request
formData.append("files.coverImage", file, file.name);
formData.append("data", JSON.stringify({ title: "My Post" }));
await api.post("/posts", formData, { headers: { "Content-Type": "multipart/form-data" } });
```

### Zustand Auth Store

```ts
// src/stores/authStore.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthState {
  token: string | null;
  user: StrapiUser | null;
  setAuth: (token: string, user: StrapiUser) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null, user: null,
      setAuth: (token, user) => set({ token, user }),
      logout: () => set({ token: null, user: null }),
    }),
    { name: "auth-storage" }
  )
);
```

---

## Authentication

```ts
// src/lib/auth.ts
export async function login(identifier: string, password: string) {
  const { data } = await api.post("/auth/local", { identifier, password });
  useAuthStore.getState().setAuth(data.jwt, data.user);
  return data;
}

export async function register(username: string, email: string, password: string) {
  const { data } = await api.post("/auth/local/register", { username, email, password });
  useAuthStore.getState().setAuth(data.jwt, data.user);
  return data;
}
```

### Protected Route (React Router v6)

```tsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";

export function ProtectedRoute({ requiredRole }: { requiredRole?: string }) {
  const { token, user } = useAuthStore();
  if (!token) return <Navigate to="/login" replace />;
  if (requiredRole && user?.role?.type !== requiredRole)
    return <Navigate to="/unauthorized" replace />;
  return <Outlet />;
}
```

### Role & Permission Setup
- `Public` role: read-only on published content
- `Authenticated` role: CRUD on user-owned content
- Custom roles: Admin → Settings → Roles
- For ownership filtering: add a `owner` relation and filter in services or custom policies

---

## Error Handling

### Strapi Error Parsing

```ts
// src/lib/strapiError.ts
import type { StrapiError } from "@/types";

export function parseStrapiError(error: unknown): string {
  const err = (error as any)?.response?.data as StrapiError | undefined;
  if (!err) return "An unexpected error occurred";
  return err.error?.message ?? "Unknown Strapi error";
}
```

### React Query Error Boundary

```tsx
import { useQueryErrorResetBoundary } from "@tanstack/react-query";
import { ErrorBoundary } from "react-error-boundary";

export function QueryErrorBoundary({ children }: { children: React.ReactNode }) {
  const { reset } = useQueryErrorResetBoundary();
  return (
    <ErrorBoundary onReset={reset} fallbackRender={({ resetErrorBoundary, error }) => (
      <div className="p-4 text-destructive">
        <p>{error.message}</p>
        <button onClick={resetErrorBoundary}>Retry</button>
      </div>
    )}>
      {children}
    </ErrorBoundary>
  );
}
```

---

## Database Patterns

### Relations
| Relation | Use case |
|---|---|
| `oneToOne` | User ↔ Profile |
| `oneToMany` | Author → Posts |
| `manyToMany` | Posts ↔ Tags |
| `manyToOne` | Comments → Post |

### Migrations
1. Run `strapi develop` locally → generates migration files in `database/migrations/`
2. Commit migration artifacts
3. `strapi start` in production applies pending migrations on boot

**Never manually alter PostgreSQL schema outside Strapi** — it desyncs the schema registry.

---

## Docker Compose (Development)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: strapi
      POSTGRES_USER: strapi
      POSTGRES_PASSWORD: strapi
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U strapi"]
      interval: 10s
      retries: 5

  strapi:
    build: ./backend
    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_NAME: strapi
      DATABASE_USERNAME: strapi
      DATABASE_PASSWORD: strapi
      NODE_ENV: development
    ports: ["1337:1337"]
    depends_on:
      postgres: { condition: service_healthy }
    volumes: ["./backend:/app", "/app/node_modules"]

  frontend:
    build: ./frontend
    ports: ["5173:5173"]
    environment:
      VITE_STRAPI_URL: http://localhost:1337
    volumes: ["./frontend:/app", "/app/node_modules"]

volumes:
  pgdata:
```

---

## Design System (Tailwind + shadcn/ui)

- Extend `tailwind.config.ts` with brand tokens mapped to CSS variables
- Customize via `cn()` — do NOT override Tailwind classes globally
- Co-locate variants using `cva()`:

```ts
import { cva } from "class-variance-authority";

export const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
      },
      size: { default: "h-10 px-4 py-2", sm: "h-9 px-3", lg: "h-11 px-8" },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
);
```

---

## Performance Patterns

- Use `select` in React Query to filter/transform without extra renders
- Use API tokens (read-only) for public pages to skip JWT overhead
- Use `fields` in populate to avoid overfetching
- Infinite scroll: `useInfiniteQuery` with `pagination[start]` + `pagination[limit]`
- Enable Strapi REST cache plugin for high-traffic public endpoints

---

## Testing

### Frontend (React Testing Library)

```tsx
import { render, screen } from "@testing-library/react";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";

const wrapper = ({ children }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

it("renders post title", () => {
  render(<PostCard post={mockPost} />, { wrapper });
  expect(screen.getByText(mockPost.title)).toBeInTheDocument();
});
```

### Backend (Strapi Integration Tests)

```ts
import request from "supertest";

let strapi;
beforeAll(async () => { strapi = await createStrapi().load(); await strapi.start(); });
afterAll(() => strapi.destroy());

it("GET /api/posts returns published posts", async () => {
  const res = await request(strapi.server.httpServer).get("/api/posts").expect(200);
  expect(res.body.data).toBeInstanceOf(Array);
});
```

---

## Advanced Patterns (Quick Reference)

For full code examples, read `references/patterns-advanced.md`.

**Optimistic Updates** — `onMutate`: cancelQueries → snapshot → setQueryData optimistically → return snapshot. `onError`: restore snapshot. `onSettled`: invalidateQueries.

**Forms** — `npm install react-hook-form zod @hookform/resolvers`. Use `zodResolver` + shadcn `<Form>` components. Catch Strapi errors with `form.setError("root", ...)`. Auto-slug: `form.setValue("slug", title.toLowerCase().replace(/\s+/g, "-"))`.

**Custom Policy / Authorization** — See `references/rbac-policies.md`. Register policy in route `config.policies`. Filter by owner in controller: `ctx.query.filters = { owner: { id: { $eq: ctx.state.user.id } } }`. Frontend: `usePermissions()` hook checks `user.role.type`.

**Upload Providers** — Cloudinary: `@strapi/provider-upload-cloudinary`. S3: `@strapi/provider-upload-aws-s3`. Both configured in `config/plugins.ts` → `upload.config`. Add CSP `img-src` entries in `strapi::security` middleware for the CDN domain.

**Strapi Admin Customization** — Rebrand via `src/admin/app.tsx` `config.theme.light.colors` + `config.translations`. Inject React components into edit view with `app.injectContentManagerComponent()`.

---

## Reference Files

Read these when the user's task touches those areas:

- `references/strapi-v5-changes.md` — Breaking changes, Document Service API, plugin changes, migration from v4
- `references/deployment.md` — Railway, Render, VPS deployment, SSL, CI/CD, env var checklist, backups
- `references/typescript-types.md` — Full Strapi v5 response types, media types, error types, auth types, typed hooks
- `references/rbac-policies.md` — Custom policies, is-owner pattern, ownership filtering, API tokens, users-permissions extension
- `references/caching.md` — REST cache plugin (memory/Redis), React Query cache tiers, prefetching, CDN cache headers
- `references/custom-plugins.md` — Plugin scaffold, server/admin structure, plugin store, custom fields, publishing to npm
- `references/real-time.md` — SSE endpoint, Socket.io plugin, polling patterns, Nginx config for WebSockets/SSE
- `references/testing-advanced.md` — MSW mocking, RTL component tests, Strapi supertest integration tests, Playwright E2E, CI
- `references/patterns-advanced.md` — Optimistic updates, react-hook-form + zod forms, upload providers (Cloudinary/S3), Strapi admin customization