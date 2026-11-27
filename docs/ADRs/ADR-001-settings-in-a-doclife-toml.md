---
type: adr
project: doclife
tags: [settings, configuration, toml]
date: 2026-11-27
date_created: 2026-11-27
date_modified: 2026-11-27
status: Proposed
---

# ADR-001: Each Repo's Rules in a `doclife.toml`

## Status
Proposed

## Context

doclife is extracted from a checker that ran in one repo, with that repo's
rules as constants in the code: which folders hold documents, which types
each folder allows, which types must be reviewed and how often, and where
the ADRs are. To check a second repo, those rules have to come from the
repo being checked ([#2](https://github.com/ndomako10/doclife/issues/2)).

Reading the original's constants sorts them three ways:

| In the original | Here |
|---|---|
| The documents folder, a templates folder that's skipped, `README.md` indexes that are skipped | Settings: which files are checked |
| Each folder's allowed types, and whether the folder or the document sets its sensitivity label | Settings: places |
| The label's field name and values (one repo calls it `visibility`, another wants `classification` with different levels) | Settings |
| Types that need `last_reviewed`, and the review period (365 days) | Settings |
| A field only one type needs (ADRs need a decision `date`); a file name pattern only one type has | Settings, by type |
| The ADR folder, index and statuses | Settings |
| Required sections on wiki pages, links between wiki topics, a generated A-Z index, aliases, a list of pages being migrated | Stays in the original repo: rules about one repo's content |
| The date format, the frontmatter syntax, how the stamp hook writes `date_modified`, the check that it isn't older than the last commit | Fixed in doclife: these are what doclife is |

The repos it's meant for include ones that aren't Python projects, such as
note stores. doclife has no runtime dependencies, and Python 3.11 reads TOML
with `tomllib` from the standard library.

## Decision

Nothing is settled yet. Suggested:

- **A `doclife.toml` at the repo root holds the rules.** It's found by
  walking up from the current folder, as git finds `.git`.
- **No file is an error, not a set of defaults.** A repo that hasn't said
  what its rules are gets a message saying so, not a check against rules it
  never chose.
- **Unknown keys are an error.** A misspelled key would otherwise switch a
  check off without anyone noticing.
- **Places are an ordered list, and the first match wins.** The original
  matched the longest folder prefix; an ordered list does the same when
  it's written most specific first, and also covers files at the repo root.

An example of the shape, not yet a format:

```toml
include = ["**/*.md"]
exclude = ["**/README.md", "templates/**", "website/**"]
review_after_days = 365

[label]
field = "classification"
values = ["public", "internal"]   # lowest first

[[places]]
path = "docs/ADRs/**"
types = ["adr"]                   # no label: the document sets it

[[places]]
path = "*.md"
types = ["policy", "plan", "reference"]
label = "internal"

[types.policy]
review = true

[types.adr]
required = ["date"]

[adr]
path = "docs/ADRs/"
index = "docs/ADRs/README.md"
statuses = ["Proposed", "Provisional", "Accepted", "Rejected", "Deprecated", "Superseded by"]
```

## Open questions

- **Link checks.** The original also fails a link to a missing page, and a
  link from a page to one with a higher label. Dead links are what link
  checkers such as lychee already do; the label rule isn't. Settled by
  deciding whether doclife takes the label rule only.
- **Paths cited outside the docs.** The original checks that every docs
  path named in code or config still exists. Useful, but not about
  frontmatter. Settled with the link question.
- **ADR numbering.** The original expects three digits (`ADR-001`). Some
  repos use four, or no prefix. Settled when a repo with another pattern
  adopts doclife; until then it's fixed at three.
- **Glob rules.** `**` and a pattern with no slash need defined behaviour
  without a dependency; Python 3.11's `fnmatch` treats `*` as crossing
  folders. Settled by the tests for places.

## Alternatives considered

- **`[tool.doclife]` in `pyproject.toml`.** The usual place for a Python
  tool's settings. Turned down as the only place: a repo of notes has no
  `pyproject.toml`, and in a repo that has one it mixes document rules into
  a package's build file.
- **Either file, with one taking precedence** (as ruff reads `ruff.toml` or
  `pyproject.toml`). More flexible, but two places to look and a rule for
  which wins. Adding `pyproject.toml` later is backwards compatible, so it
  can wait for someone to need it.
- **YAML.** Familiar from frontmatter, but needs a parser that isn't in the
  standard library, which would be doclife's first runtime dependency.
- **Command-line flags.** Too many rules, and they'd be repeated in every
  hook and CI step.

## Consequences

- Every repo that uses doclife has one more file at its root.
- The settings file and the frontmatter fields are doclife's public
  interface. Once 1.0 is out, renaming a key is a major version.
- Porting the checks ([#3](https://github.com/ndomako10/doclife/issues/3))
  starts with reading and validating this file.

## Revisions

- 2026-11-27: written.
