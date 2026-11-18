# Custom Strapi Plugin Development

## Scaffold a Plugin

```bash
cd backend
npx @strapi/sdk-plugin@latest init src/plugins/my-plugin
```

Generated structure:
```
src/plugins/my-plugin/
├── admin/
│   └── src/
│       ├── index.tsx          # Admin panel registration
│       └── pages/
│           └── HomePage.tsx   # Plugin admin UI
├── server/
│   ├── src/
│   │   ├── index.ts           # Server entry point
│   │   ├── controllers/
│   │   ├── routes/
│   │   ├── services/
│   │   └── content-types/    # Plugin-owned content types
│   └── package.json
├── package.json
└── strapi-server.ts           # Plugin export
```

---

## Plugin Server Entry (`strapi-server.ts`)

```ts
export default {
  register({ strapi }) {
    // runs at startup — register services, middlewares, etc.
  },
  bootstrap({ strapi }) {
    // runs after all plugins registered — safe to call other services
  },
  destroy({ strapi }) {
    // cleanup on shutdown
  },
  controllers: {
    myController: require("./server/src/controllers/my-controller"),
  },
  routes: {
    "content-api": {
      type: "content-api",
      routes: [
        { method: "GET", path: "/my-plugin/items", handler: "myController.list", config: { auth: false } },
      ],
    },
    admin: {
      type: "admin",
      routes: [
        { method: "GET", path: "/my-plugin/settings", handler: "myController.getSettings" },
      ],
    },
  },
  services: {
    myService: require("./server/src/services/my-service"),
  },
  contentTypes: {},
};
```

---

## Plugin Service Pattern

```ts
// server/src/services/my-service.ts
export default ({ strapi }) => ({
  async getSettings() {
    const pluginStore = strapi.store({ type: "plugin", name: "my-plugin" });
    return pluginStore.get({ key: "settings" });
  },
  async setSettings(settings: Record<string, unknown>) {
    const pluginStore = strapi.store({ type: "plugin", name: "my-plugin" });
    return pluginStore.set({ key: "settings", value: settings });
  },
});
```

Access from anywhere: `strapi.plugin("my-plugin").service("myService")`

---

## Plugin Store (Persistent Settings)

```ts
// Persist plugin config to the database (survives restarts)
const store = strapi.store({ type: "plugin", name: "my-plugin" });

// Set
await store.set({ key: "apiKey", value: "abc123" });

// Get
const apiKey = await store.get({ key: "apiKey" });

// Delete
await store.delete({ key: "apiKey" });
```

---

## Admin Panel UI (`admin/src/index.tsx`)

```tsx
import { prefixPluginTranslations } from "@strapi/helper-plugin";
import pluginId from "./pluginId";
import HomePage from "./pages/HomePage";

export default {
  register(app: any) {
    app.addMenuLink({
      to: `/plugins/${pluginId}`,
      icon: () => <span>🔌</span>,
      intlLabel: { id: `${pluginId}.plugin.name`, defaultMessage: "My Plugin" },
      Component: async () => ({ default: (await import("./pages/HomePage")).default }),
    });

    app.registerPlugin({
      id: pluginId,
      initializer: () => null,
      isReady: true,
      name: "my-plugin",
    });
  },

  async registerTrads({ locales }: { locales: string[] }) {
    // load translation files
    return [];
  },
};
```

---

## Register Plugin in Strapi

```ts
// config/plugins.ts
export default () => ({
  "my-plugin": {
    enabled: true,
    resolve: "./src/plugins/my-plugin",
  },
});
```

---

## Custom Field Plugin

Register a custom field type (e.g., color picker):

```ts
// admin/src/index.tsx — in register()
app.customFields.register({
  name: "color",
  pluginId: pluginId,
  type: "string",
  intlLabel: { id: "color.label", defaultMessage: "Color" },
  intlDescription: { id: "color.description", defaultMessage: "Pick a color" },
  components: {
    Input: async () => ({ default: (await import("./components/ColorInput")).default }),
  },
  options: { base: [], advanced: [], validator: () => ({}) },
});
```

---

## Calling Plugin Service from Another Plugin/API

```ts
// From a lifecycle hook or custom controller:
const settings = await strapi.plugin("my-plugin").service("myService").getSettings();
```

---

## Publishing to npm

```bash
cd src/plugins/my-plugin
npm run build   # compiles admin + server
npm publish --access public
```

Install in another Strapi project:
```bash
npm install strapi-plugin-my-plugin
# config/plugins.ts → enable: true
```
