#!/usr/bin/env bash
# Migrate Hugo layouts to the v0.146.0+ directory structure.
# Run from the repository root (the folder that contains .hugo/).
set -euo pipefail

LAYOUTS=".hugo/layouts"

# Verify we are in the right place before touching anything.
if [[ ! -d "$LAYOUTS/_default" ]]; then
  echo "Error: $LAYOUTS/_default not found. Run this from the repository root." >&2
  exit 1
fi

echo "==> Moving templates out of _default/ ..."
for name in baseof home list single; do
  mv -v "$LAYOUTS/_default/$name.html" "$LAYOUTS/$name.html"
done

# terms.html rendered the list of all terms in a taxonomy (e.g. /tags/).
# In v0.146.0+ that page kind is called 'taxonomy', so the file must be
# named taxonomy.html. The 'term' kind (a single tag's page) falls back
# to list.html, which is correct for this site.
mv -v "$LAYOUTS/_default/terms.html" "$LAYOUTS/taxonomy.html"

rmdir "$LAYOUTS/_default"
echo "    Removed _default/"

echo "==> Renaming partials/ → _partials/ ..."
mv -v "$LAYOUTS/partials" "$LAYOUTS/_partials"

# Minor cleanup in baseof.html:
# When "." is already the Page, ".Page.Store.Get" is redundant;
# ".Store.Get" expresses the same thing more directly.
echo "==> Cleaning up .Page.Store.Get in baseof.html ..."
sed -i 's/\.Page\.Store\.Get "/\.Store\.Get "/g' "$LAYOUTS/baseof.html"

echo ""
echo "Done. Summary of changes:"
echo "  _default/{baseof,home,list,single}.html  →  layouts root"
echo "  _default/terms.html                      →  taxonomy.html"
echo "  partials/                                →  _partials/"
echo "  baseof.html: .Page.Store.Get             →  .Store.Get"
echo ""
echo "Files that did not move:"
echo "  layouts/404.html"
echo "  layouts/_markup/render-codeblock-mermaid.html"
echo ""
echo "Rebuild: cd .hugo && hugo"
