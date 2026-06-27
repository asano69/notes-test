// イベント委譲の設計パターンを使用
// Single delegated listener for all interactive elements

import { initCopyCode } from "./copy-code.js";
import { initSidebarToggle } from "./sidebar-toggle.js";
import { initSectionSearch } from "./section-search.js";

document.addEventListener("DOMContentLoaded", () => {
  initCopyCode();
  initSidebarToggle();
  initSectionSearch();
});
