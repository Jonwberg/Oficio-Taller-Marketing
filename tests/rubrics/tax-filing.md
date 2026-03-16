# Rubric: Tax Filing
**Agent:** Tax
**Deliverable:** Project revenue declaration at project close (Segment J)

## Schema (Execution Agent validates — pass/fail)
Required fields: rfc, revenue_amount, tax_jurisdiction, filing_period, cfdi_reference, deductibles

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present; all Controller invoices accounted for in revenue total; deductibles documented
3: Revenue total present but deductibles not documented
1: Revenue amount missing or RFC absent

**Accuracy (1–5)**
5: Revenue amount matches cumulative total of all Controller invoices for this project exactly; correct tax jurisdiction applied (Mexico — IVA 16% standard unless project-specific exception applies and is documented)
3: Minor discrepancy (< 1%) likely rounding; jurisdiction correct
1: Revenue amount significantly differs from Controller totals, or wrong tax jurisdiction applied

**Clarity (1–5)**
5: Filing is complete and self-contained; CFDI references traceable to Controller invoices
3: Mostly complete; one CFDI reference missing
1: Cannot trace filing back to source invoices

**State Sync (1–5)**
5: Tax filing task completed in Asana after project close confirmed by Vera
3: Filed but Asana not updated
1: No Asana update; filing not traceable

**Timing (1–5)**
5: Filed within required period after project close
3: Slight delay but within compliance window
1: Filed late or not filed

**Decision Readiness**
N/A — Tax filing is a compliance output; no human decision gate. Average score is calculated over 5 dimensions.

## Auto-Fail Conditions
- Revenue amount does not match Controller's invoiced total for the project
- RFC absent
- Filing incomplete
- Wrong tax jurisdiction applied
