# Workflow Testing Framework Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude-native post-build QA framework that tests all 35 production agents across the 20-phase project delivery pipeline, scoring output quality against per-deliverable rubrics at every phase.

**Architecture:** Three runtime agents (Execution, Decision Gate, Gap Analysis) dispatch and evaluate real production agents with test seed data. Static files (test cases, seed data, quality rubrics) are written once and updated when the operating model changes. Entry point skills (`/test-segment`, `/test-full-run`) orchestrate test runs and write results to `tests/results/`.

**Tech Stack:** Claude Code agents (markdown), Claude Code skills (markdown), JSON seed data, Markdown rubrics and test cases. No Python. No external test runner.

**Spec:** `docs/superpowers/specs/2026-03-15-workflow-testing-framework-design.md`
**Production system:** `docs/superpowers/specs/2026-03-14-oficio-taller-agent-system-design.md`

---

## File Map

### New files to create

```
tests/
├── cases/
│   ├── TC-001-casa-moderna.md
│   ├── TC-002-casa-vista.md
│   ├── TC-003-wellness-retreat.md
│   ├── TC-004-centro-salud.md
│   ├── TC-005-biblioteca-municipal.md
│   ├── TC-006-edge-budget-mismatch.md
│   ├── TC-007-edge-bad-lead.md
│   └── TC-008-edge-site-complications.md
├── data/
│   ├── TC-001-seed.json
│   ├── TC-002-seed.json
│   ├── TC-003-seed.json
│   ├── TC-004-seed.json
│   ├── TC-005-seed.json
│   ├── TC-006-seed.json
│   ├── TC-007-seed.json
│   └── TC-008-seed.json
├── rubrics/
│   ├── lead-record.md
│   ├── lead-summary.md
│   ├── discovery-questionnaire.md
│   ├── client-fit-assessment.md
│   ├── area-program.md
│   ├── cost-basis.md
│   ├── site-readiness-report.md
│   ├── scope-of-work.md
│   ├── legal-review.md
│   ├── proposal.md
│   ├── client-communication.md
│   ├── concept-review.md
│   ├── architectural-design.md
│   ├── engineering-package.md
│   ├── budget-alignment.md
│   ├── executive-plans.md
│   ├── bid-comparison.md
│   ├── controller-invoice.md
│   ├── tax-filing.md
│   └── celia-decision-routing.md
├── agents/
│   ├── test-execution.md
│   ├── test-decision-gate.md
│   └── test-gap-analysis.md
└── skills/
    ├── test-segment.md
    └── test-full-run.md
```

### Modified files
- `plugin.json` — add 3 test agents + 2 test skills
- `.gitignore` — add `tests/results/`

---

## Chunk 1: Foundation — Directory Structure, Test Cases, Seed Data

### Task 1: Directory structure and .gitignore

**Files:**
- Create: `tests/cases/.gitkeep`, `tests/data/.gitkeep`, `tests/rubrics/.gitkeep`, `tests/agents/.gitkeep`, `tests/skills/.gitkeep`
- Modify: `.gitignore`

- [ ] **Step 1: Create directory tree**

```bash
mkdir -p tests/cases tests/data tests/rubrics tests/agents tests/skills tests/results
touch tests/cases/.gitkeep tests/data/.gitkeep tests/rubrics/.gitkeep tests/agents/.gitkeep tests/skills/.gitkeep
```

- [ ] **Step 2: Add results directory to .gitignore**

Add this line to `.gitignore`:
```
tests/results/
```

- [ ] **Step 3: Verify structure**

```bash
ls tests/
```
Expected: `agents  cases  data  rubrics  skills  results`

- [ ] **Step 4: Commit**

```bash
git add tests/ .gitignore
git commit -m "feat: scaffold tests directory structure"
```

---

### Task 2: TC-001 seed data and test case

**Files:**
- Create: `tests/data/TC-001-seed.json`
- Create: `tests/cases/TC-001-casa-moderna.md`

- [ ] **Step 1: Create TC-001 seed data**

Create `tests/data/TC-001-seed.json`:
```json
{
  "test_case_id": "TC-001",
  "scenario": "Casa Moderna",
  "project_type": "standalone_residential",
  "inbound_channel": "instagram",
  "inbound_message": "Hola, estoy buscando un arquitecto para diseñar mi casa en Los Cabos. Tengo un terreno de 2,500m² y quisiera algo moderno con piscina y terraza.",
  "lead_name": "Carlos Mendoza",
  "location": "Los Cabos, Baja California Sur",
  "site_area_sqm": 2500,
  "total_programmed_sqm": 250,
  "program": {
    "bedrooms": { "qty": 3, "avg_size_sqm": 18 },
    "bathrooms": { "qty": 3, "avg_size_sqm": 8 },
    "kitchen": { "qty": 1, "size_sqm": 20 },
    "dining_living": { "qty": 1, "size_sqm": 45 },
    "office": { "qty": 1, "size_sqm": 12 },
    "pool": { "qty": 1, "size_sqm": 35 },
    "patio": { "qty": 1, "size_sqm": 40 },
    "rooftop_terrace": { "qty": 1, "size_sqm": 5 },
    "service_areas": { "qty": 1, "size_sqm": 15 }
  },
  "special_features": ["pool", "rooftop_terrace", "solar"],
  "budget_range_usd": { "min": 300000, "max": 500000 },
  "site_conditions": "flat, no hydrology concerns",
  "client_profile": "design_engaged",
  "expected_outcome": "full_activation",
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 21600 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 16200 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 16200 }
  ],
  "total_architecture_fee_usd": 54000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-001"
}
```

- [ ] **Step 2: Create TC-001 test case definition**

Create `tests/cases/TC-001-casa-moderna.md`:
```markdown
# TC-001 — Casa Moderna

**Type:** standalone_residential
**Complexity:** Standard — happy path
**Seed data:** `tests/data/TC-001-seed.json`

## Scenario
Carlos Mendoza contacts via Instagram looking to design a 250sqm modern
residence in Los Cabos on a flat 2,500sqm site. Design-engaged client with
realistic budget ($300K–$500K). No site complications. Supervisor selected.

## Expected Flow
- Segment A: Lupe classifies as project_inquiry, creates lead record
- Segment B: Elena sends questionnaire, schedules meeting, fit approved
- Segment C: Ana produces area program (250sqm), cost basis prepared; Sol requests topo only (flat site)
- Segment D: Tomás generates SOW with standalone_residential template; architect approves both gates
- Segment E: All three prerequisites met simultaneously; Pablo builds timeline
- Segment F: Andrés produces concept package; Marcela approves (DG-07 = Pass to Agent test point)
- Segment G: Emilio completes all systems; Bruno confirms budget aligned
- Segment H: Hugo produces executive plans; Marcela approves
- Segment I: Ofelia collects 2+ bids; contractor selected; Paco submits permit
- Segment J: Construction starts; supervision active; project closes; Controller invoices; Tax files

## Key Verification Points
- standalone_residential SOW template applied (Segment D)
- No hydrologic study requested (flat site, Segment C)
- Pass to Agent simulated at DG-07 — Celia sets concept_in_progress, updates assigned_agent only
- All 11 Celia payload fields present at every Marcela gate
- route_to field (not routed_to) in payload

## Expected Final State
closed

## Edge Conditions
None — this is the baseline happy path used to calibrate rubric scoring.
```

- [ ] **Step 3: Verify files exist**

```bash
ls tests/data/ && ls tests/cases/
```
Expected: both TC-001 files listed.

- [ ] **Step 4: Commit**

```bash
git add tests/data/TC-001-seed.json tests/cases/TC-001-casa-moderna.md
git commit -m "feat: add TC-001 Casa Moderna test case and seed data"
```

---

### Task 3: TC-002 through TC-005 seed data and test cases

**Files:**
- Create: `tests/data/TC-002-seed.json` through `TC-005-seed.json`
- Create: `tests/cases/TC-002-casa-vista.md` through `TC-005-biblioteca-municipal.md`

- [ ] **Step 1: Create TC-002 seed data**

Create `tests/data/TC-002-seed.json`:
```json
{
  "test_case_id": "TC-002",
  "scenario": "Casa Vista",
  "project_type": "residential_in_development",
  "inbound_channel": "professional_contact",
  "inbound_message": "Buenas tardes, me recomendaron con ustedes. Tengo un lote en un fraccionamiento privado en San José del Cabo y quiero construir mi casa. Hay reglamento de construcción del fraccionamiento.",
  "lead_name": "Patricia Reyes",
  "location": "San José del Cabo, BCS — fraccionamiento privado",
  "site_area_sqm": 1200,
  "total_programmed_sqm": 320,
  "program": {
    "bedrooms": { "qty": 4, "avg_size_sqm": 20 },
    "bathrooms": { "qty": 4, "avg_size_sqm": 9 },
    "kitchen": { "qty": 1, "size_sqm": 25 },
    "dining_living": { "qty": 1, "size_sqm": 55 },
    "family_room": { "qty": 1, "size_sqm": 30 },
    "office": { "qty": 1, "size_sqm": 15 },
    "pool": { "qty": 1, "size_sqm": 40 },
    "terrace": { "qty": 2, "size_sqm": 20 },
    "service_areas": { "qty": 1, "size_sqm": 16 }
  },
  "special_features": ["pool", "solar", "smart_home"],
  "hoa_details": {
    "name": "Residencial Vista del Mar",
    "style_restrictions": "contemporary only, no flat roofs over 2 floors",
    "material_restrictions": "natural stone and stucco only on facade",
    "height_limit_m": 7
  },
  "budget_range_usd": { "min": 400000, "max": 700000 },
  "site_conditions": "slight slope, no hydrology concerns",
  "client_profile": "design_engaged",
  "expected_outcome": "full_activation",
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 27200 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 20400 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 20400 }
  ],
  "total_architecture_fee_usd": 68000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-002"
}
```

- [ ] **Step 2: Create TC-003 seed data**

Create `tests/data/TC-003-seed.json`:
```json
{
  "test_case_id": "TC-003",
  "scenario": "Wellness Retreat",
  "project_type": "commercial_hotel",
  "inbound_channel": "gmail",
  "inbound_message": "Hello, I'm developing a boutique wellness hotel in Todos Santos and am looking for an architectural firm. The project is approx 3,000sqm including 20 casitas, spa, restaurant, and pool. Budget around $3.5M USD.",
  "lead_name": "James Hartwell",
  "location": "Todos Santos, BCS",
  "site_area_sqm": 12000,
  "total_programmed_sqm": 3000,
  "program": {
    "casitas": { "qty": 20, "avg_size_sqm": 60 },
    "spa": { "qty": 1, "size_sqm": 300 },
    "restaurant": { "qty": 1, "size_sqm": 250 },
    "reception_lobby": { "qty": 1, "size_sqm": 150 },
    "pool_deck": { "qty": 1, "size_sqm": 400 },
    "staff_quarters": { "qty": 1, "size_sqm": 120 },
    "back_of_house": { "qty": 1, "size_sqm": 200 },
    "parking": { "qty": 1, "size_sqm": 320 }
  },
  "special_features": ["pool", "solar", "greywater_recycling", "av_system"],
  "budget_range_usd": { "min": 2000000, "max": 5000000 },
  "site_conditions": "rolling terrain, seasonal arroyo on south boundary",
  "client_profile": "design_engaged",
  "expected_outcome": "full_activation",
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 168000 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 126000 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 126000 }
  ],
  "total_architecture_fee_usd": 420000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-003"
}
```

