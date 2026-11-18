# Advanced Testing Patterns

## Frontend: MSW (Mock Service Worker) for API Mocking

```bash
npm install -D msw @mswjs/data
npx msw init public/ --save
```

```ts
// src/mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("*/api/posts", () => {
    return HttpResponse.json({
      data: [
        { id: 1, documentId: "abc123", title: "Test Post", slug: "test-post", publishedAt: new Date().toISOString() },
      ],
      meta: { pagination: { page: 1, pageSize: 10, pageCount: 1, total: 1 } },
    });
  }),

  http.post("*/api/auth/local", async ({ request }) => {
    const body = await request.json() as { identifier: string; password: string };
    if (body.password === "wrong") {
      return HttpResponse.json(
        { data: null, error: { status: 400, name: "ValidationError", message: "Invalid credentials", details: {} } },
        { status: 400 }
      );
    }
    return HttpResponse.json({ jwt: "mock-jwt", user: { id: 1, documentId: "user1", username: "testuser", email: body.identifier } });
  }),
];
```

```ts
// src/mocks/browser.ts
import { setupWorker } from "msw/browser";
import { handlers } from "./handlers";
export const worker = setupWorker(...handlers);

// src/main.tsx — enable in development
if (import.meta.env.DEV) {
  const { worker } = await import("./mocks/browser");
  await worker.start({ onUnhandledRequest: "bypass" });
}
```

---

## Frontend: Component Tests with React Testing Library + MSW

```tsx
// src/components/PostList/__tests__/PostList.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { server } from "@/mocks/server"; // MSW Node server
import { http, HttpResponse } from "msw";
import { PostList } from "../PostList";
import { createTestQueryClient } from "@/test-utils";

const wrapper = ({ children }) => (
  <QueryClientProvider client={createTestQueryClient()}>
    <MemoryRouter>{children}</MemoryRouter>
  </QueryClientProvider>
);

describe("PostList", () => {
  it("renders post titles", async () => {
    render(<PostList />, { wrapper });
    await waitFor(() => {
      expect(screen.getByText("Test Post")).toBeInTheDocument();
    });
  });

  it("shows error state on API failure", async () => {
    server.use(
      http.get("*/api/posts", () => HttpResponse.json({ error: "Server Error" }, { status: 500 }))
    );
    render(<PostList />, { wrapper });
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

```ts
// src/mocks/server.ts (Node — for Jest/Vitest)
import { setupServer } from "msw/node";
import { handlers } from "./handlers";
export const server = setupServer(...handlers);

// src/test-setup.ts
import { server } from "./mocks/server";
beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

## Frontend: Test Utilities

```ts
// src/test-utils.ts
import { QueryClient } from "@tanstack/react-query";

// Fresh client per test — avoids cross-test cache pollution
export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}
```

---

## Backend: Strapi Integration Tests (Supertest)

```ts
// tests/helpers/strapi.ts
import Strapi from "@strapi/strapi";

let instance: Strapi.Strapi;

export async function setupStrapi() {
  if (!instance) {
    instance = await Strapi({ distDir: "./dist" }).load();
    await instance.server.mount();
  }
  return instance;
}

export async function teardownStrapi() {
  await instance?.destroy();
}
```

```ts
// tests/api/posts.test.ts
import request from "supertest";
import { setupStrapi, teardownStrapi } from "../helpers/strapi";

let strapi;
let authToken: string;

beforeAll(async () => {
  strapi = await setupStrapi();

  // Create test user + get JWT
  const res = await request(strapi.server.httpServer)
    .post("/api/auth/local/register")
    .send({ username: "tester", email: "tester@test.com", password: "Test1234!" });
  authToken = res.body.jwt;
});

afterAll(teardownStrapi);

describe("GET /api/posts", () => {
  it("returns published posts unauthenticated", async () => {
    const res = await request(strapi.server.httpServer).get("/api/posts").expect(200);
    expect(res.body.data).toBeInstanceOf(Array);
  });

  it("returns 401 for protected endpoint without token", async () => {
    await request(strapi.server.httpServer).get("/api/posts/mine").expect(401);
  });

  it("returns user's posts when authenticated", async () => {
    const res = await request(strapi.server.httpServer)
      .get("/api/posts/mine")
      .set("Authorization", `Bearer ${authToken}`)
      .expect(200);
    expect(res.body.data).toBeInstanceOf(Array);
  });
});

describe("POST /api/posts", () => {
  it("creates a post as authenticated user", async () => {
    const res = await request(strapi.server.httpServer)
      .post("/api/posts")
      .set("Authorization", `Bearer ${authToken}`)
      .send({ data: { title: "Test Post", content: "Hello", slug: "test-post" } })
      .expect(200);
    expect(res.body.data.title).toBe("Test Post");
    expect(res.body.data.documentId).toBeDefined();
  });
});
```

---

## Backend: Unit Testing Services

```ts
// tests/unit/post-service.test.ts
// Mock strapi global before importing service
global.strapi = {
  documents: jest.fn().mockReturnValue({
    findMany: jest.fn().mockResolvedValue([{ id: 1, documentId: "abc", title: "Mock Post" }]),
  }),
} as unknown as typeof strapi;

import { postService } from "../../src/api/post/services/post";

describe("PostService.findOwned", () => {
  it("filters by owner id", async () => {
    const result = await postService({ strapi }).findOwned(42);
    expect(strapi.documents).toHaveBeenCalledWith("api::post.post");
    expect(result[0].title).toBe("Mock Post");
  });
});
```

---

## E2E Tests: Playwright

```bash
npm install -D @playwright/test
npx playwright install
```

```ts
// e2e/auth.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test("user can log in", async ({ page }) => {
    await page.goto("/login");
    await page.fill('[name="email"]', "test@test.com");
    await page.fill('[name="password"]', "Test1234!");
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL("/dashboard");
    await expect(page.getByText("Welcome")).toBeVisible();
  });

  test("shows error on wrong credentials", async ({ page }) => {
    await page.goto("/login");
    await page.fill('[name="email"]', "test@test.com");
    await page.fill('[name="password"]', "wrongpassword");
    await page.click('button[type="submit"]');
    await expect(page.getByText(/invalid credentials/i)).toBeVisible();
  });
});
```

```ts
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  use: {
    baseURL: "http://localhost:5173",
    trace: "on-first-retry",
  },
  webServer: [
    { command: "npm run dev", cwd: "frontend", url: "http://localhost:5173", reuseExistingServer: true },
    { command: "npm run develop", cwd: "backend", url: "http://localhost:1337/api/health", reuseExistingServer: true },
  ],
});
```

---

## CI: Run All Tests

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env: { POSTGRES_DB: strapi_test, POSTGRES_USER: strapi, POSTGRES_PASSWORD: strapi }
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: cd frontend && npm ci && npm test -- --run
      - run: cd backend && npm ci && npm test
        env: { DATABASE_HOST: localhost, DATABASE_NAME: strapi_test, NODE_ENV: test }
      - run: cd frontend && npm run build && npx playwright test
```
