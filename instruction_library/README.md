# Instruction Library

This directory is the canonical source of truth for ALL instructions in this room.
It is the **authoring surface** — `instructions/` is the deploy surface (materialized from this library).

## Pipeline

```
instruction_library/corpus/    ← Author here (full superset)
         │
         │ activation/*.active.yml (allowlist of IDs to deploy)
         │ activation/limits.yml (capacity budget)
         ↓
scripts/materialize.py         ← Runs materialization
         │
         ↓
instructions/                  ← Deploy surface (active subset)
         │
         │ scripts/push_folder_to_room.py
         ↓
Genie Room API                 ← Live room
```

## Key Rule

**NEVER add files directly to `instructions/`.**
Always author in `instruction_library/corpus/<type>/` first.
Then activate via `instruction_library/activation/<type>.active.yml`.
Then run `python scripts/materialize.py`.

## Directory Structure

```
instruction_library/
├── README.md                       ← This file
├── corpus/                         ← Full superset of all snippets
│   ├── filters/                    ← All possible filter snippets
│   ├── measures/                   ← All possible measure snippets
│   ├── dimensions/                 ← Dimension helper snippets
│   └── example_sql/               ← All possible example SQL entries
├── activation/                     ← Allowlist manifests + capacity config
│   ├── filters.active.yml
│   ├── measures.active.yml
│   ├── dimensions.active.yml
│   ├── example_sql.active.yml
│   └── limits.yml
├── reduction/                      ← Merge/isolation decision records
│   └── README.md
└── isolated/                       ← Deactivated ID manifests
    └── deactivated.yml
```
