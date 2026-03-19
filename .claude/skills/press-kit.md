# Press Kit Builder

Build a personalized press kit for architecture/design media publications.

## Usage

```
/press-kit <project-name> [publication]
```

- `project-name`: Name of the project to build the press kit for
- `publication` (optional): Target publication. If omitted, builds kits for ALL publications.

Valid publication names: `archdaily`, `yellowtrace`, `the-local-project`, `architecture-hunter`, `ad-mexico`, `archdigest`, `yinjispace`

## Instructions

When invoked, follow these steps:

### 1. Gather Project Information

Ask the user for the following project details (skip any already provided):

- **Project name** and location
- **Architect / Studio** name
- **Year of completion**
- **Project area** (m²)
- **Photography credits** (photographer name)
- **Project description** (2-3 paragraphs about the project concept, context, and design intent)
- **Key materials** used
- **Structural system**
- **Collaborators** (engineers, landscape, interior design, lighting, etc.)
- **High-resolution images available** (number and types: exterior, interior, detail, plans, sections, construction)

### 2. Load Publication Profile

Read the target publication profile from `press-kit/profiles/<publication>.md`. Each profile contains:
- Editorial focus and voice
- Visual requirements
- Content format preferences
- Submission guidelines
- What to emphasize vs. de-emphasize

### 3. Generate the Press Kit

For each target publication, read the template at `press-kit/templates/press-kit-template.md` and generate a personalized press kit by:

1. **Adapting the narrative angle** based on the publication's editorial focus
2. **Selecting and ordering images** based on their visual preferences
3. **Adjusting tone and language** to match the publication's voice
4. **Structuring content** per the publication's preferred format
5. **Highlighting the right details** (technical vs. sensorial vs. process-driven)

Write the generated press kit to `press-kit/output/<project-name>/<publication>.md`.

### 4. Generate Summary

After building all kits, output a summary table showing:
- Publication name
- Narrative angle used
- Key emphasis points
- Recommended lead image
- Output file path

## Key Principles (from Oficio Taller's communication strategy)

- The architecture sells through **sensibility + experience + intention**, not spectacle
- The right media are not the biggest ones — they're the ones that **understand silence, context, and the human**
- Think in **different angles of the same project**: each publication gets a distinct narrative
- Never send the same press kit to everyone
