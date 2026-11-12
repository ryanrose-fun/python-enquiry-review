# Python enquiry review

A small, deterministic Python example showing how to turn an incomplete enquiry into a draft for human review, without inventing missing information or sending a message.

**Author:** [Ryan Rose](https://underpin.cloud/) · Freelance Software Engineer

## Quick start

Requires Python 3.10 or newer. No packages, credentials or external services are required.

```sh
git clone https://github.com/ryanrose-fun/python-enquiry-review.git
cd python-enquiry-review
python enquiry_review.py
python enquiry_review.py --test
```

The demo prints a JSON review task using fictional data. The test command runs five standard-library unit tests.

## Workflow

```text
Enquiry → validate reference → identify missing fields → prepare draft
                                                        ↓
                                                awaiting_human_review
                                                        ↓ named reviewer
                                                approved_for_manual_use
```

Approval records a reviewer on a new immutable task. It does **not** send anything.

## Design decisions

- Frozen dataclasses keep input and task records immutable.
- Missing project, location and timing fields are requested explicitly.
- Whitespace-only values count as missing information.
- A named reviewer is required for approval; a second approval is rejected.
- No model, network, database or email dependency makes the behaviour easy to reproduce.

## Tests

The included tests cover missing fields, whitespace, complete enquiries, approval validation and a required reference. CI runs the same suite across Python 3.10, 3.11 and 3.12.

## Scope and limitations

This is an educational example, originally published on [underpin.cloud](https://underpin.cloud/examples/enquiry_review.py). It uses fictional data and is not extracted from a client system. It is not an AI agent or a production messaging service.

A production implementation would additionally need persistence, identity and access controls, audit events, concurrency handling, delivery reconciliation and a defined data-retention policy. These are intentionally outside this example.

## Related work

- [Designing an AI workflow with human review](https://underpin.cloud/guides-ai-workflow-human-review)
- [Engineering portfolio](https://underpin.cloud/engineering)
- [Contact Ryan](mailto:ryan@underpin.cloud)
