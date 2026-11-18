# TypeScript Types for Strapi v5 in React

## Base Response Types

```ts
// src/types/strapi.ts

export interface StrapiMeta {
  pagination?: {
    page: number;
    pageSize: number;
    pageCount: number;
    total: number;
  };
}

export interface StrapiResponse<T> {
  data: T;
  meta: StrapiMeta;
}

export interface StrapiListResponse<T> {
  data: T[];
  meta: StrapiMeta;
}

export interface StrapiError {
  data: null;
  error: {
    status: number;
    name: string;
    message: string;
    details: Record<string, unknown>;
  };
}
```

---

## Base Entity Fields (v5 — flat, no attributes wrapper)

```ts
// src/types/base.ts
export interface StrapiEntity {
  id: number;
  documentId: string;
  createdAt: string;
  updatedAt: string;
  publishedAt: string | null;
  locale?: string;
}
```

---

## Media / File Types

```ts
// src/types/media.ts
export interface StrapiMediaFormat {
  name: string;
  hash: string;
  ext: string;
  mime: string;
  width: number;
  height: number;
  size: number;
  url: string;
}

export interface StrapiMedia extends StrapiEntity {
  name: string;
  alternativeText: string | null;
  caption: string | null;
  width: number | null;
  height: number | null;
  formats: {
    thumbnail?: StrapiMediaFormat;
    small?: StrapiMediaFormat;
    medium?: StrapiMediaFormat;
    large?: StrapiMediaFormat;
  } | null;
  hash: string;
  ext: string;
  mime: string;
  size: number;
  url: string;
  previewUrl: string | null;
  provider: string;
}

// Helper to get the best URL for a given max width
export function getMediaUrl(media: StrapiMedia | null, maxWidth = 800): string {
  if (!media) return "";
  const base = import.meta.env.VITE_STRAPI_URL;
  if (!media.formats) return base + media.url;
  if (maxWidth <= 300 && media.formats.thumbnail) return base + media.formats.thumbnail.url;
  if (maxWidth <= 500 && media.formats.small) return base + media.formats.small.url;
  if (maxWidth <= 750 && media.formats.medium) return base + media.formats.medium.url;
  if (media.formats.large) return base + media.formats.large.url;
  return base + media.url;
}
```

---

## Auth Types

```ts
// src/types/auth.ts
export interface StrapiRole {
  id: number;
  name: string;
  description: string;
  type: "public" | "authenticated" | string;
}

export interface StrapiUser extends StrapiEntity {
  username: string;
  email: string;
  confirmed: boolean;
  blocked: boolean;
  role?: StrapiRole;
}

export interface StrapiAuthResponse {
  jwt: string;
  user: StrapiUser;
}
```

---

## Content Type Example (Post)

```ts
// src/types/post.ts
import type { StrapiEntity, StrapiMedia } from "./base";

export interface Tag extends StrapiEntity {
  name: string;
  slug: string;
}

export interface Author extends StrapiEntity {
  name: string;
  bio?: string;
  avatar?: StrapiMedia;
}

export interface PostSEO {
  metaTitle?: string;
  metaDescription?: string;
  shareImage?: StrapiMedia;
}

export interface Post extends StrapiEntity {
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  featured: boolean;
  coverImage?: StrapiMedia;
  author?: Author;
  tags?: Tag[];
  seo?: PostSEO;
}
```

---

## Typed API Hooks

```ts
// src/hooks/usePost.ts
import { useQuery, useMutation, useInfiniteQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { StrapiListResponse, StrapiResponse } from "@/types/strapi";
import type { Post } from "@/types/post";

// Single post by slug
export function usePost(slug: string) {
  return useQuery<StrapiResponse<Post>>({
    queryKey: ["post", slug],
    queryFn: async () => {
      const { data } = await api.get<StrapiListResponse<Post>>("/posts", {
        params: {
          filters: { slug: { $eq: slug } },
          populate: { author: true, tags: true, coverImage: true, seo: true },
        },
      });
      if (!data.data[0]) throw new Error("Post not found");
      return { data: data.data[0], meta: data.meta };
    },
    enabled: !!slug,
  });
}

// Infinite scroll posts
export function useInfinitePosts(pageSize = 10) {
  return useInfiniteQuery<StrapiListResponse<Post>>({
    queryKey: ["posts-infinite"],
    queryFn: async ({ pageParam = 0 }) => {
      const { data } = await api.get("/posts", {
        params: {
          populate: { coverImage: { fields: ["url", "alternativeText"] }, tags: true },
          pagination: { start: pageParam as number, limit: pageSize },
          sort: ["createdAt:desc"],
        },
      });
      return data;
    },
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages) => {
      const loaded = allPages.flatMap((p) => p.data).length;
      return loaded < lastPage.meta.pagination!.total ? loaded : undefined;
    },
  });
}

// Create post
export function useCreatePost() {
  const qc = useQueryClient();
  return useMutation<StrapiResponse<Post>, Error, Partial<Post>>({
    mutationFn: async (payload) => {
      const { data } = await api.post<StrapiResponse<Post>>("/posts", { data: payload });
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["posts"] });
      qc.invalidateQueries({ queryKey: ["posts-infinite"] });
    },
  });
}

// Update post
export function useUpdatePost() {
  const qc = useQueryClient();
  return useMutation<StrapiResponse<Post>, Error, { documentId: string; data: Partial<Post> }>({
    mutationFn: async ({ documentId, data: payload }) => {
      const { data } = await api.put<StrapiResponse<Post>>(`/posts/${documentId}`, { data: payload });
      return data;
    },
    onSuccess: (_, { documentId }) => {
      qc.invalidateQueries({ queryKey: ["posts"] });
      qc.invalidateQueries({ queryKey: ["post"] });
    },
  });
}
```

---

## Auto-Generated Types (Strapi Side)

Run `strapi develop` — Strapi writes full TypeScript types to `types/generated/`.

Sharing with frontend:
1. **Copy-paste** and keep in sync manually (simple projects)
2. **Symlink** `backend/types/generated` into `frontend/src/types/strapi-generated` (monorepo)
3. **Private npm package** — publish as `@myproject/strapi-types` (large teams)

---

## Zod Schemas for Runtime Validation

```ts
// src/lib/schemas.ts
import { z } from "zod";

export const postSchema = z.object({
  id: z.number(),
  documentId: z.string(),
  title: z.string().min(1),
  slug: z.string(),
  content: z.string(),
  publishedAt: z.string().nullable(),
});

export type PostFromSchema = z.infer<typeof postSchema>;

// Validate API response at runtime
export function validatePost(data: unknown): Post {
  return postSchema.parse(data);
}
```
