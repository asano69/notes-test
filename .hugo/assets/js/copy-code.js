function copyText(text) {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text);
  }
  // Fallback for when the Clipboard API is unavailable (e.g. plain HTTP)
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
  return Promise.resolve();
}

export function initCopyCode() {
  document.addEventListener("click", (e) => {
    if (!e.target.matches(".copy-btn")) return;
    const code = e.target.nextElementSibling.querySelector("code");
    copyText(code.textContent.trim()).then(() => {
      e.target.textContent = "Copied!";
      setTimeout(() => {
        e.target.textContent = "Copy";
      }, 2000);
    });
  });
}
