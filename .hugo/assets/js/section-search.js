const SEARCH_INPUT_SELECTOR = "#section-search";
const NAV_ITEM_SELECTOR = ".sidebar nav li";

export function initSectionSearch() {
  const search = document.querySelector(SEARCH_INPUT_SELECTOR);
  if (!search) return;

  search.addEventListener("input", () => {
    const q = search.value.toLowerCase();
    document.querySelectorAll(NAV_ITEM_SELECTOR).forEach((li) => {
      li.hidden = !li.textContent.toLowerCase().includes(q);
    });
  });
}
