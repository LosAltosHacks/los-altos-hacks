#!/usr/bin/env sh
sed -e '/<head>/a\' -e '<meta name="robots" content="noindex">' -i "$1"
