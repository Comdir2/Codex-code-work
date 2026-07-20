# Contributing to Code Work

Thank you for helping improve the skill. Contributions should preserve its central contract: authorized scope, repository awareness, root-cause reasoning, small coherent changes, proportionate verification, and honest evidence.

## Before proposing a change

1. Search [existing issues](https://github.com/Comdir2/Codex-code-work/issues) for related discussion.
2. Describe the concrete failure mode or workflow gap rather than only proposing more instructions.
3. Explain which user request should trigger the behavior and which requests should not.
4. Keep unrelated policy, formatting, and wording changes in separate proposals.

For a large change to skill behavior, open an issue before investing in a full patch. Maintainer discussion is not a guarantee that a proposal will be accepted.

## Development principles

- Preserve explicit user authority and strict task scope.
- Do not introduce automatic permission for commits, pushes, deployment, destructive operations, external messages, or adjacent fixes.
- Prefer concise operational rules over duplicated prose.
- Keep the sequential workflow complete; parallelism must remain optional.
- Require exclusive write ownership and fresh integrated verification for parallel workflows.
- Avoid unverifiable claims about performance, correctness, model behavior, or compatibility.
- Keep examples realistic and clearly separate expected workflow from guaranteed outcome.
- Do not add credentials, private URLs, customer data, or generated local state.

## Preparing a pull request

Create a focused branch or fork and include:

- the problem and intended user-visible effect;
- the exact files changed;
- an example prompt before and after the change when behavior changes;
- compatibility or scope implications;
- checks performed and their results;
- any remaining uncertainty.

## Verification checklist

Before submitting:

- confirm `SKILL.md` retains valid YAML frontmatter with `name` and `description`;
- confirm `agents/openai.yaml` remains valid YAML if it was changed;
- inspect all Markdown links and relative paths;
- run `python3 scripts/validate_skill.py`;
- run `python3 -m unittest discover -s tests`;
- run `git diff --check`;
- review the complete diff for unrelated edits and sensitive information;
- update `CHANGELOG.md` when the change is user-visible.

The repository validator is a self-contained structural check; it is not a substitute for an official Codex skill validator. If an official validator is available in your environment, run it too and report the exact command and result. If it is unavailable, state that limitation.

## License of contributions

By submitting a contribution, you agree that it may be distributed under the repository's [MIT License](LICENSE). Do not submit material you do not have the right to contribute.

## Conduct

Keep technical discussion respectful, specific, and focused on observable behavior and evidence. Harassment, personal attacks, and disclosure of another person's private information are not acceptable.
