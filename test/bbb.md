---
title: "bbb"
summary: ""
tags: []
categories: [test]
draft: 
date: 2026-06-23T20:05:27+09:00
lastmod: 
---

```sh
sudo lsof -i :<port num>

# dockerで使用しているポートの大きいものを調べる
docker ps --format '{{.ID}} {{.Names}} {{.Ports}}' | awk -F'[ ,]+' '{for(i=3;i<=NF;i++){if($i~/->/){split($i,a,":");split(a[2],b,"->");print $1,$2,b[1];break}}}' | sort -k3n -u | tail -n6

telnet <hostname or IP> <port num>
```

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
