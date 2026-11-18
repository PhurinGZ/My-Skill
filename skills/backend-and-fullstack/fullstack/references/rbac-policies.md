# RBAC, Policies & Authorization Patterns

## Custom Policy Pattern

Policies run before a controller and can block requests with 403/401.

```ts
// src/api/[content-type]/policies/is-owner.ts
import { errors } from "@strapi/utils";

export default async (policyContext, config, { strapi }) => {
  const { state, params } = policyContext;

  if (!state.user) throw new errors.UnauthorizedError("Not authenticated");

  const entry = await strapi
    .documents("api::[content-type].[content-type]")
    .findOne({ documentId: params.id, populate: { owner: { fields: ["id"] } } });

  if (!entry) throw new errors.NotFoundError();

  if (entry.owner?.id !== state.user.id) {
    throw new errors.ForbiddenError("You do not own this entry");
  }

  return true;
};
```

Register on a route:
```ts
// routes/[content-type].ts
export default {
  routes: [
    {
      method: "PUT",
      path: "/[content-type]/:id",
      handler: "[content-type].update",
      config: {
        policies: ["global::is-owner"],
        // or scoped: ["api::[content-type].is-owner"]
      },
    },
  ],
};
```

---

## Global Policy (applies across all content types)

```ts
// src/policies/is-authenticated.ts
import { errors } from "@strapi/utils";

export default async (policyContext) => {
  if (!policyContext.state.user) {
    throw new errors.UnauthorizedError();
  }
  return true;
};
```

Register in `config/middlewares.ts` or per-route via `"global::is-authenticated"`.

---

## Ownership Filtering in Service (Row-Level Security)

For list endpoints, filter by owner in the service rather than policy:

```ts
// src/api/post/services/post.ts
import { factories } from "@strapi/strapi";

export default factories.createCoreService("api::post.post", ({ strapi }) => ({
  async findOwned(userId: number) {
    return strapi.documents("api::post.post").findMany({
      filters: { owner: { id: { $eq: userId } } },
      status: "published",
    });
  },
}));
```

Override the default `find` controller to enforce ownership:
```ts
// src/api/post/controllers/post.ts
import { factories } from "@strapi/strapi";

export default factories.createCoreController("api::post.post", ({ strapi }) => ({
  async find(ctx) {
    if (ctx.state.user) {
      // authenticated: return only their entries
      ctx.query.filters = {
        ...(ctx.query.filters as object),
        owner: { id: { $eq: ctx.state.user.id } },
      };
    }
    return super.find(ctx);
  },
}));
```

---

## RBAC — Custom Roles

1. Admin → Settings → Roles → Add new role (e.g. `editor`, `moderator`)
2. Assign granular permissions per content type (find, findOne, create, update, delete, publish)
3. Assign role to users via Admin or API:

```ts
// Assign role to user programmatically (e.g. in lifecycle)
await strapi.documents("plugin::users-permissions.user").update({
  documentId: user.documentId,
  data: { role: roleId },
});
```

---

## Checking Role in Frontend

```ts
// src/hooks/usePermissions.ts
import { useAuthStore } from "@/stores/authStore";

export function usePermissions() {
  const user = useAuthStore((s) => s.user);
  const role = user?.role?.type ?? "public";

  return {
    isAuthenticated: !!user,
    isAdmin: role === "admin",
    isEditor: role === "editor",
    can: (requiredRole: string) => role === requiredRole || role === "admin",
  };
}
```

```tsx
// Usage in component
const { isAdmin, can } = usePermissions();
return (
  <>
    {can("editor") && <EditButton />}
    {isAdmin && <DeleteButton />}
  </>
);
```

---

## API Token (Server-to-Server)

For backend-to-backend calls, use API tokens (not JWT):

```ts
// Admin → Settings → API Tokens → Create token
// Set type: Read-only / Full access / Custom

// Use in request headers:
Authorization: Bearer <api-token>

// Generate read-only token per environment via Strapi bootstrap:
// src/index.ts
export default {
  async bootstrap({ strapi }) {
    const tokenService = strapi.service("admin::api-token");
    const exists = await tokenService.getByName("public-read");
    if (!exists) {
      await tokenService.create({
        name: "public-read",
        type: "read-only",
        lifespan: null, // no expiry
      });
    }
  },
};
```

---

## users-permissions Plugin Extension

Override the `/me` endpoint or add custom auth logic:

```ts
// src/extensions/users-permissions/strapi-server.ts
export default (plugin) => {
  const getMe = plugin.controllers.user.me;

  plugin.controllers.user.me = async (ctx) => {
    await getMe(ctx);
    // Enrich response with additional data
    if (ctx.body?.id) {
      const profile = await strapi.documents("api::profile.profile").findMany({
        filters: { user: { id: ctx.body.id } },
      });
      ctx.body.profile = profile[0] ?? null;
    }
  };

  return plugin;
};
```
