function copyCode(btn) {
  const code = btn.nextElementSibling.querySelector("code");
  navigator.clipboard.writeText(code.innerText).then(() => {
    btn.textContent = "Copied!";
    setTimeout(() => {
      btn.textContent = "Copy";
    }, 2000);
  });
}
