---
title: "latex-test"
summary: ""
tags: []
draft: 
date: 2026-06-26T15:30:36+09:00
lastmod: 
---

- $K_{\text{client}} = (g^b \bmod p)^a \bmod p$
- $K_{\text{client}} = (g^b)^a \bmod p$
- $K_{\text{client}} = g^{ab} \bmod p$
- $K_{\text{server}} = (g^a \bmod p)^b \bmod p$
- $K_{\text{server}} = g^{ab} \bmod p$
- $K_{\text{server}} = K_{\text{client}}$



$A \equiv B \pmod p \implies A^a \equiv B^a \pmod p$  

証明(1)：  
$AC = (B + kp)(D + mp)$  
$AC = BD + Bmp + kpD + kmp^2$  
$AC = BD + p(Bm + kD + kmp)$  
$AC \equiv BD \pmod p$  
$AA \equiv BB \pmod p$  

この法則を使い、以下の等式が求められる

- $x \equiv (x \bmod p) \pmod p$
- $x^a \equiv (x \bmod p)^a \pmod p$
- $x^a \bmod p = (x \bmod p)^a \bmod p$