- [ ] **Step 3: Create TC-004 seed data**

Create `tests/data/TC-004-seed.json`:
```json
{
  "test_case_id": "TC-004",
  "scenario": "Centro de Salud",
  "project_type": "commercial_health_center",
  "inbound_channel": "whatsapp",
  "inbound_message": "Buenos días, somos un grupo médico que quiere construir una clínica privada en La Paz. Necesitamos consultorios, área de urgencias, laboratorio y farmacia. Aprox 1,500m². Presupuesto de $1.8M USD.",
  "lead_name": "Dra. Carmen Valdez",
  "location": "La Paz, BCS",
  "site_area_sqm": 3500,
  "total_programmed_sqm": 1500,
  "program": {
    "consultorios": { "qty": 10, "avg_size_sqm": 20 },
    "urgencias": { "qty": 1, "size_sqm": 120 },
    "laboratorio": { "qty": 1, "size_sqm": 80 },
    "farmacia": { "qty": 1, "size_sqm": 60 },
    "recepcion_sala_espera": { "qty": 1, "size_sqm": 150 },
    "rayos_x": { "qty": 1, "size_sqm": 40 },
    "enfermeria": { "qty": 1, "size_sqm": 60 },
    "administracion": { "qty": 1, "size_sqm": 80 },
    "sanitarios": { "qty": 4, "avg_size_sqm": 15 },
    "estacionamiento": { "qty": 1, "size_sqm": 400 }
  },
  "special_features": ["medical_gas_systems", "specialized_hvac", "backup_generator"],
  "health_authority": "COFEPRIS",
  "budget_range_usd": { "min": 1000000, "max": 3000000 },
  "site_conditions": "flat urban lot, municipal services available",
  "client_profile": "design_engaged",
  "expected_outcome": "full_activation",
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 86400 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 64800 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 64800 }
  ],
  "total_architecture_fee_usd": 216000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-004"
}
```

- [ ] **Step 4: Create TC-005 seed data**

Create `tests/data/TC-005-seed.json`:
```json
{
  "test_case_id": "TC-005",
  "scenario": "Biblioteca Municipal",
  "project_type": "public_civic",
  "inbound_channel": "gmail",
  "inbound_message": "Estimados, el Municipio de Los Cabos está convocando firmas de arquitectura para el diseño de una nueva biblioteca pública de 2,000m². Presupuesto aprobado: $1.5M USD. El proyecto debe cumplir con los lineamientos de obra pública.",
  "lead_name": "Arq. Roberto Salinas — Dirección de Obras Públicas",
  "location": "Cabo San Lucas, BCS",
  "site_area_sqm": 5000,
  "total_programmed_sqm": 2000,
  "program": {
    "sala_lectura_adultos": { "qty": 1, "size_sqm": 400 },
    "sala_lectura_infantil": { "qty": 1, "size_sqm": 200 },
    "acervo_cerrado": { "qty": 1, "size_sqm": 300 },
    "sala_computo": { "qty": 1, "size_sqm": 150 },
    "sala_usos_multiples": { "qty": 1, "size_sqm": 200 },
    "administracion": { "qty": 1, "size_sqm": 150 },
    "sanitarios": { "qty": 4, "avg_size_sqm": 30 },
    "vestibulo": { "qty": 1, "size_sqm": 200 },
    "estacionamiento": { "qty": 1, "size_sqm": 250 }
  },
  "special_features": ["solar", "accessibility_compliance", "civic_art_space"],
  "procurement_type": "obra_publica",
  "budget_range_usd": { "min": 800000, "max": 2000000 },
  "site_conditions": "flat municipal land, no hydrology concerns",
  "client_profile": "institutional",
  "expected_outcome": "full_activation",
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 72000 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 54000 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 54000 }
  ],
  "total_architecture_fee_usd": 180000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-005"
}
```

- [ ] **Step 5: Create test case definition files TC-002 through TC-005**

Create `tests/cases/TC-002-casa-vista.md`:
```markdown
# TC-002 — Casa Vista

**Type:** residential_in_development
**Complexity:** Standard with HOA restrictions
**Seed data:** `tests/data/TC-002-seed.json`

## Scenario
Patricia Reyes — referral contact — wants a 320sqm home in a private
residential development in San José del Cabo. The development has strict
covenants: contemporary style only, natural stone/stucco facade, 7m height
limit.

## Key Verification Points
- Tomás applies `residential_in_development` template (Segment D)
- SOW includes HOA coordination clause and covenant review clause
- hoa_details from seed data referenced in scope
- Area program respects height limit implications for massing

## Expected Final State
closed
```

Create `tests/cases/TC-003-wellness-retreat.md`:
```markdown
# TC-003 — Wellness Retreat

**Type:** commercial_hotel
**Complexity:** High — large program, multiple systems
**Seed data:** `tests/data/TC-003-seed.json`

## Scenario
James Hartwell — international developer — building a 3,000sqm boutique
wellness hotel in Todos Santos. Seasonal arroyo on south boundary triggers
hydrologic study requirement. Multiple engineering systems required (solar,
greywater, AV).

## Key Verification Points
- Sol requests BOTH topo AND hydrologic study (seasonal arroyo, Segment C)
- Tomás applies `commercial_hotel` template with hospitality compliance clause
- Emilio coordinates all systems including greywater and AV (Segment G)
- Multiple bids collected and compared (Segment I)

## Expected Final State
closed
```

Create `tests/cases/TC-004-centro-salud.md`:
```markdown
# TC-004 — Centro de Salud

**Type:** commercial_health_center
**Complexity:** Specialized — health authority compliance
**Seed data:** `tests/data/TC-004-seed.json`

## Scenario
Medical group led by Dra. Carmen Valdez building a 1,500sqm private clinic
in La Paz. Requires COFEPRIS compliance, medical gas systems, specialized
HVAC, and backup generator.

## Key Verification Points
- Tomás applies `commercial_health_center` template with health authority compliance clause
- Emilio coordinates medical gas systems and specialized HVAC (non-standard engineering)
- SOW references COFEPRIS compliance as explicit deliverable

## Expected Final State
closed
```

Create `tests/cases/TC-005-biblioteca-municipal.md`:
```markdown
# TC-005 — Biblioteca Municipal

**Type:** public_civic
**Complexity:** Civic — public procurement rules
**Seed data:** `tests/data/TC-005-seed.json`

## Scenario
Municipality of Los Cabos commissioning a 2,000sqm public library via
official public works procurement process. Budget approved at government
level. Compliance with obra pública guidelines required.

## Key Verification Points
- Tomás applies `public_civic` template with civic procurement and public bidding clauses
- Client is institutional — fit assessment adjusts for organizational decision-making (not individual)
- Permit process expected to be longer (public project)

## Expected Final State
closed
```

- [ ] **Step 6: Commit**

```bash
git add tests/data/ tests/cases/
git commit -m "feat: add TC-002 through TC-005 test cases and seed data"
```

---

### Task 4: TC-006, TC-007, TC-008 edge case seed data and test cases

**Files:**
- Create: `tests/data/TC-006-seed.json`, `TC-007-seed.json`, `TC-008-seed.json`
- Create: `tests/cases/TC-006-edge-budget-mismatch.md`, `TC-007-edge-bad-lead.md`, `TC-008-edge-site-complications.md`

- [ ] **Step 1: Create TC-006 edge case seed data (budget mismatch)**

Create `tests/data/TC-006-seed.json`:
```json
{
  "test_case_id": "TC-006",
  "scenario": "Edge — Budget Mismatch",
  "project_type": "standalone_residential",
  "inbound_channel": "instagram",
  "inbound_message": "Hola, quiero una casa de 3 recámaras con alberca en Los Cabos. Mi presupuesto es de $200,000 USD.",
  "lead_name": "Miguel Torres",
  "location": "Los Cabos, BCS",
  "site_area_sqm": 800,
  "total_programmed_sqm": 220,
  "program": {
    "bedrooms": { "qty": 3, "avg_size_sqm": 18 },
    "bathrooms": { "qty": 3, "avg_size_sqm": 8 },
    "kitchen": { "qty": 1, "size_sqm": 18 },
    "dining_living": { "qty": 1, "size_sqm": 40 },
    "pool": { "qty": 1, "size_sqm": 35 },
    "patio": { "qty": 1, "size_sqm": 30 },
    "service_areas": { "qty": 1, "size_sqm": 15 }
  },
  "special_features": ["pool"],
  "budget_range_usd": { "min": 150000, "max": 200000 },
  "site_conditions": "flat, no hydrology concerns",
  "client_profile": "budget_constrained",
  "expected_outcome": "budget_misalignment_then_redesign",
  "contractor_pricing_usd": 380000,
  "redesign_scope": "remove pool, reduce living area to 160sqm",
  "redesigned_contractor_pricing_usd": 195000,
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 12000 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 9000 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 9000 }
  ],
  "total_architecture_fee_usd": 30000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-006"
}
```

- [ ] **Step 2: Create TC-007 edge case seed data (bad lead)**

Create `tests/data/TC-007-seed.json`:
```json
{
  "test_case_id": "TC-007",
  "scenario": "Edge — Bad Lead",
  "project_type": null,
  "inbound_channel": "instagram",
  "inbound_message": "Hola! Soy representante de una empresa de marketing digital. Podemos aumentar tus seguidores en Instagram por solo $99 USD al mes. Contáctanos en www.seguidores-fake.com",
  "lead_name": "unknown",
  "location": null,
  "site_area_sqm": null,
  "total_programmed_sqm": null,
  "program": null,
  "special_features": [],
  "budget_range_usd": null,
  "site_conditions": null,
  "client_profile": "spam",
  "expected_outcome": "discarded_at_screening",
  "architect_response": null,
  "payment_schedule": null,
  "total_architecture_fee_usd": null,
  "tax_jurisdiction": null,
  "currency": null,
  "rfc": null
}
```

- [ ] **Step 3: Create TC-008 edge case seed data (site complications)**

