import json
import sys

THRESHOLD = 0.90  # gate: must be >= 0.90


def main():
    text = sys.stdin.read()
    if not text.strip():
        print("No input received on stdin.")
        sys.exit(2)

    # Find the last JSON-looking line
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    data = None

    for ln in reversed(lines):
        if ln.startswith("{") and ln.endswith("}"):
            try:
                data = json.loads(ln)
                break
            except json.JSONDecodeError:
                pass

    if data is None:
        # fallback: try to parse the largest {...} block in the whole text
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                data = json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                data = None

    if data is None:
        print("Could not find a valid JSON object in input.")
        sys.exit(2)

    acc = float(data.get("accuracy", 0.0))

    if acc >= THRESHOLD:
        print(f"PASS: accuracy={acc} >= {THRESHOLD}")
        sys.exit(0)
    else:
        print(f"FAIL: accuracy={acc} < {THRESHOLD}")
        sys.exit(1)


if __name__ == "__main__":
    main()
