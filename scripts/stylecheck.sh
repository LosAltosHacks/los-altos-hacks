#!/usr/bin/env sh
set -eu
npx prettier --check '**/*.html' '**/*.css' '**/*.js'
echo "Checking for trailing whitespace..."
grep --files-with-matches --binary-files=without-match '[[:blank:]]$' --dereference-recursive frontpage/ && exit 1
npx eslint 'frontpage/**/*.js'
