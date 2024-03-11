/**
 * Minified by jsDelivr using Terser v5.3.0.
 * Original file: /npm/toastify-js@1.9.3/src/toastify.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */

/*!
 * Toastify js 1.9.3
 * https://github.com/apvarun/toastify-js
 * @license MIT licensed
 *
 * Copyright (C) 2018 Varun A P
 */

// Create a new instance of Toastify
var o = function(t) {
  return new o.lib.init(t);
};

// Helper function to get the offset value
function i(t, o) {
  return o.offset[t]
    ? isNaN(o.offset[t])
      ? o.offset[t]
      : o.offset[t] + "px"
    : "0px";
}

// Helper function to check if a class exists in an element
function s(t, o) {
  return (
    !(!t || "string" != typeof o) &&
    !!("" !==
      (t.className &&
        t.className
          .trim()
          .split(/\s+/gi)
          .indexOf(o)) > -1)
  );
}

// Toastify constructor
o.lib = o.prototype = {
  // Version of Toastify
  toastify: "1.9.3",
  // Initialize Toastify
  constructor: o,
  init: function(t) {
    // Set default options
    this.options = {};
    this.toastElement = null;
    this.options.text = t.text || "Hi there!";
    this.options.node = t.node;
    this.options.duration =
      0 === t.duration
        ? 0
        : t.duration || 3e3; // Duration in milliseconds
    this.options.selector = t.selector;
    this.options.callback = t.callback || function() {};
    this.options.destination = t.destination;
    this.options.newWindow = t.newWindow || !1;
    this.options.close = t.close || !1;
    this.options.gravity =
      "bottom" === t.gravity
        ? "toastify-bottom"
        : "toastify-top";
    this.options.positionLeft = t.positionLeft || !1;
    this.options.position = t.position || "";
    this.options.backgroundColor = t.backgroundColor;
    this.options.avatar = t.avatar || "";
    this.options.className = t.className || "";
    this.options.stopOnFocus =
      void 0 === t.stopOnFocus || t.stopOnFocus;
    this.options.onClick = t.onClick;
    this.options.offset = t.offset || { x: 0, y: 0 };
  },
  // Build the toast element
  buildToast: function() {
    if (!this.options) throw "Toastify is not initialized";
    var t = document.createElement("div");
    if (
      // Set the class for the toast element
      (t.className =
        "toastify on " + this.options.className),
      this.options.position
        ? (t.className += " toastify-" + this.options.position)
        : !0 === this.options.positionLeft
        ? (t.className += " toastify-left")
        : t.className += " toastify-right",
      // Set the gravity for the toast element
      (t.className += " " + this.options.gravity),
      this.options.backgroundColor &&
        (t.style.background = this.options.backgroundColor),
      this.options.node &&
        this.options.node.nodeType === Node.ELEMENT_NODE
    )
      t.appendChild(this.options.node);
    else if (t.innerHTML = this.options.text, "" !== this.options.avatar) {
      var o = document.createElement("img");
      o.src = this.options.avatar,
        o.className = "toastify-avatar",
        // Insert the avatar element
        "left" == this.options.position ||
          !0 === this.options.positionLeft
          ? t.appendChild(o)
          : t.insertAdjacentElement("afterbegin", o);
    }
    if (
      // Add close button if close option is true
      !0 === this.options.close
    ) {
      var s = document.createElement("span");
      s.innerHTML = "&#10006;",
        s.className = "toast-close",
        s.addEventListener(
          "click",
          function(t) {
            t.stopPropagation(),
              this.removeElement(this.toastElement),
              window.clearTimeout(
                this.toastElement.timeOutValue
              );
          }.bind(this)
        );
      var n =
        window.innerWidth > 0
          ? window.innerWidth
          : screen.width;
      // Set the position of the close button
      ("left" == this.options.position ||
        !0 === this.options.positionLeft) &&
        n > 360
        ? t.insertAdjacentElement("afterbegin", s)
        : t.appendChild(s);
    }
    // Add event listeners for stopOnFocus option
    if (
      this.options.stopOnFocus &&
      this.options.duration > 0
    ) {
      var e = this;
      t.addEventListener(
        "mouseover",
        function(o) {
          window.clearTimeout(t.timeOutValue);
        }
      ),
        t.addEventListener(
          "mouseleave",
          function() {
            t.timeOutValue = window.setTimeout(
              function() {
                e.removeElement(t);
              },
              e.options.duration
            );
