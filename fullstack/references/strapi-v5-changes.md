# Strapi v5 — Key Changes from v4

## Response Format (BREAKING)

v4 wrapped everything in `data.attributes`. v5 is flat:

```ts
// v4
response.data.attributes.title
response.data.id

// v5
response.data.title
response.data.id
response.data.documentId   // NEW: stable across draft/publish cycles
```

Update ALL frontend API response handlers when migrating from v4.

---

## Document Service API (replaces Entity Service — BREAKING)

```ts
// v4 (Entity Service)
await strapi.entityService.findMany("api::post.post", { populate: ["author"] });
await strapi.entityService.findOne("api::post.post", id, { populate: "*" });
await strapi.entityService.create("api::post.post", { data: { title: "..." } });
await strapi.entityService.update("api::post.post", id, { data: { title: "..." } });
await strapi.entityService.delete("api::post.post", id);

// v5 (Document Service) — use documentId, not numeric id
const doc = strapi.documents("api::post.post");

await doc.findMany({ populate: ["author"], status: "published" });
await doc.findOne({ documentId: "abc123", populate: "*" });
await doc.create({ data: { title: "..." } });
await doc.update({ documentId: "abc123", data: { title: "..." } });
await doc.delete({ documentId: "abc123" });
await doc.publish({ documentId: "abc123" });
await doc.unpublish({ documentId: "abc123" });
```

---

## documentId vs id

- `id`: internal auto-increment — different between draft and published copies
- `documentId`: stable string ID — same across draft/publish/locale variants
- **Always use `documentId`** for lookups, links, and API operations in v5
- The REST API returns both; use `documentId` in frontend URLs and references

---

## Draft & Publish

- Default REST API returns `status: "published"` entries only
- Query drafts: add `status=draft` param (requires auth)
- In Document Service: `status: "draft"` | `"published"` (default: `"published"`)

```ts
// REST: get drafts
GET /api/posts?status=draft   // requires authenticated request

// Document Service
await strapi.documents("api::post.post").findMany({ status: "draft" });
```

---

## Populate Changes

Populate in v5 uses the same syntax but is more powerful:

```ts
// Deep populate with field selection
populate: {
  author: { fields: ["name", "email"], populate: { avatar: { fields: ["url"] } } },
  tags: { fields: ["name", "slug"] },
  seo: true,         // populate component
  sections: { on: { // populate dynamic zone by component type
    "sections.hero": { fields: ["title", "subtitle"] },
    "sections.cta": true,
  }},
}
```

---

## Filters & Operators

```ts
filters: {
  $and: [
    { publishedAt: { $notNull: true } },
    { title: { $containsi: "strapi" } },  // case-insensitive contains
  ],
  tags: { slug: { $in: ["react", "typescript"] } },
  createdAt: { $gte: "2024-01-01" },
}
```

Operators: `$eq`, `$ne`, `$lt`, `$lte`, `$gt`, `$gte`, `$in`, `$notIn`, `$contains`, `$notContains`, `$containsi`, `$notContainsi`, `$null`, `$notNull`, `$between`, `$startsWith`, `$endsWith`, `$or`, `$and`, `$not`

---

## Plugin Development Changes

- Plugins now use the same Document Service as core
- `strapi.plugin('x').service('y')` still works
- Admin panel customization moved to `src/admin/app.tsx`:

```ts
// src/admin/app.tsx
export default {
  config: {
    locales: ["th", "en"],
    translations: { en: { "app.components.LeftMenu.navbrand.title": "My CMS" } },
  },
  bootstrap(app) {
    // customize admin panel
  },
};
```

---

## TypeScript — First-Class Support

- `types/generated/` auto-generated on `strapi develop`
- Contains full types for all content types, components, plugins
- Use in custom controllers/services:

```ts
import type { Data } from "@strapi/strapi";
// or use generated types
import type { ApiPostPost } from "../../types/generated/contentTypes";
```

---

## Middleware Signature Change

```ts
// v4
module.exports = (config, { strapi }) => async (ctx, next) => { ... };

// v5
export default (config, { strapi }) => {
  return async (ctx, next) => {
    await next();
  };
};
```

---

## CORS Configuration (v5)

```ts
// config/middlewares.ts
export default [
  // ...
  {
    name: "strapi::cors",
    config: {
      enabled: true,
      headers: "*",
      origin: ["http://localhost:5173", "https://yourdomain.com"],
    },
  },
  // ...
];
```

---

## Migrating from v4 to v5

1. Update Node.js to v18+ (v20 recommended)
2. Run `npx @strapi/upgrade major` — automated codemods available
3. Update all `entityService` calls to `documents()`
4. Update all frontend response parsers (remove `.attributes`)
5. Replace numeric `id` references with `documentId` in URLs and links
6. Re-test all custom controllers, services, and lifecycle hooks
7. Review any custom plugins for Document Service compatibility
