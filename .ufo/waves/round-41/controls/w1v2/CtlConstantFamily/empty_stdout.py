#!/usr/bin/env python3
"""Round-41 control (constant family): a clean exit code (0) and no stdout at all.

The manifest is read only to confirm it is well formed; nothing is emitted and no
URL character, component, scheme or host is judged. This measures what the
counter does with a tool that claims success by exit code alone.
"""

import json
import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    try:
        with open(argv[2], "rb") as handle:
            document = json.loads(handle.read().decode("utf-8"))
        checks = document["checks"]
        if document.get("version") != 1 or not isinstance(checks, list) or not checks:
            raise ValueError("manifest")
    except Exception:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
