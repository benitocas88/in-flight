---
name: ops-development
description: Write concise pull request descriptions using this repository's What and Why template.
---

# Pull request descriptions

When writing a PR description, use the repository's `.github/pull_request_template.md`.
Resolve this path from the repository root, not from this skill's folder.

- **What:** Describe the main changes clearly and coherently. Focus on the core work.
- **Why:** Explain the need for the change and why this approach fits.
- Use simple words and keep both sections brief. Include more detail only when the change
  needs it or the developer asks for it, such as diagrams or a deeper explanation.
- Keep the template's headings and order. Replace its prompts with accurate content.
- Update the PR description when a new commit adds a feature, architectural change, bug
  fix, or resolves a major failure. Skip minor non-functional changes such as typo fixes,
  formatting, small refactors, or comment updates unless they change the PR's scope or
  reviewer context.
- Never include AI attribution in a PR description.

## Commit messages

- Keep commit messages concise while accurately describing the overall intent and scope.
- Avoid overly verbose commit bodies.
- Never include `Co-authored-by` trailers or AI attribution.

## Large diff pre-commit check

Before running `git commit`, review the staged diff and assess the scale of substantive
code changes. Do not treat many trivial or empty file changes (such as renames, moves, or
small config edits) as a large diff by themselves.

Warn and stop before committing if the staged diff contains substantial logic changes in
more than 10 files or more than 400 changed lines. Explain that the PR may be too large
and risks reviewer rejection without a line-by-line review. Ask the developer for explicit
confirmation before proceeding with the commit.
