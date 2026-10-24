"""Byte-level acceptance check. Process exit zero is not semantic success."""
import sys
from pathlib import Path

actual = Path(sys.argv[1]).read_bytes()
expected = bytes.fromhex('33 36 20 0a')
if actual != expected:
    print(f'REJECT actual={actual!r} expected={expected!r}')
    raise SystemExit(1)
print('ACCEPT exact pinned output')
