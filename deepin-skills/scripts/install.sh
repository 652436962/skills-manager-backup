#!/bin/sh
set -eu

usage() {
    cat <<'EOF'
Usage: ./scripts/install.sh [--force]

Install every valid skill in skills/ into ${SKILL_HOME:-$HOME/.agents}/skills.

When run from a local checkout, install from that checkout. When run with
curl or wget, download the configured GitHub repository archive first.

Options:
  --force  Replace existing skills with the same name.
  -h, --help
           Show this help message.

Environment:
  SKILL_HOME  Skill root directory.
EOF
}

force=0
while [ "$#" -gt 0 ]; do
    case "$1" in
        --force)
            force=1
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            usage >&2
            exit 2
            ;;
    esac
    shift
done

source_dir=
case "$0" in
    */install.sh|install.sh)
        script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
        local_source_dir=$(dirname "$script_dir")/skills
        if [ -d "$local_source_dir" ]; then
            source_dir=$local_source_dir
        fi
        ;;
esac

if [ -z "$source_dir" ]; then
    archive_url="https://github.com/linuxdeepin/deepin-skills/archive/refs/heads/master.tar.gz"
    temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/deepin-skills.XXXXXX")
    archive_path="$temp_dir/deepin-skills.tar.gz"
    trap 'rm -rf "$temp_dir"' 0 HUP INT TERM

    if command -v curl >/dev/null 2>&1; then
        curl --fail --location --silent --show-error "$archive_url" -o "$archive_path"
    elif command -v wget >/dev/null 2>&1; then
        wget -q -O "$archive_path" "$archive_url"
    else
        echo "curl or wget is required to download Deepin skills." >&2
        exit 1
    fi

    tar -xzf "$archive_path" -C "$temp_dir"
    for repository_dir in "$temp_dir"/*; do
        if [ -d "$repository_dir/skills" ]; then
            source_dir=$repository_dir/skills
            break
        fi
    done
fi

[ -n "$source_dir" ] && [ -d "$source_dir" ] || {
    echo "Skill source directory not found." >&2
    exit 1
}

target_dir="${SKILL_HOME:-$HOME/.agents}/skills"
skill_count=0

# Check the complete source set before changing the target directory.
for source_path in "$source_dir"/*; do
    [ -d "$source_path" ] && [ -f "$source_path/SKILL.md" ] || continue
    skill=$(basename "$source_path")
    target_path="$target_dir/$skill"
    skill_count=$((skill_count + 1))

    if { [ -e "$target_path" ] || [ -L "$target_path" ]; } && [ "$force" -ne 1 ]; then
        echo "Skill already exists: $target_path (rerun with --force to replace it)" >&2
        exit 1
    fi
done

[ "$skill_count" -gt 0 ] || {
    echo "No valid skills found in: $source_dir" >&2
    exit 1
}

mkdir -p "$target_dir"

for source_path in "$source_dir"/*; do
    [ -d "$source_path" ] && [ -f "$source_path/SKILL.md" ] || continue
    skill=$(basename "$source_path")
    target_path="$target_dir/$skill"

    if [ -e "$target_path" ] || [ -L "$target_path" ]; then
        rm -rf "$target_path"
    fi

    cp -R "$source_path" "$target_path"
    echo "Installed $skill to $target_path"
done
