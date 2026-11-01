import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import guidelines_mcp as gm


class FilesystemContainmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.parent = Path(self.temp.name)
        self.root = self.parent / "root"
        self.guidelines = self.root / "guidelines"
        self.guidelines.mkdir(parents=True)
        (self.root / "uiux_vibecoding_protocol_pack_v1").mkdir()
        self.root_patch = patch.object(gm, "ROOT", self.root.resolve())
        self.root_patch.start()

    def tearDown(self):
        self.root_patch.stop()
        self.temp.cleanup()

    def make_symlink(self, link: Path, target: Path, *, directory: bool = False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unsupported in this environment: {exc}")

    def test_ordinary_file_is_discoverable(self):
        path = self.guidelines / "ordinary.md"
        path.write_text("ordinary", encoding="utf-8")
        self.assertIn(path.resolve(), gm._iter_guideline_files())
        self.assertEqual(gm._resolve_file("guidelines/ordinary.md"), path.resolve())

    def test_outside_file_symlink_is_not_enumerated_or_searchable(self):
        outside = self.parent / "outside.md"
        outside.write_text("OUTSIDE_SECRET", encoding="utf-8")
        link = self.guidelines / "external.md"
        self.make_symlink(link, outside)

        files = gm._iter_guideline_files()
        self.assertFalse(any(path.resolve() == outside.resolve() for path in files))
        result = gm.search_guidelines("OUTSIDE_SECRET", context_lines=0)
        self.assertEqual(result["total_matches"], 0)
        with self.assertRaises(ValueError):
            gm._file_metadata(link)

    def test_in_root_file_symlink_uses_canonical_policy(self):
        target = self.guidelines / "target.md"
        target.write_text("inside", encoding="utf-8")
        link = self.guidelines / "alias.md"
        self.make_symlink(link, target)

        self.assertEqual(gm._resolve_file("guidelines/alias.md"), target.resolve())
        files = gm._iter_guideline_files()
        self.assertIn(target.resolve(), files)
        self.assertEqual(sum(path == target.resolve() for path in files), 1)

    def test_outside_directory_symlink_is_rejected_for_selected_folder(self):
        outside_dir = self.parent / "outside-dir"
        outside_dir.mkdir()
        (outside_dir / "secret.md").write_text("secret", encoding="utf-8")
        link = self.guidelines / "external-dir"
        self.make_symlink(link, outside_dir, directory=True)

        with self.assertRaises(ValueError):
            gm._resolve_directory("guidelines/external-dir")
        files = gm._iter_guideline_files()
        secret = (outside_dir / "secret.md").resolve()
        self.assertFalse(any(path.resolve() == secret for path in files))
        result = gm.search_guidelines("secret", context_lines=0)
        self.assertEqual(result["total_matches"], 0)

    def test_in_root_directory_symlink_resolves_and_enumerates_safely(self):
        real = self.guidelines / "real-dir"
        real.mkdir()
        target = real / "inside.md"
        target.write_text("inside-dir", encoding="utf-8")
        link = self.guidelines / "alias-dir"
        self.make_symlink(link, real, directory=True)

        base = gm._resolve_directory("guidelines/alias-dir")
        self.assertEqual(base, real.resolve())
        self.assertIn(target.resolve(), gm._iter_guideline_files(base))


class ImprovementGuidelineRoutingTests(unittest.TestCase):
    def test_specialist_standard_routed_only_for_improvement_tasks(self):
        standard = "guidelines/REFACTORING_OPTIMIZATION_STANDARD.md"
        for task in ("refactoring", "optimization"):
            self.assertIn(standard, gm.TASK_FILES[task])
        self.assertNotIn(standard, gm.TASK_FILES["coding"])
        self.assertIn(standard, gm.EXPECTED_FILES)

    def test_real_repository_task_returns_authoritative_file(self):
        source = Path(gm.__file__).resolve().parent
        reference = source / "guidelines/REFACTORING_OPTIMIZATION_STANDARD.md"
        self.assertTrue(reference.is_file())
        original_text = reference.read_text(encoding="utf-8")
        self.assertGreater(len(original_text), 10000)
        for task in ("refactoring", "optimization"):
            result = gm.get_guidelines_for_task(task)
            self.assertFalse(result["missing"])
            self.assertFalse(result["truncated"])
            doc = next(
                item for item in result["documents"]
                if item["path"] == "guidelines/REFACTORING_OPTIMIZATION_STANDARD.md"
            )
            self.assertFalse(doc["truncated"])
            self.assertEqual(doc["content"], original_text)

    def test_improvement_task_reads_complete_standard(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            for relative in gm.TASK_FILES["refactoring"]:
                file = root / relative
                file.parent.mkdir(parents=True, exist_ok=True)
                contents = (
                    "FULL_SPECIALIST_STANDARD"
                    if relative.endswith("REFACTORING_OPTIMIZATION_STANDARD.md")
                    else f"policy:{relative}"
                )
                file.write_text(contents, encoding="utf-8")
            with patch.object(gm, "ROOT", root.resolve()):
                for task in ("refactoring", "optimization"):
                    result = gm.get_guidelines_for_task(task)
                    self.assertFalse(result["missing"])
                    self.assertFalse(result["truncated"])
                    docs = [
                        document for document in result["documents"]
                        if document["path"] == "guidelines/REFACTORING_OPTIMIZATION_STANDARD.md"
                    ]
                    self.assertEqual(len(docs), 1)
                    self.assertEqual(docs[0]["content"], "FULL_SPECIALIST_STANDARD")
                    self.assertFalse(docs[0]["truncated"])


if __name__ == "__main__":
    unittest.main()
