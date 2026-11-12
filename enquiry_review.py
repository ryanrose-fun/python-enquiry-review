"""Underpin educational example: an enquiry becomes a human review task.

Run: python enquiry_review.py
Test: python enquiry_review.py --test
Standard library only. Fictional data. No AI call, network or message sending.
This is a new public example, not code from a client system.
"""
from dataclasses import dataclass, replace
import json
import sys
import unittest


@dataclass(frozen=True)
class Enquiry:
    reference: str
    project: str = ""
    location: str = ""
    timing: str = ""


@dataclass(frozen=True)
class ReviewTask:
    enquiry_reference: str
    missing_fields: tuple[str, ...]
    draft: str
    status: str = "awaiting_human_review"
    reviewer: str = ""
    sent: bool = False


def prepare_review(enquiry: Enquiry) -> ReviewTask:
    """Prepare a draft; do not invent absent details or send anything."""
    if not enquiry.reference.strip():
        raise ValueError("An enquiry reference is required")
    required = ("project", "location", "timing")
    missing = tuple(k for k in required if not getattr(enquiry, k).strip())
    if missing:
        draft = "Thanks for your enquiry. Please share your " + ", ".join(missing) + "."
    else:
        draft = (
            f"Thanks for the details about {enquiry.project.strip()} in "
            f"{enquiry.location.strip()}, with timing of {enquiry.timing.strip()}. "
            "Our team will review the scope before confirming feasibility or a quote."
        )
    return ReviewTask(enquiry.reference, missing, draft)


def approve(task: ReviewTask, reviewer: str) -> ReviewTask:
    """Record explicit human approval. Delivery is intentionally not implemented."""
    if task.status != "awaiting_human_review":
        raise ValueError("Only a pending task can be approved")
    if not reviewer.strip():
        raise ValueError("A named reviewer is required")
    return replace(task, status="approved_for_manual_use", reviewer=reviewer.strip())


class ReviewTests(unittest.TestCase):
    def test_missing_fields_are_requested(self):
        task = prepare_review(Enquiry("DEMO-1", project="CRM integration"))
        self.assertEqual(task.missing_fields, ("location", "timing"))
        self.assertEqual(task.status, "awaiting_human_review")
        self.assertFalse(task.sent)

    def test_whitespace_counts_as_missing(self):
        self.assertIn("project", prepare_review(Enquiry("DEMO-2", project="  ")).missing_fields)

    def test_complete_enquiry_has_no_invented_price(self):
        task = prepare_review(Enquiry("DEMO-3", "CRM integration", "Hampshire", "December"))
        self.assertEqual(task.missing_fields, ())
        self.assertIn("before confirming feasibility or a quote", task.draft)

    def test_approval_requires_reviewer_and_never_sends(self):
        task = prepare_review(Enquiry("DEMO-4"))
        with self.assertRaises(ValueError):
            approve(task, " ")
        approved = approve(task, "Demo reviewer")
        self.assertEqual(approved.status, "approved_for_manual_use")
        self.assertFalse(approved.sent)
        self.assertEqual(task.status, "awaiting_human_review")
        with self.assertRaises(ValueError):
            approve(approved, "Second reviewer")

    def test_reference_required(self):
        with self.assertRaises(ValueError):
            prepare_review(Enquiry(""))


if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        from dataclasses import asdict
        task = prepare_review(Enquiry("DEMO-001", "Connect CRM enquiries to review tasks"))
        print(json.dumps(asdict(task), indent=2))
        print("Fictional example. Nothing has been sent.")
