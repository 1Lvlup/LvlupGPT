// Copyright 2014 The Flutter Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

_flutter.loader = null;

(function () {
  "use strict";

  const baseUri = ensureTrailingSlash(getBaseURI());

  function getBaseURI() {
    const base = document.querySelector("base");
    return base ? base.getAttribute("href") || "" : "";
  }

  function ensureTrailingSlash(uri) {
    if (uri === "") {
      return uri;
    }
    return uri.endsWith("/") ? uri : `${uri}/`;
  }

  /**
   * @param {Promise<any>} promise
   * @param {number} duration
   * @param {string} debugName
   * @returns {Promise<any>}
   */
  async function timeout(promise, duration, debugName) {
    if (duration < 0) {
      return promise;
    }
    let timeoutId;
    const _clock = new Promise((_, reject) => {
      timeoutId = setTimeout(() => {
        reject(
          new Error(
            `${debugName} took more than ${duration}ms to resolve. Moving on.`,
            timeout
          )
        );
      }, duration);
    });

    return Promise.race([promise, _clock]).finally(() => {
      clearTimeout(timeoutId);
    });
  }

  /**
   * @typedef {{
   *   createScriptURL: (url: string) => string,
   * }}
   */
  let TrustedTypesPolicy;

  /**
   * @param {[RegExp]} validPatterns
   * @param {string} policyName
   */
  class FlutterTrustedTypesPolicy {
    constructor(validPatterns, policyName = "flutter-js") {
      const patterns = validPatterns || [/\\.js$/];
      if (window.trustedTypes) {
        this.policy = trustedTypes.createPolicy(policyName, {
          createScriptURL: (url) => {
            const parsed = new URL(url, window.location);
            const file = parsed.pathname.split("/").pop();
            const matches = patterns.some((pattern) => pattern.test(file));
            if (matches) {
              return parsed.toString();
            }
            console.error(
              "URL rejected by TrustedTypes policy",
              policyName, ":", url, "(download prevented)"
            );
          },
        });
      }
    }
  }

  /**
   * @see: https://developers.google.com/web/fundamentals/primers/service-workers
   */
  class FlutterServiceWorkerLoader {
    /**
     * @type {TrustedTypesPolicy | undefined}
     */
    #trustedTypesPolicy;

    setTrustedTypesPolicy(policy) {
      this.#trustedTypesPolicy = policy;
    }

    /**
     * @param {*} settings
     * @returns {Promise<void>}
     */
    async loadServiceWorker(settings) {
      if (settings == null) {
        console.debug("Null serviceWorker configuration. Skipping.");
        return Promise.resolve();
      }

      if (!("serviceWorker" in navigator)) {
        let errorMessage = "Service Worker API unavailable.";
        if (!window.isSecureContext) {
          errorMessage += "\nThe current context is NOT secure.";
          errorMessage += "\nRead more: https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts";
        }
        return Promise.reject(new Error(errorMessage));
      }

      const {
        serviceWorkerVersion,
        serviceWorkerUrl = `${baseUri}flutter_service_worker.js?v=${serviceWorkerVersion}`,
        timeoutMillis = 4000,
      } = settings;

      let url = serviceWorkerUrl;
      if (this.#trustedTypesPolicy != null) {
        url = this.#trustedTypesPolicy.createScriptURL(url);
      }

      const serviceWorkerActivation = navigator.serviceWorker
        .register(url)
        .then(this.#_getNewServiceWorker.bind(this))
        .then(this.#_waitForServiceWorkerActivation.bind(this));

      return timeout(
        serviceWorkerActivation,
        timeoutMillis,
        "prepareServiceWorker"
      );
    }

    /**
     * @param {ServiceWorkerRegistration} serviceWorkerRegistrationPromise
     * @returns {Promise<ServiceWorker>}
     */
    async #_getNewServiceWorker(
      serviceWorkerRegistrationPromise
    ) {
      const reg = await serviceWorkerRegistrationPromise;

      if (
        !reg.active &&
        (reg.installing || reg.waiting)
      ) {
        console.debug(
          "Installing/Activating first service worker."
        );
        return reg.installing || reg.waiting;
      } else if (
        !reg.active.scriptURL.endsWith(
          serviceWorkerVersion
        )
      ) {
        console.debug(
          "Updating service worker."
        );
        return
