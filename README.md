# LAH

## Getting Started

If you want to stay on the happy path, do the following:

1. Use a reasonably up-to-date Debian-based linux.
2. Install [NVM](https://github.com/nvm-sh/nvm) to manage node versions.
3. Run `nvm use`
4. Run `npm install` to download versions of formatters and linters etc
5. Install format-on-save plugins for your favorite editors that will use local Prettier and ESLint. Otherwise, run them regularly with `npx [cmd] [args]`.
6. Follow the instructions for the project you work on next.

Before pushing commits, ensure they pass style and lint checks by running `./scripts/stylecheck.sh` from the root directory. Using `npx run prettier`, you will be able to run a prettier script that will fix all prettier errors.

## Development and Deployment Process

Developers work in feature branches and open pull requests to `master`.
After passing tests and review, they are merged and automatically deployed to the staging environment.
Manually testing and a more complete suite of tests can/will then occur.
Information on how to access the staging environment is available to team members.
`master` should ideally only contain production-quality code.

To get code into production, create a temporary release branch, something like `release-my-feature` or `release-version`.
This branch's `HEAD` should be in the `master`'s history, ie it's been merged and tested.
Then, push the branch and open a PR from that branch into `production`. After a final checkoff from an approved team-member, the PR is merged and automatically deployed.
The temporary release branch gives merge commits into `production` a descriptive name, and allows development to continue on master without being included in PR into `production`.

## Infrastructure

Currently infrastructure is managed manually on the AWS console, but deployments are automated from the `production` branch.
More info is in the `docs` folder.
Eventually, we might do some Infrastructure-as-Code stuff.
