"""CERBERUS A-F tests. Requested attribution: Nicholas M. Grossi and Caden H. McCullen."""
import unittest
from minimal_service.af_workflow import process, render, STEPS

class WorkflowTests(unittest.TestCase):
    def example(self):
        source = "The scope of the objective would be capturing the material, ensuring traceability is provided with evidence."
        changes = [
            ("scope", "Task presented", "A", {"selected_term": "review"}),
            ("objective", "provided requirements", "B", {"category": "requirements"}),
            ("capturing", "details", "A", {}),
            ("material", "content", "C", {}),
            ("traceability is provided with evidence", "historical information", "E", {}),
        ]
        edits = []
        for i, (old, new, letter, extra) in enumerate(changes):
            start = source.index(old)
            edits.append(dict(id=str(i), letter=letter, start=start, end=start+len(old), original=old, replacement=new, **extra))
        return dict(source=source, corrections=edits,
            structured_text="Task presented to support the provided requirements from the details of the content must include historical information.",
            structure_note="Must include establishes the specified correlation; order: Task → requirements → details of content → historical information.")

    def test_exact_example(self):
        request = self.example()
        result = process(request)
        self.assertEqual(result["type_1"], request["structured_text"])
        self.assertEqual(tuple(s["term"] for s in result["type_2"]), STEPS)
        self.assertEqual(result["type_2"][0]["entries"][0]["selected"], "review")
        self.assertEqual(result["type_2"][1]["entries"][0]["replacement"], "Task presented")
        self.assertIn("[Type 2", render(result))

    def test_repeated_category_retained(self):
        result = process(self.example())
        self.assertEqual([e["letter"] for e in result["type_2"][0]["entries"]].count("A"), 2)

    def test_no_edit(self):
        self.assertEqual(process(dict(source="Content", corrections=[]))["type_1"], "Content")

    def test_invalid_requests(self):
        for mutation in ("span", "overlap", "letter", "category", "id", "structure", "boolean", "definition"):
            request = self.example()
            edit = request["corrections"][0]
            if mutation == "span": edit["original"] = "other"
            if mutation == "overlap": request["corrections"][1] = dict(edit, id="different")
            if mutation == "letter": edit["letter"] = "G"
            if mutation == "category": del request["corrections"][1]["category"]
            if mutation == "id": request["corrections"][1]["id"] = edit["id"]
            if mutation == "structure": del request["structure_note"]
            if mutation == "boolean": edit["start"] = True
            if mutation == "definition": edit["letter"] = "D"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                process(request)

if __name__ == "__main__":
    unittest.main()
