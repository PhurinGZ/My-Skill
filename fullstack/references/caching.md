# Caching Strategies

## Strapi REST Cache Plugin

```bash
npm install @strapi/plugin-rest-cache @strapi/provider-rest-cache-memory
# or for Redis:
npm install @strapi/plugin-rest-cache @strapi/provider-rest-cache-redis
```

```ts
// config/plugins.ts
export default ({ env }) => ({
  "rest-cache": {
    enabled: true,
    config: {
      provider: {
        name: "memory",           // or "redis"
        options: { max: 32767, ttl: 60 * 60 }, // in-memory: 1hr TTL
      },
      strategy: {
        contentTypes: [
          { contentType: "api::post.post", hitpass: false },
          { contentType: "api::category.category", hitpass: false },
        ],
      },
    },
  },
});
```

### Redis provider config:
```ts
provider: {
  name: "redis",
  options: {
    socket: { host: env("REDIS_HOST", "127.0.0.1"), port: env.int("REDIS_PORT", 6379) },
    password: env("REDIS_PASSWORD", undefined),
    ttl: 60 * 60, // 1hr
  },
},
```

---

## Manual Cache Invalidation (from lifecycle)

```ts
// src/api/post/content-types/post/lifecycles.ts
export default {
  async afterCreate() {
    await strapi.plugin("rest-cache").service("cacheStore").clearByContentType("api::post.post");
  },
  async afterUpdate() {
    await strapi.plugin("rest-cache").service("cacheStore").clearByContentType("api::post.post");
  },
  async afterDelete() {
    await strapi.plugin("rest-cache").service("cacheStore").clearByContentType("api::post.post");
  },
};
```

---

## React Query Caching Strategy

### Stale-while-revalidate tiers:

```ts
// src/lib/queryClient.ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,    // 5 min — data considered fresh
      gcTime: 1000 * 60 * 30,      // 30 min — keep in memory unused
    },
  },
});
```

### Per-query overrides:
```ts
// Rarely-changing data (categories, tags) — cache longer
useQuery({ queryKey: ["categories"], queryFn: fetchCategories, staleTime: Infinity });

// Live data — always fresh
useQuery({ queryKey: ["notifications"], queryFn: fetchNotifications, staleTime: 0 });

// User-specific — short TTL
useQuery({ queryKey: ["profile", userId], queryFn: fetchProfile, staleTime: 1000 * 30 });
```

---

## Prefetching with React Query

```ts
// Prefetch on hover or route transition
async function prefetchPost(slug: string) {
  await queryClient.prefetchQuery({
    queryKey: ["post", slug],
    queryFn: () => fetchPost(slug),
    staleTime: 1000 * 60 * 5,
  });
}

// In component:
<Link
  to={`/posts/${post.slug}`}
  onMouseEnter={() => prefetchPost(post.slug)}
>
```

### Prefetch in loader (React Router v6 data API):
```ts
// src/pages/PostList/loader.ts
export async function postsLoader() {
  return queryClient.fetchQuery({
    queryKey: ["posts"],
    queryFn: fetchPosts,
  });
}
```

---

## Server-Side Caching Headers (Nginx)

Cache static frontend assets aggressively, API responses conservatively:

```nginx
# Cache frontend build assets (hashed filenames) forever
location /assets/ {
  expires 1y;
  add_header Cache-Control "public, immutable";
}

# Cache public Strapi API responses for 60s (CDN/proxy)
location /api/ {
  proxy_pass http://localhost:1337;
  proxy_cache_valid 200 60s;
  add_header X-Cache-Status $upstream_cache_status;
}

# Never cache auth endpoints
location /api/auth/ {
  proxy_pass http://localhost:1337;
  add_header Cache-Control "no-store";
}
```

---

## Optimistic Cache Updates (React Query)

See SKILL.md → "Optimistic Updates" section for full patterns.

Key principle: update `queryClient` cache immediately on mutation, rollback on error:

```ts
onMutate: async (newData) => {
  await queryClient.cancelQueries({ queryKey });
  const snapshot = queryClient.getQueryData(queryKey);
  queryClient.setQueryData(queryKey, (old) => /* apply optimistic update */);
  return { snapshot }; // rollback context
},
onError: (err, newData, context) => {
  queryClient.setQueryData(queryKey, context.snapshot); // rollback
},
onSettled: () => {
  queryClient.invalidateQueries({ queryKey }); // sync with server
},
```

---

## CDN Integration

For production, put Cloudflare (or similar) in front of Strapi:

1. Set `Cache-Control: public, max-age=60` on Strapi responses (use custom middleware)
2. Purge CDN cache on content publish via webhook → serverless function → CDN purge API
3. Use `surrogate-key` headers for tag-based purging (Cloudflare Enterprise / Fastly)

```ts
// src/middlewares/cache-headers.ts — add to public read endpoints
export default () => async (ctx, next) => {
  await next();
  if (ctx.method === "GET" && ctx.status === 200 && !ctx.state.user) {
    ctx.set("Cache-Control", "public, s-maxage=60, stale-while-revalidate=300");
  }
};
```
