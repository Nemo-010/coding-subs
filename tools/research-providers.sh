#!/bin/sh
# research-providers.sh - mine the provider list out of one or more AI-gateway repos
# and merge the results into a single union table.
#
# usage:
#   tools/research-providers.sh OUTDIR NAME=PATH_OR_GIT_URL [NAME=PATH_OR_GIT_URL ...]
#
# example:
#   tools/research-providers.sh 2026-09-20/data \
#       sub2api=/workspace/sub2api \
#       cliproxyapi=https://github.com/router-for-me/CLIProxyAPI
#
# Outputs, per repo:  providers-<name>.csv, providers-<name>.jsonl
# and once for all:   providers-union.csv
#
# The extractor is heuristic and structure-agnostic (see mine-providers.py).
# It is deliberately multi-signal: directories, symbolic constants, switch
# labels, JSON registries, YAML config, markdown tables and a provider
# vocabulary. A repo whose layout changes is still covered by at least one
# signal; new providers are caught by the vocabulary fallback.
set -eu

if [ "$#" -lt 2 ]; then
    sed -n '2,12p' "$0" >&2
    exit 2
fi

out=$1
shift
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$out"

csvs=
for spec in "$@"; do
    name=${spec%%=*}
    target=${spec#*=}
    if [ "$name" = "$target" ] || [ -z "$name" ] || [ -z "$target" ]; then
        echo "research-providers: bad spec '$spec' (want NAME=PATH_OR_URL)" >&2
        exit 2
    fi
    case "$target" in
        *://*) python3 "$here/mine-providers.py" --url "$target" --name "$name" --out "$out" ;;
        *)     python3 "$here/mine-providers.py" --repo "$target" --name "$name" --out "$out" ;;
    esac
    csvs="$csvs $out/providers-$name.csv"
done

# shellcheck disable=SC2086
python3 "$here/reconcile-providers.py" --out "$out" $csvs

echo
echo "provider lists written to $out"
echo "  next: rank them — see 2026-09-20/PROVIDER-SUPPORT.md 'Reproduce'"
