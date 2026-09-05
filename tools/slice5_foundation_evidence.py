from pathlib import Path

path = Path('docs/IMPLEMENTATION-STATUS.md')
text = path.read_text(encoding='utf-8')
text = text.replace(
    '**Slice 5 - Item Boxes, Weapons & Position-Based Distribution - IMPLEMENTATION STARTED / FOUNDATION REVIEW PENDING**',
    '**Slice 5 - Item Boxes, Weapons & Position-Based Distribution - FOUNDATION CI PASSED / MANNY REVIEW PENDING**',
    1,
)
marker = '## Slice 5 foundation CI evidence\n'
if marker not in text:
    text += '''\n\n## Slice 5 foundation CI evidence\n\nPull request **#97 — Start Slice 5 item-system foundation** is open for Manny review and is intentionally unmerged at this checkpoint. PR head before evidence recording: `3da08a741e514623ddfe28eee100b7fa8bb5ecb8`.\n\nPR CI run **33997897371** passed on Node 22.23.2:\n\n- Git LFS materialization / `git lfs fsck`: passed;\n- `npm ci`: 198 packages installed, 0 vulnerabilities;\n- strict TypeScript build/typecheck: passed;\n- ESLint with `--max-warnings 0`: passed;\n- Vitest: **19 files / 101 tests passed**, including **8 Slice 5 foundation tests**;\n- statement coverage: **89.91% overall**, **93.15% for `game/items`**;\n- runtime verification: 36 materialized GLBs and 105 runtime character PNGs passed;\n- production Vite build: passed;\n- existing large-chunk warning remains non-blocking and unchanged.\n\nNo Pages deployment occurred because this is a pull-request validation run. The next gate is Manny review/approval of PR #97 before merge. The next implementation increment remains blocked until that review decision.\n'''
path.write_text(text, encoding='utf-8')
