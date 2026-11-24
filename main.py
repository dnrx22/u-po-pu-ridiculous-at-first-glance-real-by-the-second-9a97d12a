#!/usr/bin/env python3
"""Generate a one-sentence startup pitch for the make.fun competition
u-po-pu-ridiculous-at-first-glance-real-by-the-second-9a97d12a.

Writes the pitch sentence to entry.txt in the directory given by the
MAKEFUN_OUTPUT_DIR environment variable (default /output). Deterministic,
stdlib only, no network access.
"""

import hashlib
import os
import sys

PITCH = (
    "We deliver trained goats to chew overgrown lawns, and suburban "
    "homeowners pay $49 a visit because goats eat the weeds, fertilize "
    "the soil, and never need petrol."
)


def validate(text: str) -> None:
    """Validate the pitch sentence against the competition constraints."""
    if not text:
        raise ValueError("pitch must not be empty")
    if text != text.strip():
        raise ValueError("pitch must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("pitch must be exactly one line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("pitch must not contain control characters")
    if not 1 <= len(text) <= 200:
        raise ValueError(
            f"pitch must be 1-200 characters, got {len(text)}"
        )


def main() -> int:
    validate(PITCH)
    text_bytes = PITCH.encode("utf-8")
    # Round-trip check: the text must be valid UTF-8 that decodes cleanly.
    if text_bytes.decode("utf-8") != PITCH:
        raise ValueError("pitch is not clean UTF-8")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(text_bytes)

    # Read the file back and re-validate: what is on disk must be exactly
    # the validated pitch, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != text_bytes:
        raise ValueError("written file does not match validated pitch")
    validate(written.decode("utf-8"))

    digest = hashlib.sha256(text_bytes).hexdigest()
    print(f"wrote {out_path}")
    print(f"sha256: {digest}")
    print(f"characters: {len(PITCH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
