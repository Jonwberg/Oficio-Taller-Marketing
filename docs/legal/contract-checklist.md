# Contract Preparation Checklist

Use this before sending the contract to a client. Every `[ ]` must be filled before the document goes out.

---

## Client Information
- [ ] Full legal name (as it appears on INE/passport)
- [ ] RFC (Mexican tax ID) — or passport number for foreign clients
- [ ] Legal address
- [ ] Phone number (with country code)
- [ ] Email address

## Project Information
- [ ] Project name (matches the Alcance document)
- [ ] Project address / location
- [ ] Total m² (matches the Alcance)
- [ ] Alcance document date

## Studio Information
- [ ] Studio legal entity name (confirm current: S. de R.L. de C.V. or personal)
- [ ] Studio RFC
- [ ] Studio address
- [ ] Representative name and title
- [ ] Payment account (CLABE or Wise — confirm it's current)

## Fees and Payments
- [ ] Total fee matches the Alcance exactly (including IVA)
- [ ] Total written in words (DOSCIENTOS MIL PESOS, etc.)
- [ ] Payment 1 amount = roughly 1/3 of total
- [ ] Payment 2 amount = roughly 1/3 of total
- [ ] Payment 3 amount = remainder
- [ ] Payment 1 due date = contract signing date or within 5 days
- [ ] Payment 2 due date = ~3 days before Fase 02 scheduled start
- [ ] Payment 3 due date = ~3 days before Fase 03 scheduled start
- [ ] Payments 1 + 2 + 3 = Total fee exactly

## Timeline
- [ ] Total weeks matches the Alcance
- [ ] Fase 01 weeks range filled (e.g., "Semanas 1–3")
- [ ] Fase 02 weeks range filled
- [ ] Fase 03 weeks range filled

## Final Review
- [ ] Both parties' names spelled correctly throughout
- [ ] Project name consistent throughout
- [ ] Contract date is today
- [ ] Alcance attached as Exhibit A / Anexo A
- [ ] Both signature blocks present with name and date line

---

## After Signing
- [ ] Save signed PDF as: `docs/legal/<project-id>-contrato-firmado.pdf`
- [ ] Update `project-status.json`: set `contract.signed: true` and `contract.signed_date`
- [ ] Create `campaigns/pending/<project-id>/project-status.json` from the template
- [ ] Fill all payment amounts and due dates in `project-status.json`
- [ ] Run `check-payment-gate.py <project-id> fase_01` to confirm gate is clear
