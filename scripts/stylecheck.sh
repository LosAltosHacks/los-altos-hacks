#!/usr/bin/env bash
set -eu
trap 'printf "\e[1m\e[31mStyle checks failed.\e[0m\n" >&2' ERR

npm install # ensure we use the right versions of stylechecking packages

npx prettier --check '**/*.html' '**/*.css' '**/*.js'

echo "Checking for trailing whitespace..."
grep --files-with-matches --binary-files=without-match '[[:blank:]]$' --dereference-recursive frontpage/ && false

echo "Running ESLint"
npx eslint 'frontpage/**/*.js'

printf "\e[1m\e[32mStyle checks passed.\e[0m\n" >&2
