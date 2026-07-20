import tempfile
import unittest
from pathlib import Path

from scripts.validate_skill import (
    CHECKOUT_REVISION,
    SERVICE_REQUEST_URL,
    validate_repository,
)


class ValidateSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "agents").mkdir()
        (self.root / "docs").mkdir()
        (self.root / ".github/ISSUE_TEMPLATE").mkdir(parents=True)
        (self.root / ".github/workflows").mkdir(parents=True)
        (self.root / "SKILL.md").write_text(
            "---\n"
            "name: code-work\n"
            "description: Test fixture for repository validation.\n"
            "---\n\n"
            "# Code Work\n",
            encoding="utf-8",
        )
        (self.root / "agents/openai.yaml").write_text(
            "interface:\n"
            '  display_name: "Code Work"\n'
            '  short_description: "Scoped implementation"\n'
            '  default_prompt: "Use $code-work for this task."\n',
            encoding="utf-8",
        )
        for name in ("README.md", "README.ru.md", "SERVICES.md"):
            (self.root / name).write_text(
                f"# Document\n\n[Request services]({SERVICE_REQUEST_URL})\n",
                encoding="utf-8",
            )
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\nSee [license](LICENSE).\n", encoding="utf-8"
        )
        (self.root / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (self.root / ".github/ISSUE_TEMPLATE/config.yml").write_text(
            "blank_issues_enabled: true\n", encoding="utf-8"
        )
        (self.root / ".github/workflows/validate.yml").write_text(
            "name: Validate\n\n"
            "on:\n  pull_request:\n\n"
            "permissions:\n  contents: read\n\n"
            "jobs:\n  validate:\n    steps:\n"
            f"      - uses: actions/checkout@{CHECKOUT_REVISION}\n"
            "        with:\n          persist-credentials: false\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_valid_fixture_passes(self) -> None:
        self.assertEqual(validate_repository(self.root), [])

    def test_missing_required_file_is_reported(self) -> None:
        (self.root / "LICENSE").unlink()

        self.assertIn("missing required file: LICENSE", validate_repository(self.root))

    def test_broken_local_markdown_link_is_reported(self) -> None:
        (self.root / "README.md").write_text(
            f"# Document\n\n[Request services]({SERVICE_REQUEST_URL})\n"
            "[Missing](docs/missing.md)\n",
            encoding="utf-8",
        )

        errors = validate_repository(self.root)

        self.assertIn("README.md: missing local link target: docs/missing.md", errors)

    def test_missing_central_service_link_is_reported(self) -> None:
        (self.root / "SERVICES.md").write_text(
            "# Services\n\nRequest a private discussion.\n", encoding="utf-8"
        )

        self.assertIn(
            "SERVICES.md: missing central service-request link",
            validate_repository(self.root),
        )

    def test_default_prompt_must_name_the_skill(self) -> None:
        (self.root / "agents/openai.yaml").write_text(
            "interface:\n"
            '  display_name: "Code Work"\n'
            '  short_description: "Scoped implementation"\n'
            '  default_prompt: "Use the implementation workflow."\n',
            encoding="utf-8",
        )

        self.assertIn(
            "agents/openai.yaml: default_prompt must mention $code-work",
            validate_repository(self.root),
        )

    def test_malformed_skill_yaml_scalar_is_reported(self) -> None:
        (self.root / "SKILL.md").write_text(
            "---\nname: code-work\ndescription: [unterminated\n---\n\n# Code Work\n",
            encoding="utf-8",
        )

        errors = validate_repository(self.root)

        self.assertTrue(any("malformed plain scalar" in error for error in errors), errors)

    def test_malformed_agent_yaml_scalar_is_reported(self) -> None:
        (self.root / "agents/openai.yaml").write_text(
            "interface:\n"
            '  display_name: "unterminated\n'
            '  short_description: "Scoped implementation"\n'
            '  default_prompt: "Use $code-work for this task."\n',
            encoding="utf-8",
        )

        errors = validate_repository(self.root)

        self.assertTrue(any("invalid double-quoted scalar" in error for error in errors), errors)

    def test_broken_reference_style_link_is_reported(self) -> None:
        (self.root / "README.md").write_text(
            f"# Document\n\n[Request services]({SERVICE_REQUEST_URL})\n"
            "[Missing][missing]\n\n[missing]: docs/not-there.md\n",
            encoding="utf-8",
        )

        errors = validate_repository(self.root)

        self.assertIn(
            "README.md: missing local link target: docs/not-there.md",
            errors,
        )

    def test_checkout_revision_must_be_pinned(self) -> None:
        workflow = self.root / ".github/workflows/validate.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(CHECKOUT_REVISION, "main"),
            encoding="utf-8",
        )

        errors = validate_repository(self.root)

        self.assertTrue(any("single reviewed revision" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
