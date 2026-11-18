# Review every pull request automatically

`.github/workflows/review.yml` is a reusable GitHub Actions workflow. On each pull request it runs [Claude Code Action](https://github.com/anthropics/claude-code-action) with this skill and posts the report as one PR comment. It never approves, requests changes or pushes.

## Set up a repository

1. Install the [Claude GitHub app](https://github.com/apps/claude) on the repository.
2. Add your Anthropic API key as a repository secret named `ANTHROPIC_API_KEY`:

   ```sh
   gh secret set ANTHROPIC_API_KEY -R <owner>/<repo>
   ```

3. Add `.github/workflows/looks-good-to-ai.yml`:

   ```yaml
   name: Review PRs with Looks Good to AI

   on:
     pull_request:
       types: [opened, synchronize, ready_for_review, reopened]

   jobs:
     review:
       permissions:
         contents: read
         pull-requests: write
         id-token: write
       uses: laulauraluo/looks-good-to-ai/.github/workflows/review.yml@main
       secrets: inherit
   ```

## Limits

- **Pull requests from forks are skipped.** GitHub does not pass secrets to them, and running a model on untrusted code with write access is unsafe. Review those by hand or from your own agent.
- Drafts are skipped until they are marked ready for review.
- **No key, no review.** If `ANTHROPIC_API_KEY` isn't set, the review job is skipped instead of failing, so the check stays green.
- Each run uses your API key, so it costs tokens on every push to a pull request.
