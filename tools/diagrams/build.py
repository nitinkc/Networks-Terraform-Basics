"""Regenerate every .drawio + .svg diagram in docs/ from the specs in this folder.

    python3 tools/diagrams/build.py            # rebuild everything
    python3 tools/diagrams/build.py theory     # only modules whose name contains 'theory'

Pure standard library. Each spec writes <name>.drawio (editable in draw.io) and
<name>.svg (embedded by MkDocs) from the same primitives, so they never drift apart.
"""
import importlib
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

MODULES = ["theory_a", "theory_b", "theory_c", "theory_d", "theory_e", "labs_a", "labs_b", "f5"]
PREFIXES = ("d0", "d1", "lab", "tf", "f5_", "apigee_", "shopnow", "lab_f5")


def main(flt=""):
    count = 0
    for name in MODULES:
        if flt and flt not in name:
            continue
        mod = importlib.import_module(name)
        for fn_name, fn in inspect.getmembers(mod, inspect.isfunction):
            if fn.__module__ == name and fn_name.startswith(PREFIXES) and not inspect.signature(fn).parameters:
                fn()
                count += 1
    print(f"built {count} diagrams")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