Create `tests/data/TC-008-seed.json`:
```json
{
  "test_case_id": "TC-008",
  "scenario": "Edge — Site Complications",
  "project_type": "commercial_hotel",
  "inbound_channel": "gmail",
  "inbound_message": "Good morning, I have a 15,000sqm property in East Cape with a small stream running through it. Interested in building a boutique hotel — 15 rooms, restaurant, infinity pool. Budget $2.5M USD.",
  "lead_name": "David Chen",
  "location": "East Cape, BCS",
  "site_area_sqm": 15000,
  "total_programmed_sqm": 2000,
  "program": {
    "rooms": { "qty": 15, "avg_size_sqm": 55 },
    "restaurant": { "qty": 1, "size_sqm": 200 },
    "pool_deck": { "qty": 1, "size_sqm": 300 },
    "reception": { "qty": 1, "size_sqm": 100 },
    "back_of_house": { "qty": 1, "size_sqm": 150 },
    "staff": { "qty": 1, "size_sqm": 80 }
  },
  "special_features": ["infinity_pool", "solar", "greywater_recycling"],
  "budget_range_usd": { "min": 1500000, "max": 4000000 },
  "site_conditions": "steep slope on west side, stream running through northeast corner — hydrology study required",
  "hydrology_risk": "stream proximity requires setback analysis and possible retention basin",
  "activation_blocker": "hydrologic study pending — estimated 6 weeks",
  "client_profile": "design_engaged",
  "expected_outcome": "activation_delayed_by_hydrology",
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 120000 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 90000 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 90000 }
  ],
  "total_architecture_fee_usd": 300000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-008"
}
```

- [ ] **Step 4: Create edge case test case definition files**

Create `tests/cases/TC-006-edge-budget-mismatch.md`:
```markdown
# TC-006 — Edge: Budget Mismatch

**Type:** standalone_residential
**Complexity:** Edge case — budget misalignment requiring redesign
**Seed data:** `tests/data/TC-006-seed.json`

## Scenario
Miguel Torres wants a 220sqm house with pool in Los Cabos on a $200K budget.
Contractor pricing at Segment G comes in at $380K — nearly double the budget.
Bruno recommends redesign: remove pool, reduce to 160sqm. After redesign,
contractor pricing at $195K aligns with budget.

## Key Verification Points
- DG-09 (Budget Alignment): Bruno simulates Reject — budget_misaligned state set
- Redesign loop triggers (back to Felipe per feedback_type)
- After redesign: second DG-09 produces budget_aligned state
- Executive plans only begin after budget_aligned confirmed

## Expected Final State
closed (after redesign loop resolves)

## Edge Conditions
- budget_misaligned state must be set before redesign — not skipped
- executive_plans_in_progress must NOT appear before budget_aligned
```

Create `tests/cases/TC-007-edge-bad-lead.md`:
```markdown
# TC-007 — Edge: Bad Lead (Spam)

**Type:** N/A
**Complexity:** Edge case — spam detection and discard
**Seed data:** `tests/data/TC-007-seed.json`

## Scenario
An Instagram DM from a fake marketing account offering social media followers.
Lupe should detect this as spam, archive the lead, and trigger no downstream agents.

## Key Verification Points
- Lupe classifies category as "spam" (Segment A)
- No lead summary sent to Marcela — lead archived immediately
- No Elena, Ana, Sol, or any downstream agent dispatched
- Asana lead task created with status "discarded"
- Final state: lead_screened (not lead_summary_sent_to_marcela)

## Expected Final State
lead_screened (discarded, not forwarded)

## Edge Conditions
- This test STOPS at Segment A — do not continue to Segment B
- A false positive (legitimate lead incorrectly classified as spam) would be a Critical failure
```

Create `tests/cases/TC-008-edge-site-complications.md`:
```markdown
# TC-008 — Edge: Site Complications

**Type:** commercial_hotel
**Complexity:** Edge case — hydrology blocker at activation gate
**Seed data:** `tests/data/TC-008-seed.json`

## Scenario
David Chen has a 15,000sqm East Cape property with a stream through it.
Sol identifies that a hydrologic study is required (6-week timeline).
The activation gate is blocked until the study arrives.

## Key Verification Points
- Sol requests BOTH topo AND hydrologic study (stream present, Segment C)
- Blocker logged in Asana: activation_delayed_by_hydrology
- Vera holds activation gate — does NOT activate until study received
- site_data_pending state persists until hydrology resolved

## Expected Final State
project_activated (once hydrology study received and activation prerequisites met)

## Edge Conditions
- Site data blocker must be logged explicitly — not silently waited on
- Activation must not proceed until ALL three prerequisites satisfied
```

- [ ] **Step 5: Verify all 8 test cases and seed files exist**

```bash
ls tests/cases/ | wc -l && ls tests/data/ | wc -l
```
Expected: `8` and `8`

- [ ] **Step 6: Commit**

```bash
git add tests/data/ tests/cases/
git commit -m "feat: add TC-006 through TC-008 edge case test cases and seed data"
```

---

## Chunk 2: Quality Rubrics

### Task 5: Lead and discovery rubrics

**Files:**
- Create: `tests/rubrics/lead-record.md`, `lead-summary.md`, `discovery-questionnaire.md`, `client-fit-assessment.md`

- [ ] **Step 1: Create lead-record rubric**

Create `tests/rubrics/lead-record.md`:
```markdown
# Rubric: Lead Record
**Agent:** Lupe
**Deliverable:** Asana lead task created on inbound message receipt

## Schema (Execution Agent validates — pass/fail)
Required fields: source_channel, category, received_at, summary, status

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All custom fields populated, raw message stored verbatim in task body
3: All fields present but raw message summarized not preserved verbatim
1: Any required field missing

**Accuracy (1–5)**
5: source_channel exactly matches inbound platform; category correctly classified
3: source_channel correct, category could be argued either way
1: Wrong platform identified or wrong category

**Clarity (1–5)**
5: Summary in task body is immediately scannable — project type, location, client name visible
3: Summary present but requires reading to understand context
1: Summary is absent or a raw paste with no structure

**State Sync (1–5)**
5: Asana task created with status = "new", correct section, correct project tag
3: Task created but in wrong section or missing tag
1: No Asana task created

**Timing (1–5)**
5: Task created within expected window after inbound message receipt
3: Minor delay but task exists
1: Task missing or significantly delayed

**Decision Readiness (1–5)**
N/A for lead record — this deliverable feeds Marcela's review, not a standalone decision

## Auto-Fail Conditions
- No Asana task created
- received_at field missing
- status field absent
- Legitimate lead classified as spam (false positive) — Critical failure
```

- [ ] **Step 2: Create lead-summary rubric**

Create `tests/rubrics/lead-summary.md`:
```markdown
# Rubric: Lead Summary
**Agent:** Lupe
**Deliverable:** Structured summary sent to Marcela for review (DG-01)

## Schema (Execution Agent validates — pass/fail)
Required fields: project_name, source_channel, raw_message, initial_assessment, recommended_action

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Source, channel, raw message, classification, and initial assessment all present
3: Most fields present, one minor omission
1: Missing source or raw message

**Accuracy (1–5)**
5: Project type classified correctly; legitimacy assessment is defensible
3: Classification approximately right but arguable
1: Wrong classification or legitimacy assessment contradicts message content

**Clarity (1–5)**
5: Marcela can make approve/reject/pass decision in under 30 seconds from this summary
3: Summary provides context but requires a follow-up read of the raw message
1: Unclear or confusing; Marcela cannot decide without more information

**State Sync (1–5)**
5: Asana state updated to lead_summary_sent_to_marcela
3: Summary sent but Asana state not updated
1: Neither sent nor state updated

**Timing (1–5)**
5: Summary sent promptly after lead creation
3: Minor delay, summary eventually sent
1: Summary never sent or excessive delay

**Decision Readiness (1–5)**
5: Summary includes a clear recommended action (approve / reject / pass) with brief rationale
3: Context provided but no recommendation
1: Summary requires Marcela to research before deciding

## Auto-Fail Conditions
- Summary is empty
- source field is missing
- Classification is "unknown" without written explanation
```

- [ ] **Step 3: Create discovery-questionnaire rubric**

Create `tests/rubrics/discovery-questionnaire.md`:
```markdown
# Rubric: Discovery Questionnaire
**Agent:** Elena
**Deliverable:** Questionnaire sent to lead after Marcela approval (Segment B)

## Schema (Execution Agent validates — pass/fail)
Required fields: sent_to, sent_at, project_type_question, budget_question, timeline_question, location_question

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Covers all 8 required topics: project type, approximate size, site location, budget range, desired timeline, special requirements, design style preferences, site ownership status
3: 6–7 topics covered, one minor omission
1: Missing budget or project type question

**Accuracy (1–5)**
5: Questions are tailored to the project type from the lead summary (residential vs commercial vs civic)
3: Generic questionnaire sent without project type adjustment
1: Questions are inappropriate for the lead context

**Clarity (1–5)**
5: Questions are conversational, warm, and inviting — not a bureaucratic form
3: Questions are clear but feel formal or cold
1: Questions are confusing or off-putting

**State Sync (1–5)**
5: Asana state updated to followup_sent; lead status updated to "responded" when reply received
3: Questionnaire sent but Asana not updated
1: No state update

**Timing (1–5)**
5: Questionnaire sent within 24h of lead qualification
3: Sent within 48h
1: Sent after 48h or not at all

**Decision Readiness (1–5)**
5: Questionnaire will produce responses that allow Elena to prepare a complete fit assessment
3: Most questions are useful; one or two gaps in coverage
1: Questionnaire will not produce enough information for fit assessment

## Auto-Fail Conditions
- Questionnaire sent to wrong contact (not the inbound lead)
- Budget question absent
- Project type not addressed
```

- [ ] **Step 4: Create client-fit-assessment rubric**

Create `tests/rubrics/client-fit-assessment.md`:
```markdown
# Rubric: Client Fit Assessment
**Agent:** Elena
**Deliverable:** Fit summary sent to Marcela after first meeting (DG-02)

## Schema (Execution Agent validates — pass/fail)
Required fields: meeting_notes, assessment_dimensions, recommendation, rationale

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All four assessment dimensions present: design engagement level, budget realism relative to program, scope clarity, collaborative working style indicators
3: Three of four dimensions present
1: Missing design engagement or budget realism assessment

**Accuracy (1–5)**
5: Meeting notes attributed correctly (what the client said vs Elena's interpretation clearly separated)
3: Notes summarized but attribution clear from context
1: Notes mixed with interpretation, no way to distinguish

**Clarity (1–5)**
5: Recommendation is explicit — "proceed", "decline", or "request more information" — no ambiguity
3: Recommendation implied but not stated directly
1: No recommendation present

**State Sync (1–5)**
5: Asana state updated to discovery_completed; fit summary sent to Marcela via correct channel
3: Summary sent but state not updated
1: Neither summary sent nor state updated

**Timing (1–5)**
5: Fit assessment sent to Marcela within 24h of first meeting
3: Sent within 48h
1: Not sent or excessive delay

**Decision Readiness (1–5)**
5: Any red flags documented with specific evidence from meeting; Marcela can decide immediately
3: Red flags mentioned but not substantiated
1: Marcela cannot make a fit decision from this assessment without follow-up

## Auto-Fail Conditions
- No explicit recommendation (proceed / decline / more info)
- Any of the four required assessment dimensions missing
```

