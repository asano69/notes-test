// Sidebar collapses on desktop, or slides in as an overlay on mobile.
// The breakpoint below must match the one used in main.css.
const DESKTOP_QUERY = "(min-width: 768px)";
const TOGGLE_BTN_SELECTOR = "#sidebar-toggle";

function isSidebarOpen() {
  return window.matchMedia(DESKTOP_QUERY).matches
    ? !document.body.classList.contains("sidebar-collapsed")
    : document.body.classList.contains("sidebar-mobile-open");
}

function syncAriaExpanded(btn) {
  btn.setAttribute("aria-expanded", String(isSidebarOpen()));
}

export function initSidebarToggle() {
  const btn = document.querySelector(TOGGLE_BTN_SELECTOR);
  if (btn) syncAriaExpanded(btn);

  document.addEventListener("click", (e) => {
    const btn = e.target.closest(TOGGLE_BTN_SELECTOR);
    if (!btn) return;

    const toggleClass = window.matchMedia(DESKTOP_QUERY).matches
      ? "sidebar-collapsed"
      : "sidebar-mobile-open";
    document.body.classList.toggle(toggleClass);
    syncAriaExpanded(btn);
  });
}
