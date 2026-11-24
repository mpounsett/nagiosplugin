# Formatting Ruff Statistics

It's possible to nicely format `ruff` statistics for GitHub by using the
`ruff_md.py` script in this directory.

```bash
FORCE_HYPERLINK=1 FORCE_COLOR=1 uv run ruff check --statistics 2>&1 | python3 scripts/ruff_md.py | pbcopy
```

This will then paste nicely into a GitHub issue comment.