- [ ] **Step 5: Verify rubric files**

```bash
ls tests/rubrics/
```
Expected: 4 files listed.

- [ ] **Step 6: Commit**

```bash
git add tests/rubrics/
git commit -m "feat: add lead and discovery rubrics"
```

---

### Task 6: Pre-scope and scope rubrics

**Files:**
- Create: `tests/rubrics/area-program.md`, `cost-basis.md`, `site-readiness-report.md`, `scope-of-work.md`, `legal-review.md`, `proposal.md`, `client-communication.md`

- [ ] **Step 1: Create area-program rubric**

Create `tests/rubrics/area-program.md`:
```markdown
# Rubric: Area Program
**Agent:** Ana
**Deliverable:** Room-by-room area matrix (Segment C)

## Schema (Execution Agent validates — pass/fail)
Required fields: spaces (array with name, qty, size_sqm per entry), total_sqm, assumptions

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Every space from seed data program has name, quantity, and size in sqm; special features that are programmed spaces (pool, rooftop) included with size
3: All spaces present but one or two missing size values
1: Total sqm missing, or any programmed space has no size

**Accuracy (1–5)**
5: Total programmed sqm correctly calculated and matches sum of all spaces
3: Total present but off by minor rounding
1: Total missing or significantly wrong

**Clarity (1–5)**
5: Matrix is readable as standalone document; no conversation context needed
3: Matrix understandable but requires some context
1: Matrix not readable without back-reference to client conversation

**State Sync (1–5)**
5: Asana state updated to area_program_in_progress then area_program_confirmed
3: State partially updated
1: No Asana update

**Timing (1–5)**
5: Area program delivered within expected window after fit approval
3: Minor delay
1: Not delivered or excessive delay

**Decision Readiness (1–5)**
5: Assumptions documented where client input was incomplete; Marcela can review with full context
3: Assumptions partially documented
1: No assumptions section; Marcela cannot evaluate validity of program

## Auto-Fail Conditions
- total_sqm missing
- Any programmed space has no size value
- No assumptions section
```

- [ ] **Step 2: Create cost-basis rubric**

Create `tests/rubrics/cost-basis.md`:
```markdown
# Rubric: Cost Basis
**Agent:** Ana
**Deliverable:** Preliminary cost estimate (Segment C, reviewed at DG-03)

## Schema (Execution Agent validates — pass/fail)
Required fields: cost_per_sqm, base_construction_cost, architecture_fee_pct, architecture_fee, engineering_allowance, contingency_pct, total_estimate, assumptions

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present: cost/sqm basis with source, base cost, arch fee %, arch fee $, engineering allowance, contingency %, total, assumptions list
3: Most fields present, one minor omission
1: Total missing or architecture fee absent

**Accuracy (1–5)**
5: Math is correct — base cost = area × cost/sqm; total = sum of all components
3: Small arithmetic error but structure is right
1: Major calculation error or unsupported cost/sqm claim

**Clarity (1–5)**
5: Clearly labeled as preliminary estimate; assumptions documented with specifics
3: Labeled as preliminary but assumptions generic
1: Not labeled as preliminary; no assumptions

**State Sync (1–5)**
5: Asana cost_basis_ready state set; linked to area program task
3: State set but not linked
1: No Asana update

**Timing (1–5)**
5: Cost basis produced concurrently with area program finalization
3: Slight lag but produced before DG-03
1: Not produced before Marcela review

**Decision Readiness (1–5)**
5: Marcela can assess budget feasibility immediately from this document
3: Some gaps but general picture clear
1: Cannot assess budget feasibility from this document

## Auto-Fail Conditions
- No assumptions section
- Total estimate missing
- Architecture fee absent
```

- [ ] **Step 3: Create site-readiness-report rubric**

Create `tests/rubrics/site-readiness-report.md`:
```markdown
# Rubric: Site Readiness Report
**Agent:** Sol
**Deliverable:** Site document request and status update (Segment C — Vera status update, not Celia gate)

## Schema (Execution Agent validates — pass/fail)
Required fields: required_documents, request_sent_at, current_status, blockers

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Required documents correctly identified based on site_conditions from seed data; topo always required; hydrologic study required when stream/slope/wetland present
3: Topo requested but hydrologic study missed when conditions warrant it
1: Topo not included in requirements

**Accuracy (1–5)**
5: Document requirements match site conditions exactly (no over-requesting, no under-requesting)
3: One document over-requested or slightly wrong
1: Wrong documents requested for site type

**Clarity (1–5)**
5: Client receives clear instructions with document specifications and deadline
3: Instructions sent but deadline missing
1: No clear instructions to client

**State Sync (1–5)**
5: Asana state updated from site_data_pending to site_data_complete when received; blocker logged when overdue
3: Status updated but blocker not logged when overdue
1: No Asana update

**Timing (1–5)**
5: Document request issued concurrently with area program work (parallel tracks)
3: Minor lag but within acceptable window
1: Request not issued until after area program complete (defeats purpose of parallel track)

**Decision Readiness (1–5)**
5: Vera can assess activation readiness from this report at any time
3: Status readable but incomplete
1: Vera cannot assess document readiness

## Auto-Fail Conditions
- Topo map not included in requirements
- No Asana status update
- Blocker not logged when documents are overdue and activation is pending
```

- [ ] **Step 4: Create scope-of-work rubric**

Create `tests/rubrics/scope-of-work.md`:
```markdown
# Rubric: Scope of Work
**Agent:** Tomás
**Deliverable:** Full SOW document (Segment D, reviewed at DG-04)

## 20-Item Checklist (all must be present)
1. Conceptual design phase defined with deliverables
2. Architectural design phases defined with deliverables
3. Executive architectural plans included with deliverables
4. Optional architectural supervision clause included
5. Landscape architecture scope stated (or explicitly excluded)
6. Structural engineering collaboration defined
7. Electrical engineering scope included
8. Lighting design scope stated
9. Water systems scope defined
10. Irrigation scope included (or explicitly excluded)
11. Solar systems scope included (or explicitly excluded)
12. Local contractor cost validation planned
13. Payment schedule with milestone names, percentages, and trigger events
14. Deliverables listed by phase with specifics
15. Responsibilities matrix assigning every major deliverable to a named party
16. Exclusions documented with specifics (not generic)
17. Revision assumptions stated per phase
18. Timeline structure clear with phase sequence
19. Project-type-specific clauses included (see below)
20. E-signature path defined

## Project-Type Clause Requirements
- standalone_residential: standard residential clauses
- residential_in_development: HOA coordination clause + covenant review clause
- commercial_hotel: hospitality compliance clause + brand standards coordination
- commercial_health_center: health authority compliance clause + medical equipment coordination
- public_civic: civic procurement clause + public bidding compliance

## Schema (Execution Agent validates — pass/fail)
Required sections: scope_phases, payment_schedule, responsibilities_matrix, exclusions, revision_assumptions, project_type_clauses

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All 20 checklist items present and complete; correct project-type-specific clauses applied
3: 17–19 items present; project-type clause missing or incomplete
1: Any of items 1, 2, 3, 13, 15, 16 missing (critical sections)

**Accuracy (1–5)**
5: Deliverables per phase match the production pipeline exactly; responsibilities name real parties
3: Minor mismatch in deliverable description but structure correct
1: Wrong project type template applied

**Clarity (1–5)**
5: Client can sign this document with full understanding of what they are buying
3: Clear to a professional but dense for a client
1: Ambiguous scope or unclear deliverables

**State Sync (1–5)**
5: Asana state updated to scope_in_preparation then scope_sent_for_architect_review
3: Partial update
1: No Asana update

**Timing (1–5)**
5: SOW produced within expected window after area program and cost basis confirmed
3: Minor delay
1: Not produced or excessive delay

**Decision Readiness (1–5)**
5: Architect reviewer can approve or flag specific sections immediately
3: Document ready but some sections need clarification
1: Architect cannot evaluate without significant additional information

## Auto-Fail Conditions
- Payment schedule missing
- Exclusions section absent
- Project type template not applied (wrong or generic clauses)
- Any of the 20 checklist items completely absent
```

- [ ] **Step 5: Create legal-review rubric**

Create `tests/rubrics/legal-review.md`:
```markdown
# Rubric: Legal Review
**Agent:** Legal
**Deliverable:** Clause review of proposal before architect approval gate (Segment D, DG-05)

## Schema (Execution Agent validates — pass/fail)
Required fields: reviewed_by, reviewed_at, ip_rights_status, compliance_flags, approval_status

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All proposal clauses reviewed; IP and usage rights addressed; project-type-specific compliance verified
3: Most sections reviewed; IP rights checked but compliance flags generic
1: IP section not reviewed

**Accuracy (1–5)**
5: Compliance issues correctly identified with proposed resolution paths
3: Flag raised but resolution path not proposed
1: Known compliance issue missed

**Clarity (1–5)**
5: Output is either a clean approval or a specific flag list with resolution — no ambiguity
3: Mostly clear but some "may need to review" language
1: "Looks okay" without evidence of review

**State Sync (1–5)**
5: Asana legal review task completed; result linked to proposal task
3: Review done but not linked
1: No Asana update

**Timing (1–5)**
5: Review completed concurrently with Renata's proposal assembly (parallel)
3: Minor lag but done before architect gate
1: Not done before architect gate fires

**Decision Readiness (1–5)**
5: Vera can proceed to architect gate immediately on clean approval; flags are actionable
3: Approval given but some ambiguity remains
1: Cannot determine if it is safe to proceed

## Auto-Fail Conditions
- IP and usage rights section not reviewed
- Approval given with open unresolved flags
- No evidence that the full proposal was reviewed
```

- [ ] **Step 6: Create proposal rubric**

Create `tests/rubrics/proposal.md`:
```markdown
# Rubric: Proposal
**Agent:** Renata
**Deliverable:** Full client-facing proposal (Segment D, DG-05)

## Schema (Execution Agent validates — pass/fail)
Required sections: scope_summary, budget_detail, timeline_phases, process_narrative, bilingual (es + en)

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All sections present in both Spanish and English; no placeholders; SOW, budget, timeline, and narrative all complete
3: All sections present but one language version incomplete
1: Missing language version (Spanish or English), or placeholder text present

**Accuracy (1–5)**
5: SOW section reflects Tomás's approved scope exactly; budget matches Bruno's figures exactly
3: Minor wording differences but no material changes to scope or figures
1: Budget figures differ from Bruno's estimates

**Clarity (1–5)**
5: Client-ready — professional, no internal notes, no agent commentary, no jargon
3: Mostly client-ready but minor internal artifact remains
1: Internal notes or agent commentary visible in document

**State Sync (1–5)**
5: Asana state shows proposal ready for architect review
3: Proposal assembled but state not updated
1: No Asana update

**Timing (1–5)**
5: Proposal assembled promptly after Bruno's budget and SOW approval
3: Minor delay
1: Not assembled or excessive delay

**Decision Readiness (1–5)**
5: Architect can approve or flag specific sections with no additional context needed
3: Mostly ready but one section needs clarification
1: Architect cannot evaluate without back-and-forth

## Auto-Fail Conditions
- Spanish language version missing
- English language version missing
- Placeholder text present
- Budget does not match Bruno's figures
```

