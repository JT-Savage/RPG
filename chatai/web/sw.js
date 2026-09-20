/*
 * Service worker for Private Character Chat.
 *
 * Its only job is to make the app installable and survive a flaky
 * Wi-Fi hop: the shell (HTML/CSS/JS/icons) is cached so the app opens
 * instantly from the home screen, while everything that carries actual
 * chat data always goes to the network. Nothing is ever sent anywhere
 * but this same origin — the worker has no push, no sync, no analytics.
 *
 * Note: browsers only register service workers on a secure context
 * (https:// or localhost). Over plain http:// on a LAN address the app
 * still works and still installs to the iOS home screen, just without
 * this offline layer. See the README's HTTPS section.
 */
"use strict";

const VERSION = "v1";
const SHELL_CACHE = `chatai-shell-${VERSION}`;
const MEDIA_CACHE = `chatai-media-${VERSION}`;

const SHELL_ASSETS = [
  "/",
  "/offline.html",
  "/manifest.webmanifest",
  "/static/style.css",
  "/static/app.js",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
  "/static/icons/maskable-512.png",
  "/static/icons/apple-touch-icon-180.png",
  "/static/icons/favicon-32.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL_CACHE);
    // One unreachable asset (or a passcode redirect on "/") shouldn't fail
    // the whole install and leave the app permanently un-cached.
    await Promise.allSettled(SHELL_ASSETS.map(async (asset) => {
      const response = await fetch(asset, { cache: "reload" });
      if (response.ok && !response.redirected) await cache.put(asset, response);
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== SHELL_CACHE && k !== MEDIA_CACHE)
            .map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Lets a freshly loaded page activate an updated worker without a second reload.
self.addEventListener("message", (event) => {
  if (event.data === "skip-waiting") self.skipWaiting();
});

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const response = await fetch(request);
    if (response && response.ok && request.method === "GET") {
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    const cached = await cache.match(request, { ignoreSearch: true });
    if (cached) return cached;
    throw err;
  }
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // Never touch the API, and never buffer a streamed reply.
  if (url.pathname.startsWith("/api/")) return;
  if ((request.headers.get("accept") || "").includes("text/event-stream")) return;

  // Page loads: fresh if we can reach the server, otherwise the cached
  // shell, otherwise a short "can't reach your server" page.
  if (request.mode === "navigate") {
    event.respondWith((async () => {
      try {
        return await fetch(request);
      } catch (err) {
        const cache = await caches.open(SHELL_CACHE);
        return (await cache.match("/"))
            || (await cache.match("/offline.html"))
            || new Response("Offline", { status: 503, headers: { "Content-Type": "text/plain" } });
      }
    })());
    return;
  }

  // Avatars: cheap to re-fetch, nice to have offline.
  if (url.pathname.startsWith("/media/")) {
    event.respondWith(networkFirst(request, MEDIA_CACHE));
    return;
  }

  if (url.pathname.startsWith("/static/") || url.pathname === "/manifest.webmanifest") {
    event.respondWith(networkFirst(request, SHELL_CACHE));
  }
});
