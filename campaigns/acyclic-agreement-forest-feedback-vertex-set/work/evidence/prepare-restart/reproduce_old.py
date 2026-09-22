"""Reproduce the old oracle's internal-node-renaming error from preserved Git history."""
import json
from pathlib import Path
import subprocess
import types

root = Path(__file__).resolve().parents[5]
path = 'campaigns/acyclic-agreement-forest-feedback-vertex-set/work/check.py'
source = json.loads(Path(__file__).with_name('internal-renaming.json').read_text())
code = subprocess.run(['git', 'show', 'a056e65:' + path], cwd=root,
                      check=True, capture_output=True, text=True).stdout
old = types.ModuleType('old_check')
old.__file__ = str(root/path)
exec(compile(code, old.__file__, 'exec'), old.__dict__)
actual, _, status = old.source_oracle(source)
assert actual == 2 and status == 'ok'
print('Old checker a056e65: optimum=2; definition: optimum=1 (identical labelled trees).')
