// Fallback for when the Clipboard API is unavailable (e.g. plain HTTP)
function copyText(text) {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text);
  }
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
  return Promise.resolve();
}

export function handleCopyCode(btn) {
  const code = btn.nextElementSibling.querySelector("code");
  copyText(code.textContent.trim()).then(() => {
    btn.textContent = "Copied!";
    setTimeout(() => {
      btn.textContent = "Copy";
    }, 2000);
  });
}
