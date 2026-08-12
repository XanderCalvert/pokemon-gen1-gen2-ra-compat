#!/usr/bin/env bash
# Sync explicitly allowlisted files from the private PokemonYellow research
# repo into this public display repo. Every published file is listed in
# scripts/snapshot-manifest.txt -- this script never discovers files on its
# own and never copies a directory wholesale.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISPLAY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$SCRIPT_DIR/snapshot-manifest.txt"
SOURCE_ROOT="$(cd "$DISPLAY_ROOT/.." && pwd)/PokemonYellow"
DRY_RUN=0
AUDIT=0

usage() {
    cat <<EOF
Usage: $(basename "$0") [--source PATH] [--dry-run] [--audit]

  --source PATH   Path to the private PokemonYellow repo (default: the
                   sibling directory, ../PokemonYellow relative to this
                   display repo).
  --dry-run       Print "source -> destination" for every manifest entry
                   without copying anything.
  --audit         List files under managed destination directories that
                   are NOT in the manifest (nothing is copied or deleted).
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        --source) SOURCE_ROOT="$2"; shift 2 ;;
        --dry-run) DRY_RUN=1; shift ;;
        --audit) AUDIT=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
    esac
done

# --- safety: verify we know where we are before touching anything ---

if [ ! -f "$DISPLAY_ROOT/README.md" ] || [ ! -d "$DISPLAY_ROOT/games/yellow" ] || [ ! -d "$DISPLAY_ROOT/shared/scripts" ]; then
    echo "Refusing to run: '$DISPLAY_ROOT' doesn't look like the display repo root (missing README.md / games/yellow / shared/scripts)." >&2
    exit 1
fi

if [ ! -d "$SOURCE_ROOT" ]; then
    echo "Refusing to run: source repo not found at '$SOURCE_ROOT' (pass --source to override)." >&2
    exit 1
fi

if [ ! -d "$SOURCE_ROOT/scripts" ] || [ ! -d "$SOURCE_ROOT/games/yellow" ] || [ ! -d "$SOURCE_ROOT/vendor/pokeyellow" ]; then
    echo "Refusing to run: '$SOURCE_ROOT' doesn't look like the PokemonYellow source repo (missing scripts/ / games/yellow/ / vendor/pokeyellow/)." >&2
    exit 1
fi

if [ ! -f "$MANIFEST" ]; then
    echo "Refusing to run: manifest not found at '$MANIFEST'." >&2
    exit 1
fi

# Belt-and-suspenders ban, even though the manifest is an explicit
# allowlist: never let a path referencing these through, no matter how it
# got into the manifest.
BANNED_PATTERN='(^|/)(roms|saves?|states?|bios)(/|$)|\.(gb|gbc|sav|state|sgm|srm|bin)$|(^|/)(credential|secret|\.env)'

is_banned() {
    printf '%s' "$1" | grep -Eiq "$BANNED_PATTERN"
}

declare -A COUNTS=([italian]=0 [french]=0 [german]=0 [shared]=0 [other]=0)
declare -a MANAGED_DEST_DIRS=()
declare -A KNOWN_DEST=()

category_for() {
    case "$1" in
        games/yellow/italian/*) echo italian ;;
        games/yellow/french/*) echo french ;;
        games/yellow/german/*) echo german ;;
        shared/*) echo shared ;;
        *) echo other ;;
    esac
}

while IFS='|' read -r src_rel dst_rel; do
    [ -z "${src_rel:-}" ] && continue
    case "$src_rel" in \#*) continue ;; esac
    [ -z "${dst_rel:-}" ] && { echo "Malformed manifest line (missing '|'): $src_rel" >&2; exit 1; }

    if is_banned "$src_rel" || is_banned "$dst_rel"; then
        echo "Refusing manifest entry (matches banned pattern): $src_rel -> $dst_rel" >&2
        exit 1
    fi

    src="$SOURCE_ROOT/$src_rel"
    dst="$DISPLAY_ROOT/$dst_rel"
    dst_dir="$(dirname "$dst_rel")"
    MANAGED_DEST_DIRS+=("$dst_dir")
    KNOWN_DEST["$dst_rel"]=1

    if [ "$AUDIT" -eq 1 ]; then
        continue
    fi

    echo "$src_rel -> $dst_rel"
    if [ "$DRY_RUN" -eq 1 ]; then
        continue
    fi

    if [ ! -f "$src" ]; then
        echo "Missing required source file: $src" >&2
        exit 1
    fi

    mkdir -p "$DISPLAY_ROOT/$dst_dir"
    cp "$src" "$dst"

    if ! cmp -s "$src" "$dst"; then
        echo "Verification failed after copy: $src != $dst" >&2
        exit 1
    fi

    cat=$(category_for "$dst_rel")
    COUNTS[$cat]=$((COUNTS[$cat] + 1))
done < "$MANIFEST"

if [ "$AUDIT" -eq 1 ]; then
    echo "Auditing managed destination directories for files not in the manifest..."
    found_unexpected=0
    # de-duplicate
    mapfile -t uniq_dirs < <(printf '%s\n' "${MANAGED_DEST_DIRS[@]}" | sort -u)
    for dir_rel in "${uniq_dirs[@]}"; do
        dir="$DISPLAY_ROOT/$dir_rel"
        [ -d "$dir" ] || continue
        while IFS= read -r -d '' f; do
            f_rel="${f#"$DISPLAY_ROOT/"}"
            f_rel="${f_rel//\\//}"
            if [ -z "${KNOWN_DEST[$f_rel]:-}" ]; then
                echo "  unexpected: $f_rel"
                found_unexpected=1
            fi
        done < <(find "$dir" -maxdepth 1 -type f -print0)
    done
    if [ "$found_unexpected" -eq 0 ]; then
        echo "No unexpected files found."
    fi
    exit 0
fi

if [ "$DRY_RUN" -eq 1 ]; then
    echo "Dry run complete. Nothing was copied."
    exit 0
fi

total=$((COUNTS[italian] + COUNTS[french] + COUNTS[german] + COUNTS[shared] + COUNTS[other]))
echo
echo "Snapshot updated successfully"
echo
echo "Italian: ${COUNTS[italian]}"
echo "French: ${COUNTS[french]}"
echo "German: ${COUNTS[german]}"
echo "Shared: ${COUNTS[shared]}"
echo "Total: $total"
