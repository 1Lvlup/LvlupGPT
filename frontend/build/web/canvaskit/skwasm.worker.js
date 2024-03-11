"use strict"; // Use strict mode to enforce better error handling and prevent some actions from being taken.

var Module = {}; // Initialize an empty object to hold module information.

var ENVIRONMENT_IS_NODE =  // Determine if the code is running in a Node.js environment.
    typeof process === "object" &&
    typeof process.versions === "object" &&
    typeof process.versions.node === "string";

if (ENVIRONMENT_IS_NODE) {
    // If in Node.js environment, import required modules and assign them to global variables.
    var nodeWorkerThreads = require("worker_threads");
    var parentPort = nodeWorkerThreads.parentPort;

    parentPort.on("message", data => {
        onmessage({ data: data }); // Attach an event listener for incoming messages and pass the data to the onmessage function.
    });

    var fs = require("fs");
    Object.assign(global, {
        self: global,
        require: require,
        Module: Module,
        location: { href: __filename },
        Worker: nodeWorkerThreads.Worker,
        importScripts: function (f) {
            (0, eval)(fs.readFileSync(f, "utf8") + "//# sourceURL=" + f);
        },
        postMessage: function (msg) {
            parentPort.postMessage(msg);
        },
        performance: global.performance || { now: function () { return Date.now(); } }
    });
}

// ... Rest of the code ...