- [ ] **Step 7: Create client-communication rubric**

Create `tests/rubrics/client-communication.md`:
```markdown
# Rubric: Client Communication
**Agent:** Rosa
**Deliverable:** Any outbound client message (status updates, proposals, revision acknowledgements)

## Schema (Execution Agent validates — pass/fail)
Required fields: channel, message_body, project_reference, status (draft — awaiting approval)

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Message includes project name, relevant context, clear action requested
3: Project name present but context incomplete
1: No project reference

**Accuracy (1–5)**
5: Message accurately reflects the current project state and any decisions made
3: Mostly accurate but one minor factual gap
1: Inaccurate or misleading information about project status

**Clarity (1–5)**
5: One clear next step for the client; no ambiguity about what is expected of them
3: Next step implied but not explicit
1: Client cannot determine what to do from this message

**State Sync (1–5)**
5: Message in draft status — Marcela approval required before send; Asana status updated after approval
3: Draft but Asana not updated
1: Message sent without Marcela approval

**Timing (1–5)**
5: Message drafted promptly after triggering event
3: Minor delay
1: Significant delay or message not drafted

**Decision Readiness (1–5)**
5: Marcela can approve this message in under 60 seconds
3: Message nearly ready but one phrase needs adjustment
1: Message requires significant rework before approval

## Auto-Fail Conditions
- Message sent without Marcela approval
- Project reference missing
- Confidential internal information included in client-facing message
```

- [ ] **Step 8: Verify rubrics**

```bash
ls tests/rubrics/ | wc -l
```
Expected: `11` (4 from Task 5 + 7 from this task)

- [ ] **Step 9: Commit**

```bash
git add tests/rubrics/
git commit -m "feat: add pre-scope and scope quality rubrics"
```

---

### Task 7: Design, engineering, and final phase rubrics

**Files:**
- Create: `concept-review.md`, `architectural-design.md`, `engineering-package.md`, `budget-alignment.md`, `executive-plans.md`, `bid-comparison.md`, `controller-invoice.md`, `tax-filing.md`, `celia-decision-routing.md`

- [ ] **Step 1: Create concept-review rubric**

Create `tests/rubrics/concept-review.md`:
```markdown
# Rubric: Concept Design Review
**Agent:** Andrés
**Deliverable:** Concept design package readiness confirmation (Segment F, DG-07)

## Schema (Execution Agent validates — pass/fail)
Required fields: deliverables_checklist (3d_model, renders, material_direction, color_direction, space_arrangement), presentation_milestone, review_notes

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All five deliverables confirmed complete; in-person presentation logged as milestone with date
3: Four of five deliverables confirmed; presentation logged
1: Any deliverable unconfirmed, or presentation not logged

**Accuracy (1–5)**
5: Review notes capture Marcela's specific feedback — not just "approved"
3: Approval captured but feedback generic
1: No review notes; just a status flag

**Clarity (1–5)**
5: Any revision notes are specific and actionable for the design team (room X needs Y)
3: Revision direction given but not specific to particular spaces
1: Revision notes vague or absent when revision was required

**State Sync (1–5)**
5: State moves concept_in_progress → concept_ready_for_review → concept_approved (or concept_rejected + revision)
3: State updated but intermediate state skipped
1: No state update

**Timing (1–5)**
5: Concept package ready within expected window after project activation
3: Minor delay
1: Significant delay or concept not produced

**Decision Readiness (1–5)**
5: Marcela can approve or reject the concept with the information in this package
3: Mostly ready but one deliverable needs clarification
1: Marcela cannot evaluate concept without additional material

## Auto-Fail Conditions
- Any of the five deliverables unconfirmed
- In-person presentation milestone not logged
```

- [ ] **Step 2: Create architectural-design rubric**

Create `tests/rubrics/architectural-design.md`:
```markdown
# Rubric: Architectural Design
**Agent:** Felipe
**Deliverable:** Detailed architectural design set (Segment F, DG-08)

## Schema (Execution Agent validates — pass/fail)
Required fields: design_set_status, concept_reflection_confirmed, area_program_compliance, structural_coordination_notes

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Design set reflects approved concept; all rooms from area program present; structural coordination notes included; material specs consistent with concept approval
3: Most rooms present; one minor program omission
1: Rooms missing from area program, or concept not reflected

**Accuracy (1–5)**
5: No unexplained departures from approved concept; sizes match area program targets
3: Minor size variance but program intent preserved
1: Major departure from concept without documented reason

**Clarity (1–5)**
5: Design is complete enough for engineering handoff — no open design questions remain
3: Mostly complete; one area flagged for later resolution
1: Multiple open design questions remain before engineering can begin

**State Sync (1–5)**
5: State moves architectural_design_in_progress → architectural_design_approved
3: State updated but intermediate tracking missing
1: No state update

**Timing (1–5)**
5: Architectural design delivered within expected window after concept approval
3: Minor delay
1: Significant delay or design not produced

**Decision Readiness (1–5)**
5: Marcela can approve and hand off to Emilio immediately
3: Nearly ready; one clarification needed
1: Design cannot proceed to engineering without rework

## Auto-Fail Conditions
- Rooms from area program missing in design
- Concept not reflected (unexplained departures)
- No structural coordination notes
```

- [ ] **Step 3: Create engineering-package rubric**

Create `tests/rubrics/engineering-package.md`:
```markdown
# Rubric: Engineering Package
**Agent:** Emilio
**Deliverable:** Complete engineering coordination package (Segment G, feeds DG-09)

## Schema (Execution Agent validates — pass/fail)
Required fields: systems_status (structural, electrical, lighting, water), conditional_systems, all_inputs_confirmed, conflicts_resolved

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required systems present and confirmed (structural, electrical, lighting, water); conditional systems addressed (irrigation if landscaping in scope, solar if in scope, AV if in scope); no pending consultant inputs
3: Required systems present; one conditional system not addressed
1: Any required system absent

**Accuracy (1–5)**
5: Engineering package explicitly declared complete and ready for budget alignment; all consultant inputs confirmed received
3: Mostly complete but one consultant input still pending
1: Pending inputs declared complete when they are not

**Clarity (1–5)**
5: Any design conflicts identified during engineering are documented with proposed resolutions
3: Conflicts noted but not resolved
1: Conflicts ignored or not documented

**State Sync (1–5)**
5: States move structural_engineering_in_progress and systems_engineering_in_progress to budget_alignment_pending
3: State partially updated
1: No state update

**Timing (1–5)**
5: Engineering package complete within expected window after architectural design approval
3: Minor delay (external consultant timeline is acceptable reason)
1: Package declared incomplete or significantly delayed without documented reason

**Decision Readiness (1–5)**
5: Bruno can proceed to contractor pricing immediately
3: Mostly ready; one minor item outstanding
1: Cannot proceed to budget alignment without additional engineering work

## Auto-Fail Conditions
- Any required system absent (structural, electrical, lighting, water)
- Pending consultant inputs undeclared when package marked complete
```

- [ ] **Step 4: Create budget-alignment rubric**

Create `tests/rubrics/budget-alignment.md`:
```markdown
# Rubric: Budget Alignment Analysis
**Agent:** Bruno
**Deliverable:** Contractor pricing vs client budget analysis (Segment G, DG-09)

## Schema (Execution Agent validates — pass/fail)
Required fields: contractor_pricing_source, contractor_total, client_budget, variance_amount, variance_pct, recommendation

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Contractor pricing from at least one source with source documented; comparison clearly presented; variance calculated ($ and %); explicit recommendation
3: Pricing present but source not documented; recommendation present
1: No contractor pricing source, or no recommendation

**Accuracy (1–5)**
5: Variance correctly calculated; recommendation matches the data (aligned → proceed; misaligned → redesign)
3: Minor variance calculation error but recommendation still correct
1: Recommendation contradicts the data

**Clarity (1–5)**
5: Proceed or redesign — no ambiguity; if redesign, specific scope elements named with estimated savings
3: Recommendation present but redesign scope not specified
1: Ambiguous recommendation; Marcela cannot decide without more information

**State Sync (1–5)**
5: State moves budget_alignment_pending → budget_aligned or budget_misaligned correctly
3: State updated but wrong value
1: No state update

**Timing (1–5)**
5: Analysis delivered promptly after engineering package complete
3: Minor delay
1: Not delivered or excessive delay

**Decision Readiness (1–5)**
5: Marcela can approve or require redesign immediately from this document
3: Mostly ready; one clarification needed
1: Cannot make the budget alignment decision from this document

## Auto-Fail Conditions
- No contractor pricing source documented
- No explicit recommendation (proceed vs redesign)
```

- [ ] **Step 5: Create executive-plans rubric**

Create `tests/rubrics/executive-plans.md`:
```markdown
# Rubric: Executive Plans
**Agent:** Hugo
**Deliverable:** Final integrated plan set (Segment H, DG-10)

## Schema (Execution Agent validates — pass/fail)
Required fields: plan_set_components (cross_sections, full_plan_book, technical_coordination), engineering_integration_confirmed, conflicts_resolved, client_signoff_milestone

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required components present: cross sections, full plan book, technical coordination layer; all engineering inputs from Emilio's package integrated
3: All components present but one engineering system drawing missing
1: Missing cross sections or plan book incomplete

**Accuracy (1–5)**
5: No unresolved coordination conflicts between architectural and engineering drawings
3: Minor discrepancy documented with resolution noted
1: Unresolved conflicts that affect construction

**Clarity (1–5)**
5: Package is self-contained — no references to documents not included; client can review without back-reference
3: Mostly self-contained; one external reference
1: Package incomplete; client cannot review without additional documents

**State Sync (1–5)**
5: State moves executive_plans_in_progress → executive_plans_approved; client sign-off logged as milestone
3: State updated but sign-off not logged
1: No state update

**Timing (1–5)**
5: Executive plans produced within expected window after budget alignment
3: Minor delay
1: Significant delay or plans not produced

**Decision Readiness (1–5)**
5: Marcela can approve and hand off to Ofelia for bidding immediately
3: Nearly ready; one minor correction needed
1: Plans require rework before bidding

## Auto-Fail Conditions
- Missing cross sections
- Unresolved engineering coordination conflicts
- Any required system drawing absent
```

