// Copyright 2014 The Flutter Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Initialize the Flutter loader with a null value
_flutter.loader = null;

// Self-invoking anonymous function with strict mode enabled
(function () {
  "use strict";

  // Get the base URI of the document
  const baseUri = ensureTrailingSlash(getBaseURI());

  // Function to get the base URI of the document
  function getBaseURI() {
    const base = document.querySelector("base");
    return base ? base.getAttribute("href") || "" : "";
  }

  // Function to ensure a trailing slash in the URI
  function ensureTrailingSlash(uri) {
    if (uri === "") {
      return uri;
    }
    return uri.endsWith("/") ? uri : `${uri}/`;
  }

  /**
   * @typedef {{
   *   createScriptURL: (url: string) => string,
   * }}
   */
  let TrustedTypesPolicy; // Type definition for TrustedTypesPolicy

  /**
   * @param {[RegExp]} validPatterns
   * @param {string} policyName
   */
  class FlutterTrustedTypesPolicy {
    // Class to create a Trusted Types policy
    constructor(validPatterns, policyName = "flutter-js") {
      const patterns = validPatterns || [/\\.js$/];
      if (window.trustedTypes) {
        // Create a Trusted Types policy if the browser supports it
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
    // Class to load the Flutter Service Worker

    #trustedTypesPolicy; // Instance variable to store the TrustedTypesPolicy

    setTrustedTypesPolicy(policy) {
      // Setter for the TrustedTypesPolicy
      this.#trustedTypesPolicy = policy;
    }

    /**
     * @param {*} settings
     * @returns {Promise<void>}
     */
    async loadServiceWorker(settings) {
      // Asynchronous function to load the Service Worker
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
      // Function to get the new Service Worker
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
        // Functionality to update the Service Worker is incomplete
        return;
      }
    }

    /**
     * @param {ServiceWorker} newServiceWorker
     * @returns {Promise<void>}
     */
    async #_waitForServiceWorkerActivation(newServiceWorker) {
      // Function to wait for the new Service Worker to activate
      return new Promise((resolve) => {
        newServiceWorker.addEventListener("statechange", () => {
          if (newServiceWorker.state === "activated") {
            resolve();
          }
        });
      });
    }
  }

})();

