# Code Work

A Codex skill for scoped, test-backed software implementation.

Code Work helps Codex implement features, fix defects, refactor code, and perform migrations while preserving the user's approved scope. It emphasizes repository-aware planning, root-cause analysis, small coherent changes, and fresh verification evidence.

[Русская версия](README.ru.md) · [Quickstart](docs/quickstart.md) · [Examples](examples/README.md) · [Support](SUPPORT.md) · [Services](SERVICES.md)

![Codex Engineering Guardrails: build with discipline, verify with evidence](assets/social-preview.jpg)

## What this skill is for

Use Code Work when a task authorizes changes to production code or other implementation files. The skill directs Codex to:

- treat the explicit user request as the controlling contract;
- inspect repository instructions and current changes before editing;
- find the responsible mechanism before fixing a defect;
- implement the smallest coherent, reviewable slice;
- select checks that exercise the affected behavior;
- report fresh evidence, limitations, and deliberately unchanged findings.

It does not grant permission to deploy, publish, push, commit, change live systems, delete data, or expand the task beyond the user's authorization.

## Adaptive parallelism

Code Work can use parallel execution when the model and environment provide suitable resources, but parallelism is optional. The skill first separates dependent and independent work, then applies these guardrails:

- start with a bounded budget of two to four workers;
- parallelize read-only exploration, independent components, or isolated checks;
- assign one owner to every write surface;
- serialize shared contracts, schemas, lockfiles, services, ports, and other common state;
- fall back to the same workflow sequentially when isolation or resources are insufficient;
- verify the integrated result directly instead of relying only on worker summaries.

These rules aim to preserve correctness and scope. This repository does not claim a universal speedup or quality improvement from parallel execution.

## Installation from GitHub

Use the `skill-installer` bundled with Codex. For the default Codex home directory:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Comdir2/Codex-code-work \
  --path . \
  --name code-work
```

If your Codex home is not `~/.codex`, use the corresponding path to the bundled installer. Restart Codex after installation so the skill catalog is refreshed.

See the [quickstart](docs/quickstart.md) for a first task and installation checks.

## Usage

Invoke the skill explicitly when you want the implementation workflow to control the task:

```text
Use $code-work to fix the duplicate invoice creation bug. Keep the public API
unchanged, add a focused regression test, run the affected test suite, and do
not deploy or modify unrelated billing code.
```

When installed, Codex may also select the skill automatically for a matching coding request. Explicit invocation is useful when scope, evidence, or execution constraints are especially important.

The expected workflow is:

1. establish acceptance criteria, scope, invariants, risks, and required evidence;
2. inspect repository guidance, status, code paths, and test configuration;
3. reproduce a defect or identify the public seam for a feature;
4. make a small coherent change and run focused checks;
5. inspect the diff and run proportionate broader verification;
6. hand off changed behavior, evidence, assumptions, and unresolved risks.

More realistic prompts and workflow expectations are available in [examples](examples/README.md).

## Pairing with Code Verification

Code Work is the implementation skill. [Code Verification](https://github.com/Comdir2/Codex-code-verification) is its read-only counterpart for independent review, testing, diagnosis, coverage analysis, and release-readiness judgments.

For a higher-assurance workflow, use Code Work to implement the authorized change, then start a separate verification task with `code-verification`. Separation helps the verifier assess the requirements and evidence without silently extending the implementation scope.

## Professional help

If you want repository onboarding, custom implementation guardrails, or a separately scoped delivery engagement, use the [central service request form](https://github.com/Comdir2/Codex-engineering-guardrails/issues/new?template=service-request.yml). The form creates a public GitHub issue, so provide only a sanitized summary. Do not post credentials, private repository contents, proprietary source code, customer data, private URLs, or commercial secrets.

Opening the form is only a request to discuss scope. It is not an order, quote, contract, or authorization to begin work. See [Services](SERVICES.md) for the available engagement types and non-binding starting ranges.

## Project documentation

- [Quickstart](docs/quickstart.md)
- [Prompt examples](examples/README.md)
- [Engineering decision guides](references/engineering-decisions.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Optional professional services](SERVICES.md)

## Benchmarks

No performance or correctness improvement is claimed in this README. A reproducible scenario corpus and methodology are published at [Codex Engineering Guardrails / benchmark](https://github.com/Comdir2/Codex-engineering-guardrails/tree/main/benchmark). The current validator proves fixture integrity and known baselines; it does not invoke or score a model. Any future model results must be interpreted with their scenarios, environments, run records, and limitations.

## License

Code Work is available under the [MIT License](LICENSE). The open-source skill remains free to use, modify, distribute, and include in commercial work under that license. Optional support and services do not change the license of the public repository.

## Project status and independence

The initial documented release is `v1.0.0`. See the [changelog](CHANGELOG.md) for its contents.

This is an independent community project. It is not an official OpenAI or GitHub product and is not endorsed by either company.
