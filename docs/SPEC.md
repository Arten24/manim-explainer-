# QUONITRON Manim Master Library — Project Specification

Status: Foundation (Part 0)  
Library version: 0.1.0  
Catalog version: 1.0.0  
Date: 2026-10-15

## Purpose

This repository is a reusable animation system for producing consistent
educational videos with Manim Community Edition. It is designed so that
human authors and AI coding agents can:

1. Read an educational script and divide it into logical scenes.
2. Identify the visual concepts needed for each scene.
3. Search the master animation catalog.
4. Reuse tested components and scene templates.
5. Configure existing components instead of rewriting them.
6. Compose scenes with consistent typography, color, spacing, and motion.
7. Generate natural English subtitles that can be read without audio.
8. Export subtitle files and scene timing metadata for later voiceover.
9. Render and validate the video.
10. Register newly created, tested components for future reuse.

Not every possible animation can be prebuilt. The system covers broad
categories and is expected to grow part by part.

## Non-goals (this milestone)

- Implementing the full twenty-part visual library in one pass.
- Generating or requiring recorded voiceover.
- Claiming render success in environments without Cairo, Pango, and FFmpeg.
- Marking untested visual components as tested.

## Architecture

| Area | Location | Role |
| --- | --- | --- |
| Design system | `quonitron/design/` | Colors, type, spacing, motion, themes |
| Components | `quonitron/components/` | Reusable animation building blocks |
| Catalog | `quonitron/catalog/` | JSON inventory + JSON Schema + search |
| Scenes | `quonitron/scenes/` | Scene specs and later Manim templates |
| Subtitles | `quonitron/subtitles/` | Cue model, SRT, WebVTT, estimated timing |
| Planning | `quonitron/planning/` | Script → scene split and search hints |
| Render | `quonitron/render/` | Preview vs production render settings |
| QA | `quonitron/qa/` | Schema, import, syntax, catalog integrity |
| Tests | `tests/` | Unit tests that do not require a GPU/Cairo |
| Docs | `docs/` | Specification, plan, agent guide |

JSON is the searchable catalog. Python modules are the implementations.
The catalog must not become a dump of thousands of lines of Python.

## Visual identity

Default theme: **quonitron_dark**.

- Background `#0B0F19`, surface `#141A2A`
- Primary text `#F5F7FA`, secondary `#A9B4C7`
- Accent `#4F8CFF`, secondary accent `#7C5CFF`
- Success / warning / danger for semantic highlights only
- Premium dark editorial look: clean type, restrained accents, readable
  diagrams, smooth motion
- Avoid cheap glow spam, clutter, and random style changes

Themes are configurable without changing component APIs.

## Subtitle policy

Workflow is **subtitle-first**, not voiceover-first.

- Subtitles are complete English sentences.
- Timing is estimated from configurable words-per-minute.
- Estimated timings are **not** synchronized to a real speaker.
- SRT and WebVTT export are supported.
- Subtitle generation is independent of animation rendering.

## Catalog contract

Every component has:

- Stable dotted `id` (example: `math.equation.transform`)
- `name`, `category`, `tags`, `aliases`, `description`
- `module` and `class_name`
- `parameters`, `defaults`, `dependencies`, `compatibility`
- `test_status`: `untested` | `syntax_ok` | `unit_ok` | `render_ok` | `tested`
- `example`, `limitations`, `related_ids`, `part`

Rules:

- Never mark untested code as `tested`.
- Never silently break existing component APIs.
- Reject duplicate IDs and broken related-id references.
- Catalog Python modules and class names must import.

## Agent reuse order

1. Search the catalog.
2. Read API, dependencies, examples, limitations.
3. Reuse with parameters.
4. Compose with other components.
5. Create a new component only if needed.
6. Test it.
7. Register it in the catalog with docs and a regression test.

## Twenty-part plan

See `docs/development-plan.md`. Implement one part at a time. Keep the
default branch usable.

## Environment

- Python 3.10+
- Manim Community Edition `>=0.18.1,<1.0` (verified against 0.22.0 metadata)
- `jsonschema` for catalog validation
- Cairo, Pango, and FFmpeg are required for actual video renders

This cloud workspace could not install system Cairo/Pango/FFmpeg packages
during foundation setup. Unit tests and catalog QA therefore run without
Manim rendering. A small preview render is required before claiming any
visual component as `render_ok` or `tested`.
