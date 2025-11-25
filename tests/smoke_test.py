"""Verbose smoke test for piraye package.

This script performs a minimal import and normalization operation and
prints the normalized text and punctuation positions. It exits with
code 0 on success and non-zero on failure so CI can detect problems.
"""

# Add project root to sys.path so the test can import the local `piraye`
# package when the file is executed directly (e.g. `python tests/smoke_test.py`).
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from piraye import NormalizerBuilder


def run_smoke_test():
    try:
        # Build a simple normalizer without tokenization to avoid external downloads
        norm = (
            NormalizerBuilder()
            .alphabet_en()
            .punctuation_en()
            .space_normal()
            .remove_extra_spaces()
            .build()
        )

        text = "Hello  ,World!"
        normalized_text, result = norm.normalize(text)

        print("Original:", repr(text))
        print("Normalized:", repr(normalized_text))
        print("Punctuation positions:", result.punc_positions)

        # Basic sanity checks
        if not isinstance(normalized_text, str):
            print("FAIL: Normalized text is not a string")
            return 2
        if normalized_text == "":
            print("FAIL: Normalization produced an empty string")
            return 3
        if not hasattr(result, "punc_positions"):
            print("FAIL: Result missing punc_positions")
            return 4
        if not isinstance(result.punc_positions, list):
            print("FAIL: punc_positions is not a list")
            return 5

        for pos in result.punc_positions:
            if not (0 <= pos < len(normalized_text)):
                print(f"FAIL: Punctuation position {pos} out of range")
                return 6
            ch = normalized_text[pos]
            if ch.isalnum() or ch.isspace():
                print(f"FAIL: Character at {pos} is not punctuation: {ch!r}")
                return 7

        print("SMOKE TEST PASSED")
        return 0

    except Exception as exc:  # show unexpected errors
        print("SMOKE TEST ERROR:", exc)
        return 1


if __name__ == "__main__":
    run_smoke_test()
