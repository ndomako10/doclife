# doclife

Frontmatter checks for Markdown docs kept in git: each document carries a
type and its created, modified and last-reviewed dates. A pre-commit hook
stamps the modified date, a checker enforces the rest, and a report lists
documents due for review.

**Status: pre-alpha.** Nothing is released yet. It is being extracted from
a checker that has run in one repo for some time, and is built for a small
number of repos first.

## What it will do

- Check that each document has the fields its type requires, and that
  each folder holds only the types allowed there.
- Stamp `date_modified` on commit, and fail when a document's date is older
  than its last commit.
- List documents whose `last_reviewed` is `never` or older than a set
  period, for policies, runbooks and other documents that go stale.
- Check Architecture Decision Records: numbering, status and the index.

Each repo's folders, types and periods go in a settings file. It has no
runtime dependencies beyond Python 3.11 or newer.

## Development

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe --require-hashes -r requirements-dev.txt
uv pip install --python .venv/Scripts/python.exe --no-deps --no-build-isolation -e .
pre-commit install
.venv/Scripts/python.exe -m pytest
```

On Linux or macOS, the venv's programs are in `.venv/bin/`.

`requirements-dev.txt` is compiled with hashes from `requirements-dev.in`;
the command is in its header. Decisions are in [docs/ADRs](docs/ADRs/README.md).

## License

[GPL-3.0-or-later](LICENSE). Running doclife on a repo places no terms on
that repo's documents; the license covers doclife itself.
