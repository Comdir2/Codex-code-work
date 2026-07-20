# Code Work quickstart

This guide installs the skill and walks through one bounded implementation task.

## Prerequisites

- A Codex environment with skill support.
- Python 3 for the bundled installer.
- Network access to `github.com` during installation.
- A repository you are authorized to modify.

## 1. Install from GitHub

For the default Codex home directory, run:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Comdir2/Codex-code-work \
  --path . \
  --name code-work
```

The installer does not overwrite an existing skill directory. If `code-work` is already installed, review that installation and decide deliberately whether it should be retained, backed up, or replaced.

Restart Codex after a successful installation.

## 2. Confirm the installed files

For the default Codex home directory:

```bash
test -f ~/.codex/skills/code-work/SKILL.md
test -f ~/.codex/skills/code-work/agents/openai.yaml
```

A zero exit status confirms that the expected files exist. It does not by itself prove that a particular Codex session has refreshed its skill catalog; restart the session if the skill is not listed.

## 3. Start with an explicit change contract

A useful first prompt names the behavior, boundaries, compatibility constraints, and evidence:

```text
Use $code-work to fix the CLI crash when --format json is combined with an
empty result set. Preserve the existing JSON schema and exit codes. Add a
focused regression test, run the affected CLI tests and existing static
checks, and do not change unrelated output formatting or publish anything.
```

If the request leaves an important public-interface or safety choice open, expect Codex to stop and ask before choosing for you. Small non-material assumptions may be stated and used to continue.

## 4. Check the workflow, not just the final patch

A Code Work task should normally produce evidence for these stages:

1. repository guidance and current worktree state were inspected;
2. acceptance criteria and protected invariants were identified;
3. the failure was reproduced, or the feature seam was traced;
4. the implementation was limited to a coherent slice;
5. focused and proportionate broader checks were run with fresh results;
6. the final handoff distinguished confirmed, partial, unverified, and failed evidence where relevant.

Parallel workers may be used only for independent work with exclusive write ownership and an integration check. A sequential execution is equally valid.

## 5. Request an independent verification pass

For material changes, install [Code Verification](https://github.com/Comdir2/Codex-code-verification) and begin a separate task:

```text
Use $code-verification to independently review the implementation against the
original acceptance criteria. Keep the review read-only, run the relevant
checks from a clean understanding of the diff, and report findings by severity.
```

The verification task should not silently fix findings unless the user separately authorizes production changes.

## Next steps

- Browse [realistic prompt examples](../examples/README.md).
- Review the [engineering decision guides](../references/engineering-decisions.md).
- Read the [support policy](../SUPPORT.md) before opening an issue.
- For optional repository onboarding or a separately scoped engagement, read [Services](../SERVICES.md) and use the [central service request form](https://github.com/Comdir2/Codex-engineering-guardrails/issues/new?template=service-request.yml). The form is public; never include secrets, private code, customer data, or private URLs.
