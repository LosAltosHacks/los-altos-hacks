# LAH

## Getting Started

If you want to stay on the happy path, do the following:

1. Use a reasonably up-to-date Debian-based linux.
2. Install [NVM](https://github.com/nvm-sh/nvm) to manage node versions.
3. Run `nvm use`
4. Run `npm install` to download versions of formatters and linters etc
5. Install format-on-save plugins for your favorite editors that will use local Prettier and ESLint. Otherwise, run them regularly with `npx [cmd] [args]`.
6. Follow the instructions for the project you work on next.

Before pushing commits, ensure they pass style and lint checks by running `./scripts/stylecheck.sh` from the root directory.