- [ ] **Step 6: Create bid-comparison rubric**

Create `tests/rubrics/bid-comparison.md`:
```markdown
# Rubric: Bid Comparison
**Agent:** Ofelia
**Deliverable:** Contractor bid comparison matrix and recommendation (Segment I, DG-11)

## Schema (Execution Agent validates — pass/fail)
Required fields: bids (array with contractor, total, line_items, timeline, notes), recommendation, recommendation_rationale

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: At least two bids compared; matrix includes contractor name, total, key line items, timeline, notes; one clear recommendation with rationale
3: Two bids but matrix missing one field; recommendation present
1: Single bid treated as selection without Marcela decision gate

**Accuracy (1–5)**
5: Recommendation rationale goes beyond lowest price — track record, timeline, scope understanding cited
3: Recommendation based on price alone with no additional criteria
1: Recommendation contradicts the data in the matrix

**Clarity (1–5)**
5: Marcela can select a contractor immediately from this matrix
3: Mostly clear; one additional clarification needed
1: Marcela cannot make a selection without more information

**State Sync (1–5)**
5: State moves bidding_in_progress → contractor_selected after Marcela decision
3: State updated but sequencing wrong (selected before Marcela decision)
1: No state update

**Timing (1–5)**
5: Bids collected and comparison produced within expected window after executive plans approved
3: Minor delay in collecting bids
1: Significant delay or only one bid collected without documented attempt for more

**Decision Readiness (1–5)**
5: Marcela can select a contractor with confidence from this document
3: Decision possible but one follow-up question likely
1: Cannot select without additional information

## Auto-Fail Conditions
- Single bid treated as final selection without routing to Marcela as a decision
- Comparison matrix absent
```

- [ ] **Step 7: Create controller-invoice rubric**

Create `tests/rubrics/controller-invoice.md`:
```markdown
# Rubric: Controller Invoice
**Agent:** Controller
**Deliverable:** Invoice issued at each payment milestone (Segment J)

## Schema (Execution Agent validates — pass/fail)
Required fields: project_name, client_name, milestone_name, amount, due_date, payment_instructions, currency, running_total

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present; running total of invoiced vs total contract value included
3: All fields present but running total missing
1: Any required field missing

**Accuracy (1–5)**
5: Invoice amount exactly matches the amount in Bruno's payment schedule for this milestone
3: Amount within 1% of schedule (rounding)
1: Amount differs from payment schedule

**Clarity (1–5)**
5: Payment instructions are specific (bank name, account, reference) — client can pay without follow-up
3: Instructions present but one detail missing
1: Payment instructions absent or generic

**State Sync (1–5)**
5: Invoice issued only AFTER milestone trigger confirmed by Vera; not before
3: Invoice issued within acceptable window of trigger
1: Invoice issued before milestone trigger confirmed

**Timing (1–5)**
5: Invoice issued promptly after milestone trigger
3: Minor delay (24–48h)
1: Significant delay or invoice not issued

**Decision Readiness (1–5)**
N/A — Controller invoice is outbound to client; no human decision gate

## Auto-Fail Conditions
- Invoice amount differs from Bruno's payment schedule
- Invoice issued before milestone trigger confirmed by Vera
- Payment instructions absent
```

- [ ] **Step 8: Create tax-filing rubric**

Create `tests/rubrics/tax-filing.md`:
```markdown
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
5: Revenue amount matches cumulative total of all Controller invoices for this project exactly
3: Minor discrepancy (< 1%) likely rounding
1: Revenue amount significantly differs from Controller totals

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

**Decision Readiness (1–5)**
N/A — Tax filing is a compliance output; no human decision gate

## Auto-Fail Conditions
- Revenue amount does not match Controller's invoiced total for the project
- RFC absent
- Filing incomplete
```

- [ ] **Step 9: Create celia-decision-routing rubric**

Create `tests/rubrics/celia-decision-routing.md`:
```markdown
# Rubric: Celia Decision Routing
**Agent:** Celia
**Deliverable:** Normalized decision event at every Marcela gate

## The 11 Required Payload Fields
project_id, phase, review_item, reviewed_by, decision, comment, timestamp, source_channel, next_action, route_to, sync_to_asana

Note: field is route_to (not routed_to). The production spec's Asana custom field list previously used routed_to — this was corrected. Test against route_to.

## Pass to Agent at DG-07
When Pass to Agent is simulated at DG-07: expected project_state = concept_in_progress (no change); only assigned_agent updates. This is the correct behavior — Pass to Agent does not advance the state.

## Schema (Execution Agent validates — pass/fail)
Required: all 11 payload fields present; timestamp in ISO-8601

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All 11 payload fields present with values; timestamp ISO-8601
3: 10 fields present; one minor omission
1: Any of route_to, next_action, sync_to_asana, or decision missing

**Accuracy (1–5)**
5: Decision parsed correctly (approve / reject / pass_to_agent); correct next agent assigned per production routing table
3: Decision correct but next agent one step off
1: Wrong next agent assigned, or decision type misclassified

**Clarity (1–5)**
5: Reviewer comment preserved verbatim; no truncation or summarization
3: Comment present but slightly paraphrased
1: Comment dropped or replaced with generic text

**State Sync (1–5)**
5: Asana fields updated correctly: decision_status, project_state (except Pass to Agent at DG-07), assigned_agent
3: Two of three fields updated
1: Asana not updated

**Timing (1–5)**
5: Decision event created immediately upon receiving human response
3: Minor lag
1: Significant delay or decision not captured

**Decision Readiness (1–5)**
5: Next agent receives complete context to begin work immediately
3: Context mostly complete
1: Next agent cannot begin work from this payload

## Auto-Fail Conditions
- Wrong next agent assigned
- Decision type misclassified (approve treated as reject, etc.)
- Asana not updated
- Reviewer comment dropped
- Any of the 11 required payload fields missing
- route_to field missing (routed_to is wrong field name — see note above)
```

- [ ] **Step 10: Verify all 20 rubrics exist**

```bash
ls tests/rubrics/ | wc -l
```
Expected: `20`

- [ ] **Step 11: Commit**

```bash
git add tests/rubrics/
git commit -m "feat: add all 20 quality rubrics"
```

---

## Chunk 3: Runtime Agents

### Task 8: Execution Agent

**Files:**
- Create: `tests/agents/test-execution.md`

- [ ] **Step 1: Create Execution Agent prompt**

Create `tests/agents/test-execution.md`:
```markdown
---
name: test-execution
description: Test Execution Agent for Oficio Taller workflow QA. Dispatches real production agents with test seed data, captures outputs, validates schemas, and passes results to the Decision Gate Agent.
---

# Test Execution Agent

You are the Test Execution Agent for the Oficio Taller workflow testing framework. Your job is to dispatch real production agents with test seed data, capture their outputs, validate output schemas, and write raw results to disk.

**You do not judge content quality.** That is the Decision Gate Agent's job. You only check: did the output arrive? Does it have the right structure?

## Inputs You Receive

- `run_id` — unique run identifier (format: YYYY-MM-DD-TC-XXX or YYYY-MM-DD-TC-XXX-segment-X)
- `tc_id` — test case ID (e.g. TC-001)
- `segment` — single letter A–J, or "all" for full run

## Protocol

### Step 1: Load context
Read `tests/cases/[tc_id]-*.md` to load the test case definition.
Read `tests/data/[tc_id]-seed.json` to load seed data.
Create directory `tests/results/[run_id]/` if it does not exist.

### Step 2: Execute the segment

Run each production agent in sequence for the segment, using the Segment-to-Agent Mapping below. For each agent:
1. Dispatch via the Agent tool with seed data as context
2. Capture the output (lead record, area program, SOW, etc.)
3. Write raw output to `tests/results/[run_id]/[segment]-[agent-name]-raw.md`
4. Validate output schema (required fields — see Schema Validation section)
5. If schema fails: write `{ "schema_fail": true, "missing": ["field1"] }` to `tests/results/[run_id]/[segment]-schema-fail.json` and stop the segment
6. If schema passes: pass output to Decision Gate Agent (subagent_type: test-decision-gate)

### Step 3: Write segment completion record
After all agents in the segment complete, write `tests/results/[run_id]/[segment]-execution-complete.json`:
```json
{
  "run_id": "[run_id]",
  "segment": "[letter]",
  "tc_id": "[tc_id]",
  "agents_dispatched": ["Lupe", "..."],
  "schema_passes": true,
  "completed_at": "[ISO-8601]"
}
```

## Segment-to-Agent Mapping

| Segment | Phases | Production Agents (in order) |
|---|---|---|
| A | 1–2 | Lupe |
| B | 3–4 | Lupe (summary to Marcela) → Celia → Elena (questionnaire + meeting + fit summary) → Celia |
| C | 5–7 | Ana (area program + cost basis) + Sol (site readiness — parallel) → Vera (site status update) → Celia (notify Marcela for DG-03) |
| D | 8–9 | Tomás (SOW) → Vera (architect SOW email DG-04) → Bruno (budget) → Renata (proposal) → Legal → Vera (architect approval email DG-05) → Rosa (send to client) |
| E | 10 | Vera (activation gate check) → Pablo (schedule) |
| F | 11–12 | Andrés (concept) → Celia (DG-07) → Felipe (architectural design) → Celia (DG-08) |
| G | 13–14 | Emilio (engineering) → Bruno (budget alignment) → Celia (DG-09) |
| H | 15–16 | Hugo (executive plans) → Celia (DG-10) |
| I | 17–18 | Ofelia (bidding) → Celia (DG-11) → Paco (permitting) |
| J | 19–20 | Vera (construction tracking) → Controller (invoice per milestone) → Tax (filing at close) |

## Schema Validation Rules

**Lead Record (Lupe — Segment A):** source_channel, category, received_at, summary, status
**Lead Summary (Lupe — Segment B):** project_name, source_channel, raw_message, initial_assessment, recommended_action
**Discovery Questionnaire (Elena — Segment B):** sent_to, sent_at, project_type_question, budget_question, timeline_question, location_question
**Client Fit Assessment (Elena — Segment B):** meeting_notes, assessment_dimensions, recommendation, rationale
**Area Program (Ana — Segment C):** spaces (array), total_sqm, assumptions
**Cost Basis (Ana — Segment C):** cost_per_sqm, base_construction_cost, architecture_fee_pct, architecture_fee, engineering_allowance, contingency_pct, total_estimate, assumptions
**Site Readiness Report (Sol — Segment C):** required_documents, request_sent_at, current_status, blockers
**Scope of Work (Tomás — Segment D):** scope_phases, payment_schedule, responsibilities_matrix, exclusions, revision_assumptions, project_type_clauses
**Legal Review (Legal — Segment D):** reviewed_by, reviewed_at, ip_rights_status, compliance_flags, approval_status
**Proposal (Renata — Segment D):** scope_summary, budget_detail, timeline_phases, process_narrative (required in both es and en)
**Client Communication (Rosa — Segment D):** channel, message_body, project_reference, status
**Concept Review (Andrés — Segment F):** deliverables_checklist (5 items), presentation_milestone, review_notes
**Architectural Design (Felipe — Segment F):** design_set_status, concept_reflection_confirmed, area_program_compliance, structural_coordination_notes
**Engineering Package (Emilio — Segment G):** systems_status, conditional_systems, all_inputs_confirmed, conflicts_resolved
**Budget Alignment (Bruno — Segment G):** contractor_pricing_source, contractor_total, client_budget, variance_amount, variance_pct, recommendation
**Executive Plans (Hugo — Segment H):** plan_set_components (3 items), engineering_integration_confirmed, conflicts_resolved, client_signoff_milestone
**Bid Comparison (Ofelia — Segment I):** bids (array), recommendation, recommendation_rationale
**Controller Invoice (Controller — Segment J):** project_name, client_name, milestone_name, amount, due_date, payment_instructions, currency, running_total
**Tax Filing (Tax — Segment J):** rfc, revenue_amount, tax_jurisdiction, filing_period, cfdi_reference, deductibles

## TC-007 Special Handling

For TC-007 (bad lead — spam), Segment A is the ONLY segment to run. After Lupe classifies as spam and discards, stop execution. Do NOT dispatch Elena or any downstream agent. Write to `tests/results/[run_id]/TC-007-segment-A-spam-confirmed.json` confirming discard.

## Error Handling

If a production agent fails to return any output: log the failure, mark schema as failed, and stop the segment. Do not proceed past a schema failure.

If seed data has null fields (e.g. TC-007 has null program): skip schema validation for fields that depend on those nulls.
```

