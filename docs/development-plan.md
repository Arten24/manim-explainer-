# Twenty-part development plan

Implement **one part at a time**. Do not declare a part complete without
working code, tests, and an honest limitations note.

| Part | Focus | Status |
| --- | --- | --- |
| 0 | Repository, specification, catalog schema, design tokens, QA | **done (this commit)** |
| 1 | Foundation and design system (Manim-facing theme application) | not started |
| 2 | Basic motion library | not started |
| 3 | Transitions and scene changes | not started |
| 4 | Text and typography | not started |
| 5 | Subtitle system (full planner + metadata sidecar) | not started |
| 6 | Shapes and 2D graphics | not started |
| 7 | Charts and data visualization | not started |
| 8 | Mathematics and geometry | not started |
| 9 | Physics and engineering | not started |
| 10 | Programming and code animation | not started |
| 11 | Data structures and algorithms | not started |
| 12 | AI and machine learning visuals | not started |
| 13 | Diagrams and system architecture | not started |
| 14 | Camera and composition | not started |
| 15 | Advanced motion and effects | not started |
| 16 | 3D and spatial visuals | not started |
| 17 | Sound-ready timing and voiceover preparation | not started |
| 18 | Full video templates | not started |
| 19 | Automated QA and render testing | not started |
| 20 | Agent integration, catalog expansion, final integration | not started |

Part 0 ships a working subtitle **export** and a script splitter so later
parts have something real to compose against. Part 5 still owns the full
narration planner, reading-speed tooling, and voiceover metadata files.

Part 1 owns applying the design system inside Manim scenes (background,
safe areas, title styles) once a render environment is available.
