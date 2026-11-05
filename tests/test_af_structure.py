"""CERBERUS Structure regression tests.
Requested attribution: Nicholas M. Grossi and Caden H. McCullen.
"""
import unittest
from minimal_service.af_workflow import process, render, STEPS

class StructureTests(unittest.TestCase):
    def request(self):
        return {"source": "Review the material.", "corrections": [
            {"id": "C-01", "letter": "C", "start": 11, "end": 19,
             "original": "material", "replacement": "content"}]}

    def test_substitution_has_no_structure_correction(self):
        result = process(self.request())
        self.assertEqual(result["type_1"], "Review the content.")
        self.assertEqual(result["type_2"][3]["entries"], [])
        self.assertEqual(tuple(s["term"] for s in result["type_2"]), STEPS)
        self.assertIn("No structural correction applied", render(result))
        self.assertNotIn("D –", render(result))

    def test_identical_explicit_structure_has_no_d_label(self):
        request = dict(self.request(), structured_text="Review the content.",
                       structure_note="Term order unchanged.")
        self.assertEqual(process(request)["type_2"][3]["entries"], [])

    def test_unchanged_source_has_no_d_label(self):
        result = process({"source": "Content", "corrections": []})
        self.assertEqual(result["type_2"][3]["entries"], [])
        self.assertNotIn("D –", render(result))

    def test_explicit_restructuring_retains_record(self):
        request = dict(self.request(), structured_text="The content requires review.",
                       structure_note="Explicitly supplied sentence restructuring.")
        entry = process(request)["type_2"][3]["entries"][0]
        self.assertEqual(entry["letter"], "D")
        self.assertEqual(entry["before"], "Review the content.")
        self.assertEqual(entry["after"], request["structured_text"])
        self.assertEqual(entry["note"], request["structure_note"])

if __name__ == "__main__":
    unittest.main()
