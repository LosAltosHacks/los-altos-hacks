#!/usr/bin/env bash
set -eu
trap 'printf "\e[1m\e[31mStyle checks failed.\e[0m\n" >&2' ERR

grep_exclude_pattern_file="/tmp/lah_exclude_file"
cat <<EOF > "$grep_exclude_pattern_file"
*.min.js
*.svg
EOF

grep --binary-files=without-match --files-with-matches '.' \
--dereference-recursive --exclude-from "$grep_exclude_pattern_file" ./frontpage | xargs -L 1 -I {} \
bash -c '[ ! $(tail -c 1 {}) ] ||  { echo "{}: Missing newline at EOF."; false; }'


npx prettier --check '**/*.html' '**/*.css' '**/*.js'


echo "Checking for trailing whitespace..."
grep --files-with-matches --binary-files=without-match '[[:blank:]]$' \
--dereference-recursive frontpage/ && false

echo "Running ESLint"
npx eslint 'frontpage/**/*.js'

printf "\e[1m\e[32mStyle checks passed.\e[0m\n" >&2
