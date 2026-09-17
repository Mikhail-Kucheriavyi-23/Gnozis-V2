"""Machine-readable context recovery entry point."""

from __future__ import annotations

import argparse
import json

from .snapshot import build_context_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit a read-only Gnozis context snapshot")
    parser.add_argument("--root", default=".", help="project checkout root")
    args = parser.parse_args()
    print(json.dumps(build_context_snapshot(args.root), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
