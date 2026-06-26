---
title: "bbb"
summary: ""
tags: []
categories: [test]
draft: 
date: 2026-06-23T20:05:27+09:00
lastmod: 
---


bbbb [aaa](/test/aaa/)


```js
// assets/js/copy-code.js
function copyCode(btn) {
  const code = btn.nextElementSibling.querySelector("code");
  navigator.clipboard.writeText(code.innerText).then(() => {
    btn.textContent = "Copied!";
    setTimeout(() => { btn.textContent = "Copy"; }, 2000);
  });
}
```
