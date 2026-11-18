# Real-Time Patterns with Strapi

## Option 1: Polling (Simplest)

For low-frequency updates, React Query's `refetchInterval` is enough:

```ts
// Refresh every 10 seconds
useQuery({
  queryKey: ["notifications"],
  queryFn: fetchNotifications,
  refetchInterval: 10_000,
  refetchIntervalInBackground: false, // pause when tab is hidden
});
```

---

## Option 2: Server-Sent Events (SSE) — Strapi Custom Endpoint

SSE is one-directional (server → client), lightweight, and works through proxies.

### Strapi SSE endpoint:

```ts
// src/api/event-stream/routes/sse.ts
export default {
  routes: [
    { method: "GET", path: "/events/stream", handler: "event-stream.stream", config: { auth: false } },
  ],
};

// src/api/event-stream/controllers/event-stream.ts
export default {
  async stream(ctx) {
    ctx.set({
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
    });
    ctx.status = 200;

    // Send initial ping
    ctx.res.write("data: connected\n\n");

    // Push updates from an EventEmitter or lifecycle hooks
    const send = (data: unknown) => ctx.res.write(`data: ${JSON.stringify(data)}\n\n`);

    // Register listener
    strapi.eventHub.on("entry.publish", send);

    // Cleanup on disconnect
    ctx.req.on("close", () => {
      strapi.eventHub.off("entry.publish", send);
    });

    // Keep alive (nginx times out idle connections after 60s by default)
    const keepAlive = setInterval(() => ctx.res.write(": keep-alive\n\n"), 25_000);
    ctx.req.on("close", () => clearInterval(keepAlive));

    // Never resolve — the stream stays open
    await new Promise(() => {});
  },
};
```

### React client:

```ts
// src/hooks/useEventStream.ts
import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";

export function useEventStream(queryKeysToInvalidate: string[][]) {
  const qc = useQueryClient();

  useEffect(() => {
    const es = new EventSource(`${import.meta.env.VITE_STRAPI_URL}/api/events/stream`);

    es.onmessage = (e) => {
      if (e.data === "connected") return;
      queryKeysToInvalidate.forEach((key) => qc.invalidateQueries({ queryKey: key }));
    };

    es.onerror = () => {
      es.close();
      // Auto-reconnect after 5s
      setTimeout(() => es.close(), 5_000);
    };

    return () => es.close();
  }, []);
}
```

---

## Option 3: WebSockets via Socket.io Plugin

```bash
npm install strapi-plugin-io
```

```ts
// config/plugins.ts
export default () => ({
  io: {
    enabled: true,
    config: {
      IOServerOptions: { cors: { origin: "http://localhost:5173", methods: ["GET", "POST"] } },
      contentTypes: {
        post: { enabled: true, populate: "*" }, // auto-emit on CRUD
      },
      events: [
        { name: "connection", handler: "global::io.connection" },
      ],
    },
  },
});
```

### React client (socket.io-client):

```bash
npm install socket.io-client
```

```ts
// src/lib/socket.ts
import { io } from "socket.io-client";

export const socket = io(import.meta.env.VITE_STRAPI_URL, {
  autoConnect: false,
  transports: ["websocket"],
});

// src/hooks/useSocket.ts
import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { socket } from "@/lib/socket";

export function usePostUpdates() {
  const qc = useQueryClient();

  useEffect(() => {
    socket.connect();

    socket.on("post:create", () => qc.invalidateQueries({ queryKey: ["posts"] }));
    socket.on("post:update", (post) => {
      qc.setQueryData(["post", post.slug], post);
      qc.invalidateQueries({ queryKey: ["posts"] });
    });
    socket.on("post:delete", () => qc.invalidateQueries({ queryKey: ["posts"] }));

    return () => {
      socket.off("post:create");
      socket.off("post:update");
      socket.off("post:delete");
      socket.disconnect();
    };
  }, []);
}
```

---

## Option 4: Webhooks → External Queue → Push

For production real-time (e.g., notifications to many clients):

```
Strapi lifecycle → webhook → serverless fn → Redis pub/sub → WebSocket server → clients
```

1. Strapi fires webhook on `entry.publish`
2. Serverless function receives it, publishes to Redis channel
3. Dedicated WebSocket server (separate from Strapi) subscribes and pushes to connected clients

This decouples real-time infrastructure from Strapi's Node.js process.

---

## Nginx Configuration for SSE & WebSockets

```nginx
location /api/events/ {
  proxy_pass http://localhost:1337;
  proxy_http_version 1.1;
  proxy_set_header Connection "";          # SSE: no upgrade
  proxy_buffering off;                     # SSE: disable buffering
  proxy_read_timeout 3600s;               # keep SSE connection alive
  chunked_transfer_encoding on;
}

location /socket.io/ {
  proxy_pass http://localhost:1337;
  proxy_http_version 1.1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";   # WebSocket upgrade
  proxy_read_timeout 3600s;
}
```
