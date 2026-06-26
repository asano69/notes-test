import { handleCopyCode } from "./copy-code.js";

// イベント委譲の設計パターンを使用。
// Single delegated listener for all interactive elements
document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener("click", (e) => {
    if (e.target.matches(".copy-btn")) handleCopyCode(e.target);
    // Add future button handlers here
  });
});
