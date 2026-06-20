// Copy text to the clipboard, falling back to execCommand when the
// Clipboard API is unavailable (e.g. plain HTTP on a non-localhost host).
function copyText(text) {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text);
  }
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed"; // keep it off-screen, avoid scrolling
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
  return Promise.resolve();
}

// Add a copy button to every code block.
document.querySelectorAll("pre").forEach((pre) => {
  const code = pre.querySelector("code");
  if (!code) return;

  const button = document.createElement("button");
  button.type = "button";
  button.className = "copy-button";
  button.textContent = "Copy";
  button.addEventListener("click", () => {
    copyText(code.textContent.trim()).then(() => {
      button.textContent = "Copied!";
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1500);
    });
  });

  pre.appendChild(button);
});