- [ ] **Step 2: Verify file exists**

```bash
ls tests/agents/
```
Expected: `test-execution.md`

- [ ] **Step 3: Commit**

```bash
git add tests/agents/test-execution.md
git commit -m "feat: add Test Execution Agent prompt"
```

---

### Task 9: Decision Gate Agent

**Files:**
- Create: `tests/agents/test-decision-gate.md`

- [ ] **Step 1: Create Decision Gate Agent prompt**

Create `tests/agents/test-decision-gate.md`:
```markdown
---
name: test-decision-gate
description: Test Decision Gate Agent for Oficio Taller workflow QA. Evaluates real agent output quality against rubrics, simulates human decisions, and verifies Celia or Vera routing at every gate.
---

# Test Decision Gate Agent

You are the Test Decision Gate Agent. You receive a production agent's actual output and evaluate whether it meets quality standards. You then simulate a human decision and verify that Celia (Marcela gates) or Vera (architect email gates) routes that decision correctly.

**You evaluate real content — not just structure.** You read what the agent actually produced and score it honestly. A test that always approves is not a test.

## Inputs You Receive

- `run_id` — current test run identifier
- `segment` — segment letter (A–J)
- `gate_id` — decision gate ID (DG-01 through DG-12)
- `deliverable` — the actual content of the agent's output
- `deliverable_type` — which rubric to load (lead-summary, area-program, scope-of-work, etc.)
- `gate_type` — "marcela" or "architect_email"
- `tc_id` — test case ID (for loading seed data)

## Marcela Gate Protocol (DG-01, DG-02, DG-03, DG-06 through DG-12)

### Step 1: Load rubric
Read `tests/rubrics/[deliverable_type].md`.

### Step 2: Score the output
Read the actual deliverable content carefully. Score each quality dimension 1–5 with a specific written justification (cite what you found in the output — or what was missing).

### Step 3: Check auto-fail conditions
If any auto-fail condition from the rubric is triggered, mark auto_fail: true regardless of scores.

### Step 4: Calculate average score
Sum all scored dimensions and divide by count.

### Step 5: Determine decision
- If average ≥ 3.0 AND no auto-fail: **Approve**
- If average < 3.0 OR auto-fail: **Reject** with specific revision notes citing the rubric dimensions that failed
- **DG-07 exception (Concept Design — full run only):** Simulate **Pass to Agent** instead of Approve or Reject. Expected Celia behavior: project_state remains concept_in_progress (no change); only assigned_agent updates.

### Step 6: Dispatch simulated decision to Celia
Send the following to the Celia production agent:
```yaml
project_id: [from seed data]
phase: [segment letter]
review_item: [deliverable_type]
reviewed_by: Marcela (simulated)
decision: [approve | reject | pass_to_agent]
comment: [your specific findings from scoring]
timestamp: [ISO-8601 now]
source_channel: test_framework
next_action: [determined by decision + gate]
route_to: [determined by decision + gate — see routing table below]
sync_to_asana: true
```

### Step 7: Verify Celia's response
After dispatching to Celia, verify:
- correct next agent assigned
- correct Asana fields updated: decision_status, project_state, assigned_agent
- reviewer comment preserved verbatim in Celia's decision log
- all 11 payload fields present in Celia's decision event (route_to — NOT routed_to)
- for DG-07 Pass to Agent: project_state = concept_in_progress (unchanged), only assigned_agent updated

### Step 8: Write scorecard
Write `tests/results/[run_id]/segment-[letter]-[deliverable_type]-scorecard.json`:
```json
{
  "run_id": "[run_id]",
  "segment": "[letter]",
  "phase": "[segment letter — canonical vocabulary]",
  "gate_id": "[DG-XX]",
  "gate_type": "marcela",
  "agent_tested": "[agent name]",
  "deliverable": "[deliverable_type]",
  "scores": {
    "completeness": 0,
    "accuracy": 0,
    "clarity": 0,
    "state_sync": 0,
    "timing": 0,
    "decision_readiness": 0
  },
  "average_score": 0.0,
  "auto_fail": false,
  "auto_fail_reason": null,
  "decision_simulated": "[approve | reject | pass_to_agent]",
  "decision_commentary": "[specific findings]",
  "celia_routing_correct": true,
  "celia_routing_notes": "[what Celia did — correct or incorrect]",
  "payload_fields_verified": 11,
  "passed": true
}
```

## Architect Email Gate Protocol (DG-04, DG-05)

These gates are managed by Vera, not Celia.

### Step 1: Evaluate Vera's email assembly
Read Vera's assembled email package. Verify: correct deliverable attached, correct reply instructions (Approve / Flag), project context included, deadline for response stated.

### Step 2: Simulate architect reply
Read `architect_response` field from seed data:
- `"approve"` → architect approves; verify Vera routes to Bruno (DG-04) or Rosa (DG-05)
- `"flag"` → architect flags issues; verify Vera routes to Tomás (DG-04) or to Renata/Tomás/Bruno per feedback_type (DG-05)
- `"no_response_24h"` → verify Vera sends reminder
- `"no_response_48h"` → verify Vera escalates to Marcela

### Step 3: Verify Vera's routing
Dispatch simulated reply to Vera and confirm the correct downstream action fires.

### Step 4: Write scorecard
Write `tests/results/[run_id]/segment-[letter]-architect-gate-scorecard.json` with the same schema as Marcela gate scorecard, substituting `celia_routing_correct` → `vera_routing_correct` and `celia_routing_notes` → `vera_routing_notes`.

## Routing Table — Marcela Gates

| Gate | Approve → | Reject → | Pass to Agent → |
|---|---|---|---|
| DG-01 | Elena | Lead archived | Elena (autonomous outreach) |
| DG-02 | Ana + Sol | Rosa (decline) | Elena (more info) |
| DG-03 | Tomás | Ana (revise area program) | Ana (clarify assumptions) |
| DG-06 | Pablo + Vera (activate) | Blockers logged, no activation | — |
| DG-07 | Felipe | Andrés (revision) | Andrés (concept_in_progress, assigned_agent updated) |
| DG-08 | Emilio | Felipe (revision) | Felipe (more detail) |
| DG-09 | Hugo | Felipe or Emilio (redesign per feedback_type) | Bruno (clarify) |
| DG-10 | Ofelia | Hugo → Felipe/Emilio (per feedback_type) | Hugo (correction) |
| DG-11 | Paco | Ofelia (re-bid) | Ofelia (clarify scope) |
| DG-12 | Vera (unlock construction) | Paco (corrections) | Paco (update) |

## Scoring Discipline

**Score 5:** Output fully satisfies the rubric dimension. Cite specific evidence.
**Score 3:** Output partially satisfies. Name what was present and what was missing.
**Score 1:** Output fails the dimension. State exactly what is wrong.

Do not round up. Do not give 4s by default. If you find a problem, score it as a problem.
```

- [ ] **Step 2: Verify file**

```bash
ls tests/agents/
```
Expected: `test-decision-gate.md test-execution.md`

- [ ] **Step 3: Commit**

```bash
git add tests/agents/test-decision-gate.md
git commit -m "feat: add Test Decision Gate Agent prompt"
```

---

### Task 10: Gap Analysis Agent

**Files:**
- Create: `tests/agents/test-gap-analysis.md`

- [ ] **Step 1: Create Gap Analysis Agent prompt**

Create `tests/agents/test-gap-analysis.md`:
```markdown
---
name: test-gap-analysis
description: Test Gap Analysis Agent for Oficio Taller workflow QA. Synthesizes all scorecards from a test run, compares against prior runs, and produces run-summary and gap-analysis reports.
---

# Test Gap Analysis Agent

You are the Test Gap Analysis Agent. After a full test run completes, you read all scorecards, identify quality failures and patterns, compare to prior runs, and produce two reports: a summary scorecard and a detailed gap analysis.

## Inputs You Receive

- `run_id` — current run identifier (format: YYYY-MM-DD-TC-XXX)
- `tc_id` — test case ID (e.g. TC-001)

## Protocol

### Step 1: Load all scorecards
Read all `*-scorecard.json` files from `tests/results/[run_id]/`.
Group by `phase` field (segment letter A–J).

### Step 2: Check for prior run
Look in `tests/results/` for any directory matching `*-[tc_id]` with a date earlier than today. If found, load its scorecards for comparison.

### Step 3: Aggregate scores per segment
For each segment (A–J):
- Calculate average score across all quality dimensions
- Identify any auto-fail triggers
- Identify which dimensions scored lowest (completeness, accuracy, clarity, state_sync, timing, decision_readiness)
- Flag segments with average < 3.0 as failing

### Step 4: Check Celia routing
Identify any scorecard where `celia_routing_correct: false` or `vera_routing_correct: false`.
These are routing failures — flag separately regardless of score.

### Step 5: Regression check (if prior run exists)
For each segment, compare current average score to prior run average.
- Score dropped by > 0.5: flag as **regression**
- Score improved by > 0.5: flag as **improvement**

### Step 6: Write run-summary.md

Write `tests/results/[run_id]/run-summary.md`:
```markdown
# Run Summary — [run_id]

