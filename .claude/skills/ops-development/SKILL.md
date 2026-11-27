---
name: ops-development
description: Guide PR descriptions, commit messages, and staged-diff checks before commits.
---

# Pull request descriptions

Resolve repository paths from the repository root.

- Use `.github/pull_request_template.md` if present. Preserve all headings and their order;
  replace prompts with accurate content. If it is empty, has no placeholders, or is
  absent, add the required PR content without removing existing headings; if absent, use:

  ## What

  ## Why

- **What:** State the main changes clearly and coherently.
- **Why:** Explain the need and why this approach fits.
- Keep descriptions brief, use simple words, and focus on core changes. Add detail only
  when needed or requested.
- Update an existing PR description after commits adding a feature, architectural change,
  bug fix, or major-failure resolution. This applies both when editing the PR directly and
  when preparing updated text for the developer. Skip minor non-functional changes unless
  they alter the PR's scope or reviewer context.

## Commit messages

Keep commit messages concise and accurate to the change's intent and scope; avoid verbose
bodies. Follow `AGENTS.md`'s rule against AI attribution and `Co-authored-by` trailers.

## Large diff pre-commit check

Before `git commit`, inspect only staged changes with `git diff --cached`. Count added
plus deleted lines (not net delta or hunk context) in qualifying changes to application
behavior or logic, meaningful unit-test logic, or migration schema/data behavior. Count
each file containing qualifying changes.

Exclude lockfiles, generated code/artifacts, pure renames or moves, formatting-only
changes, and minor configuration edits. Count configuration changes only when they
substantially affect application behavior.

If unstaged edits exist, assess the staged diff separately; do not include unstaged edits.
If a partial staging makes the intended commit unclear, clarify or stage the intended
changes before assessing.

If more than 10 files or more than 400 qualifying added-plus-deleted lines meet these
criteria, stop before committing. Warn that the PR may be too large and risk rejection
without line-by-line review, then ask for explicit confirmation before proceeding.
