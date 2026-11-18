# Advanced Patterns

## Optimistic Updates (React Query)

```ts
// src/hooks/usePosts.ts — optimistic toggle
export function useToggleFeatured() {
  const qc = useQueryClient();
  return useMutation<StrapiResponse<Post>, Error, { documentId: string; featured: boolean }>({
    mutationFn: ({ documentId, featured }) =>
      api.put(`/posts/${documentId}`, { data: { featured } }).then((r) => r.data),

    onMutate: async ({ documentId, featured }) => {
      const key = ["posts"];
      await qc.cancelQueries({ queryKey: key });
      const snapshot = qc.getQueryData<StrapiListResponse<Post>>(key);

      qc.setQueryData<StrapiListResponse<Post>>(key, (old) =>
        old
          ? { ...old, data: old.data.map((p) => (p.documentId === documentId ? { ...p, featured } : p)) }
          : old
      );
      return { snapshot };
    },

    onError: (_err, _vars, context) => {
      if (context?.snapshot) qc.setQueryData(["posts"], context.snapshot);
    },

    onSettled: () => qc.invalidateQueries({ queryKey: ["posts"] }),
  });
}
```

Pattern: always `cancelQueries` → snapshot → optimistic update → rollback on error → `invalidateQueries` on settled.

---

## Form Handling (react-hook-form + zod + shadcn/ui)

```bash
npm install react-hook-form zod @hookform/resolvers
```

```tsx
// src/components/PostForm.tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useCreatePost } from "@/hooks/usePosts";
import { parseStrapiError } from "@/lib/strapiError";

const postSchema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters"),
  slug: z.string().regex(/^[a-z0-9-]+$/, "Slug must be lowercase with hyphens only"),
  content: z.string().min(10, "Content too short"),
  excerpt: z.string().max(200).optional(),
});

type PostFormValues = z.infer<typeof postSchema>;

export function PostForm() {
  const form = useForm<PostFormValues>({
    resolver: zodResolver(postSchema),
    defaultValues: { title: "", slug: "", content: "", excerpt: "" },
  });

  const createPost = useCreatePost();

  async function onSubmit(values: PostFormValues) {
    try {
      await createPost.mutateAsync(values);
      form.reset();
    } catch (err) {
      form.setError("root", { message: parseStrapiError(err) });
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField control={form.control} name="title" render={({ field }) => (
          <FormItem>
            <FormLabel>Title</FormLabel>
            <FormControl><Input {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <FormField control={form.control} name="content" render={({ field }) => (
          <FormItem>
            <FormLabel>Content</FormLabel>
            <FormControl><Textarea rows={8} {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        {form.formState.errors.root && (
          <p className="text-sm text-destructive">{form.formState.errors.root.message}</p>
        )}
        <Button type="submit" disabled={createPost.isPending}>
          {createPost.isPending ? "Saving…" : "Publish"}
        </Button>
      </form>
    </Form>
  );
}
```

### Auto-generate slug from title:
```ts
const title = form.watch("title");
useEffect(() => {
  if (!form.getValues("slug")) {
    form.setValue("slug", title.toLowerCase().replace(/\s+/g, "-").replace(/[^a-z0-9-]/g, ""));
  }
}, [title]);
```

---

## Upload Providers (Cloudinary / S3)

### Cloudinary:
```bash
npm install @strapi/provider-upload-cloudinary
```

```ts
// config/plugins.ts
export default ({ env }) => ({
  upload: {
    config: {
      provider: "cloudinary",
      providerOptions: {
        cloud_name: env("CLOUDINARY_NAME"),
        api_key: env("CLOUDINARY_KEY"),
        api_secret: env("CLOUDINARY_SECRET"),
      },
      actionOptions: { upload: {}, uploadStream: {}, delete: {} },
    },
  },
});
```

### AWS S3:
```bash
npm install @strapi/provider-upload-aws-s3
```

```ts
upload: {
  config: {
    provider: "aws-s3",
    providerOptions: {
      accessKeyId: env("AWS_ACCESS_KEY_ID"),
      secretAccessKey: env("AWS_ACCESS_SECRET"),
      region: env("AWS_REGION"),
      params: { ACL: env("AWS_ACL", "public-read"), Bucket: env("AWS_BUCKET") },
    },
    actionOptions: { upload: {}, uploadStream: {}, delete: {} },
  },
},
```

Add CSP for image domains in `config/middlewares.ts` → `strapi::security` config:
```ts
contentSecurityPolicy: {
  useDefaults: true,
  directives: {
    "connect-src": ["'self'", "https:"],
    "img-src": ["'self'", "data:", "blob:", "res.cloudinary.com", "your-bucket.s3.amazonaws.com"],
    "media-src": ["'self'", "data:", "blob:", "res.cloudinary.com"],
    upgradeInsecureRequests: null,
  },
},
```

---

## Strapi Admin Customization

### Rebrand admin panel (`src/admin/app.tsx`):
```ts
export default {
  config: {
    locales: ["en", "th"],
    theme: {
      light: {
        colors: {
          primary100: "#f0f4ff",
          primary200: "#d9e2ff",
          primary500: "#4945FF",
          primary600: "#271FE0",
          primary700: "#1a14b3",
          buttonPrimary500: "#4945FF",
          buttonPrimary600: "#271FE0",
        },
      },
    },
    translations: {
      en: {
        "app.components.LeftMenu.navbrand.title": "My CMS",
        "app.components.LeftMenu.navbrand.workplace": "Admin Panel",
      },
    },
    head: { favicon: "/favicon.ico" },
    auth: { logo: "/logo.png" },
    menu: { logo: "/logo.png" },
  },
  bootstrap(app) {
    // Inject custom component into edit view
    app.injectContentManagerComponent("editView.right-links", "before", {
      name: "preview-button",
      Component: () => import("./extensions/PreviewButton").then((m) => ({ default: m.PreviewButton })),
    });
  },
};
```