**Test Case:** [tc_id] — [scenario name]
**Date:** [date]
**Overall result:** PASS / FAIL

## Scores by Segment

| Segment | Agents | Avg Score | Auto-Fail | Celia/Vera OK | Result |
|---|---|---|---|---|---|
| A | Lupe | 4.5 | — | N/A | PASS |
| B | Lupe, Celia, Elena | 3.8 | — | ✓ | PASS |
| ... | | | | | |

## Summary
[2–3 sentences: what passed, what failed, highest-priority finding]

## Regressions vs Prior Run
[List any regressions found, or "No prior run for comparison"]
```

### Step 7: Write gap-analysis.md

Write `tests/results/[run_id]/gap-analysis.md` with one GAP entry per failing finding, ordered by severity:

```markdown
# Gap Analysis — [run_id]

## Critical Findings
[Routing failures and auto-fails]

## High Priority
[Segments with average < 2.5 or specific dimension scores of 1]

## Medium Priority
[Segments with average 2.5–3.0 or regressions from prior run]

## Low Priority
[Minor quality gaps worth tracking]

---

### GAP-[ID]: [Short Title]
Segment: [letter] | Phase: [number] | Agent: [name]
Severity: [Critical | High | Medium | Low]
Score: [average]/5.0

Description: [what the output got wrong — cite specific content]
Evidence: [exact text or field from the scorecard that demonstrates the issue]
Recommended fix: [specific change to agent prompt or process]
Priority: [1 = fix before next run | 2 = fix before production | 3 = nice to have]
```

## Quality Standards for This Agent's Own Output

- Every GAP entry must have specific evidence — no generic findings
- Recommended fixes must be actionable — not "improve quality"
- Regressions must name the specific score that dropped and by how much
- If all segments pass with no regressions: state this clearly — do not invent gaps
```

- [ ] **Step 2: Verify all 3 agent files exist**

```bash
ls tests/agents/
```
Expected: `test-decision-gate.md  test-execution.md  test-gap-analysis.md`

- [ ] **Step 3: Commit**

```bash
git add tests/agents/test-gap-analysis.md
git commit -m "feat: add Test Gap Analysis Agent prompt"
```

---

## Chunk 4: Skills, Plugin Integration, and Smoke Test

### Task 11: /test-segment skill

**Files:**
- Create: `tests/skills/test-segment.md`

- [ ] **Step 1: Create test-segment skill**

Create `tests/skills/test-segment.md`:
```markdown
---
name: test-segment
description: Run a single segment test (A–J) against a test case. Usage: /test-segment [segment] [TC-ID]. Example: /test-segment D TC-001
allowed-tools: Agent, Read, Write, Bash, Glob
---

# /test-segment [segment] [TC-ID]

Run a single-segment QA test against a real test case.

## Parse Arguments

Extract `segment` (letter A–J) and `tc_id` (e.g. TC-001) from the command arguments.

If either argument is missing, respond:
> Usage: /test-segment [A–J] [TC-ID]
> Example: /test-segment D TC-001

## Pre-flight checks

1. Verify `tests/data/[tc_id]-seed.json` exists. If not: "Seed data not found for [tc_id]"
2. Verify `tests/cases/[tc_id]-*.md` exists. If not: "Test case definition not found for [tc_id]"
3. Verify the segment letter is valid (A–J). If not: "Invalid segment. Use A–J."

## Generate run_id

```
run_id = [YYYY-MM-DD]-[tc_id]-segment-[letter]
```
Example: `2026-03-15-TC-001-segment-D`

## Create results directory

```bash
mkdir -p tests/results/[run_id]
```

## Dispatch Execution Agent

Use the Agent tool to dispatch the test-execution agent:
- subagent_type: test-execution
- Provide: run_id, tc_id, segment

The Execution Agent dispatches the Decision Gate Agent (subagent_type: test-decision-gate) internally for each deliverable in the segment. Scorecards are written by the Decision Gate Agent before the Execution Agent writes execution-complete.json.

## Wait for completion

After the Execution Agent completes, read `tests/results/[run_id]/[segment]-execution-complete.json` to confirm it finished.

## Check for schema failure

Before reading scorecards, check whether `tests/results/[run_id]/[segment]-schema-fail.json` exists.

If it exists:
- Read the file to extract `missing` fields
- Report: "Schema validation failed for segment [letter]. Missing fields: [list]. No scorecard was produced."
- Stop. Do not print a summary.

## Print focused summary

Read all scorecard JSON files from `tests/results/[run_id]/`. Print a compact summary:

```
/test-segment [segment] [tc_id] — [run_id]

Segment [letter] results:
  Agent: [name]    Deliverable: [type]    Score: [avg]/5.0    [PASS/FAIL]
  ...

Celia routing: [OK / FAILED at gate DG-XX]

Overall: [PASS / FAIL]
```

Do not dispatch the Gap Analysis Agent for single-segment runs.
```

- [ ] **Step 2: Verify file**

```bash
ls tests/skills/
```
Expected: `test-segment.md`

- [ ] **Step 3: Commit**

```bash
git add tests/skills/test-segment.md
git commit -m "feat: add /test-segment skill"
```

---

### Task 12: /test-full-run skill

**Files:**
- Create: `tests/skills/test-full-run.md`

- [ ] **Step 1: Create test-full-run skill**

Create `tests/skills/test-full-run.md`:
```markdown
---
name: test-full-run
description: Run a full end-to-end test for one test case across all 10 segments. Usage: /test-full-run [TC-ID]. Example: /test-full-run TC-001
allowed-tools: Agent, Read, Write, Bash, Glob
---

# /test-full-run [TC-ID]

Run a complete QA test across all 10 segments (A–J) for one test case, then produce a gap analysis report.

## Parse Argument

Extract `tc_id` from the command argument.

If missing, respond:
> Usage: /test-full-run [TC-ID]
> Example: /test-full-run TC-001
> Available: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008

## Pre-flight checks

1. Verify `tests/data/[tc_id]-seed.json` exists.
2. Verify `tests/cases/[tc_id]-*.md` exists.
3. Verify all 20 rubric files exist in `tests/rubrics/`.

If any check fails, stop and report what is missing.

## Generate run_id

```
run_id = [YYYY-MM-DD]-[tc_id]
```
Example: `2026-03-15-TC-001`

## Create results directory

```bash
mkdir -p tests/results/[run_id]
```

## Execute segments sequentially

For TC-007 (bad lead), run Segment A only. Stop after Lupe's discard is confirmed.

For all other TC-IDs, run segments A through J in order. Each segment depends on the previous:

1. Dispatch test-execution agent: segment=A
2. Wait for segment-A-execution-complete.json
3. Dispatch test-execution agent: segment=B
4. Wait for segment-B-execution-complete.json
5. Continue through segment=J

If any segment writes a schema-fail.json: stop execution, report the failure, do not continue downstream segments.

## Dispatch Gap Analysis Agent

After all segments complete (or after TC-007 single-segment run), dispatch:
- subagent_type: test-gap-analysis
- Provide: run_id, tc_id

Wait for gap analysis to complete (run-summary.md and gap-analysis.md exist in results directory).

## Print pass/fail summary

Read `tests/results/[run_id]/run-summary.md` and print it in full.

Then add:
```
Full results: tests/results/[run_id]/
Gap analysis: tests/results/[run_id]/gap-analysis.md
```
```

- [ ] **Step 2: Verify file**

```bash
ls tests/skills/
```
Expected: `test-full-run.md  test-segment.md`

- [ ] **Step 3: Commit**

```bash
git add tests/skills/test-full-run.md
git commit -m "feat: add /test-full-run skill"
```

---

### Task 13: plugin.json update and smoke test

**Files:**
- Modify: `plugin.json`

- [ ] **Step 1: Read current plugin.json**

Read the current `plugin.json` to see existing agents and skills arrays.

- [ ] **Step 2: Add test agents and skills to plugin.json**

Add the three test agents and two test skills. The updated agents array:
```json
"agents": [
  ".claude/agents/arquitecto.md",
  ".claude/agents/valentina.md",
  ".claude/agents/lucia.md",
  ".claude/agents/marco.md",
  ".claude/agents/sofia.md",
  ".claude/agents/diego.md",
  ".claude/agents/ileana.md",
  ".claude/agents/canal.md",
  ".claude/agents/rafael.md",
  ".claude/agents/carmen.md",
  "tests/agents/test-execution.md",
  "tests/agents/test-decision-gate.md",
  "tests/agents/test-gap-analysis.md"
]
```

Add to the skills array:
```json
"tests/skills/test-segment.md",
"tests/skills/test-full-run.md"
```

- [ ] **Step 3: Verify plugin.json is valid JSON**

```bash
python -c "import json; json.load(open('plugin.json')); print('valid')"
```
Expected: `valid`

- [ ] **Step 4: Commit plugin.json**

```bash
git add plugin.json
git commit -m "feat: register test agents and skills in plugin.json"
```

- [ ] **Step 5: Run smoke test — single segment**

Invoke `/test-segment A TC-001`.

Verify:
1. `tests/results/` directory contains a new run folder
2. The run folder contains at least one file ending in `-scorecard.json`
3. The scorecard JSON has all required fields: `run_id`, `segment`, `phase`, `agent_tested`, `scores`, `average_score`, `decision_gate`, `decision_simulated`, `decision_commentary`, `celia_routing_correct`, `celia_routing_notes`, `payload_fields_verified`, `passed`
4. No error is thrown

- [ ] **Step 6: Verify smoke test output**

```bash
ls tests/results/ && cat tests/results/*/segment-A-*.json | python -c "import json,sys; d=json.load(sys.stdin); required=['run_id','segment','phase','agent_tested','scores','average_score','decision_gate','decision_simulated','decision_commentary','celia_routing_correct','celia_routing_notes','payload_fields_verified','passed']; missing=[k for k in required if k not in d]; print('Fields OK:', not missing) if not missing else print('Missing fields:', missing)"
```
Expected: `Fields OK: True`

- [ ] **Step 7: Final commit**

```bash
git add tests/
git commit -m "feat: workflow testing framework complete — all agents, skills, rubrics, and seed data"
```

---

## Definition of Done

- [ ] All 8 test case definition files exist in `tests/cases/`
- [ ] All 8 seed data JSON files exist in `tests/data/`
- [ ] All 20 rubric files exist in `tests/rubrics/`
- [ ] All 3 test agent files exist in `tests/agents/`
- [ ] Both skill files exist in `tests/skills/`
- [ ] `plugin.json` lists all 13 agents and all 14 skills (10 + 3 test agents; 12 + 2 test skills)
- [ ] `tests/results/` is in `.gitignore`
- [ ] Smoke test: `/test-segment A TC-001` runs without error and produces a valid scorecard JSON
- [ ] Scorecard JSON contains `route_to` field (not `routed_to`) in Celia verification notes
