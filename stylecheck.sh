set -e
npx prettier --check '**/*.html' '**/*.css' '**/*.js'
npx eslint 'frontpage/**/*'
