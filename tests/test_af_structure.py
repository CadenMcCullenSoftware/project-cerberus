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

    def test_restructuring_does_not_imply_d(self):
        request = dict(self.request(), structured_text="The content requires review.",
                       structure_note="Explicit sentence restructuring.")
        result = process(request)
        step = result["type_2"][3]
        self.assertEqual(step["entries"], [])
        self.assertEqual(step["restructuring"]["before"], "Review the content.")
        self.assertEqual(step["restructuring"]["after"], request["structured_text"])
        self.assertNotIn("D –", render(result))
        self.assertIn(request["structured_text"], render(result))

    def test_supplied_definition_is_recorded_not_verified(self):
        request = {"source": "A triangle has four sides.", "corrections": [],
                   "structured_text": "A triangle has three sides.",
                   "structure_note": "Correct the supplied definition.",
                   "structure_definition": "A triangle is a polygon with three sides."}
        result = process(request)
        entry = result["type_2"][3]["entries"][0]
        self.assertEqual(entry["letter"], "D")
        self.assertEqual(entry["definition"], request["structure_definition"])
        self.assertEqual(entry["definition_status"], "supplied_not_verified")
        self.assertIn("D –", render(result))

    def test_invalid_structure_definition_is_rejected(self):
        for value in ("", "  ", None, [], {}):
            request = dict(self.request(), structured_text="The content requires review.",
                           structure_note="Restructure.", structure_definition=value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                process(request)

    def test_definition_requires_changed_structured_text(self):
        for fields in ({}, {"structured_text": "Review the content.", "structure_note": "Unchanged."}):
            request = dict(self.request(), structure_definition="Supplied definition.", **fields)
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                process(request)

    def test_wrong_letter_types_are_controlled_errors(self):
        for value in ([], {}, None, 1):
            request = self.request()
            request["corrections"][0]["letter"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                process(request)

if __name__ == "__main__":
    unittest.main()
