const CACHE = "cache"

self.addEventListener("activate", (event) => {
  const cacheWhitelist = [CACHE]

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName)
          }
        })
      )
    })
  )
})

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => {
      cache.addAll([
        "/static/css/reset.css",
        "/static/css/base.css",
        "/static/css/index.css",
        "/static/img/loader.svg",
        "/static/img/favicon.png",
        "/static/js/external/handlebars.min.js",
        "/static/js/app.js",
        "/static/js/library/api.js",
        "/static/js/library/translate.js",
        "/static/js/library/utils.js",
        "/static/js/widgets/centered.js",
        "/static/js/widgets/loader.js",
      ])
    })
  )
})

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response) {
        return response
      }

      return fetch(event.request).then((response) => {
        if (!response || response.status !== 200 || response.type !== "basic" || response.url.indexOf("api") >= 0) {
          return response
        }

        caches.open(CACHE).then((cache) => {
          cache.put(event.request, response)
        })

        return response
      })
    })
  )
})
