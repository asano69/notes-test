---
title: "findコマンドサンプル"
summary:
tags: []
categories: [sample]
draft:
date: 2025-11-17T15:12:00+09:00
lastmod:
---

npm-lan_defaultをnpm_lan_brに書き換え
```
find . \( -name "compose.yaml" -o -name "docker-compose.yml" \) \
  -exec sed -i 's/npm-lan_default/npm_lan_br/g' {} +

find . \( -name "compose.yaml" -o -name "docker-compose.yml" \) \
  -exec sed -i 's/npm-wan_default/npm_wan_br/g' {} +

find . -maxdepth 2 -mindepth 2 -name "docker-compose.yml" \
  -exec bash -c 'mv "$0" "$(dirname "$0")/compose.yaml"' {} \;

```


gitignore
```
# まずすべて無視
*
# ディレクトリ自体は無視しない
!*/
# compose.yaml は例外的に管理対象
!**/compose.yaml
```

container_name が無いサービスだけに container_name: <サービス名> を自動付与するワンライナー。
```
find /root/stacks -type f -name "compose.yaml" -exec sh -c '
  yq -y -i ".services |= with_entries(
    if (.value.container_name == null) 
      then .value.container_name = .key | .
      else . end
  )" "$1"
' _ {} \;

```

docker のcompose yamlを整理しているのだが、つぎのワンライナーを考えて 
/root/stacksにある複数のフォルダの中のcompose.yamlのなかの、restart: alwaysのものをrestart: unless-stoppedに書き換え
```
find /root/stacks -type f -name "compose.yaml" -exec sh -c '
  yq -y -i ".services |= with_entries(
    if .value.restart == \"always\" 
      then .value.restart = \"unless-stopped\" | . 
      else . end
  )" "$1"
' _ {} \;

```

docker のcompose yamlを整理しているのだが、つぎのワンライナーを考えて 
/root/stacksにある複数のフォルダの中のcompose.yamlのなかの、バインドマウントしているcompose.yamlの一覧
```
find /root/stacks -type f -name "compose.yaml" -exec sh -c '
  file="$1"
  if yq ".services[].volumes[]? | select(test(\"^/\"))" "$file" >/dev/null 2>&1; then
    echo "$file"
  fi
' _ {} \;
```

docker のcompose yamlを整理しているのだが、つぎのワンライナーを考えて 
/root/stacksにある複数のフォルダの中のcompose.yamlのなかの、バインドマウントしているサービス名の一覧
```
find /root/stacks -type f -name "compose.yaml" -exec sh -c '
  yq -r ".services | to_entries[] | select(.value.volumes[]? | test(\"^/\")) | .key" "$1"
' _ {} \; | sort -u

```

ディレクトリだけ所有者を変更してファイルはそのままにしたいということですね。Gitで「dubious ownership」エラー対策などで使えます。
```shell
sudo find . -type d -exec chown root:root {} +
```
