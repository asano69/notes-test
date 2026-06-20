---
title: "SoftEther VPN Client"
summary:
tags: []
categories: [sample]
draft:
date: 2025-10-26T11:52:26+09:00
lastmod:
---

 
 # SoftEther VPN Client

- Windows：VPNマネージャが使える。
- iPhone：SSTPコネクト、標準のVPN機能（但し不安定）
- Linux：~~network-manager-l2tp~~ openvpn
	- NetworkManager + openvpn拡張

WindowsのVPNマネージャの場合
- プロトコルはSoftetherでポートは5555を使う。仮想HUB名はDEFAULT
- NAT-Tを設定すると、Softether社のVPSを経由することになる。なので使わない。

iPhoneの場合
- SSTPコネクトを使う。サーバは、softether-server.1yo.uk、ホスト名は空白、ポートは5555、TLSサーバ検証はオン、仮想HUBはDEFAULT、コネクション数は３、UDP高速化機能はオン、NAT-Tは使わない。

Androidの場合
- OpenVPN Clientを使う。


### Linux - SoftEtherのvpcmdを使う場合
- この方法は結局、成功しなかった。VPNを有効化するとインターネットに接続できなくなる。
```shell
# SoftEtherの公式サイトから最新版のクライアントをダウンロードする。
sudo /usr/local/vpnclient/vpncmd # コネクションの作成

# AccountCreate Connect-XXX /SERVER:softether-server.1yo.uk:5555 /HUB:DEFAULT /USERNAME:asano /NICNAME:vNIC-XXX
# AccountPasswordSet Connect-XXX /PASSWORD:****** /TYPE:standard
# AccountConnect Connect-XXX
# AccountGet Connect-XXX

dhclient vpn_vnic-xxx # IPv4を取得
resolvectl status # DNSサーバの確認
```

参考：
```cardlink
url: https://cgbeginner.net/ubuntu-softether-vpn-client/
title: "Ubuntu(Linux)でSoftEther VPNクライアント構築 詳細メモ"
description: "VPN(Virtual Private Network)は、仮想的な通信トンネルを構成したプライベートネットワークのこと。通信内容を暗号化しつつ、仮想的にネットワークを接続できる技術です。VPNを使って通信の安全性を高めたり、自宅にVPNサ..."
host: cgbeginner.net
image: https://cgbeginner.net/wp-content/uploads/2023/01/softether-vpn.png
favicon: https://cgbeginner.net/wp-content/uploads/2016/09/cropped-favicon_512-32x32.png

```

### ❌ Linux - Network Managerを使う場合
- Lubuntu LxQtで試した。GNOME系ならもっと簡単にできたかもしれない。
- L2TP/IPSecプロトコルを使う。Linuxでは比較的安定していた。あらかじめ、L2TP/IPSecプロトコルに対応させてSoftetherServerを構築しておく。
- 接続設定をつくるときポート番号を指定する必要はなかった。L2TP/IPSecではポートが決まっているからかもしれない。
```text title=NeteorkManager fold
Type: Password
User name: asano
Password: ******, すべてのユーザーのパスワードを保存
IPSec Setting:
	Type PSK
	Pre-Shared key: ******
```
```shell
apt install network-manager-l2tp
# GUIで、L2TP/IPSecのプロファイルを作成し、適用する。
# nm-connection-editor を起動し、パスワードの保存方法を『すべてのユーザーのパスワードを保存』に変更する。
# パスワード入力欄のすぐそばにある。
journalctl -fu NetworkManager # つながらない場合、ログを確認する

# 以下のようにVPNの事前共有鍵(PSK)を記述：IPsec PSKの例
# nano /etc/ipsec.secrets
cat /etc/ipsec.secrets
echo '64.110.97.156 : PSK "******"' >>/etc/ipsec.secrets
# 64.110.97.156 はVPNサーバーのIPに置き換え
sudo chmod 600 /etc/ipsec.secrets
sudo chown root:root /etc/ipsec.secrets
sudo nmcli connection reload # Network Mangerの再読込
sudo nmcli connection up "softether-vpn-server"
```

### ✅ Linux - Softether OpenVPN Client
```shell
# Network Managerでプロファイルをインポートできるようにする
sudo apt install network-manager-openvpn-gnome
```
- プロファイルをインポート後、ユーザ名とパスワードを入力
- パスワードの保存方法を『すべてのユーザーのパスワードを保存』に変更する。
