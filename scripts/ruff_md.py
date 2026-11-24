#!/usr/bin/env python3
import re
import sys

OSC8 = re.compile(r"\x1b\]8;[^;\x1b\x07]*;([^\x1b\x07]*)(?:\x1b\\|\x07)(.*?)"
                  r"\x1b\]8;;(?:\x1b\\|\x07)")
SGR = re.compile(r"\x1b\[[0-9;]*m")

rows = []
footer = []

for line in sys.stdin.read().splitlines():
    line = OSC8.sub(lambda m: f"[{m.group(2)}]({m.group(1)})", line)
    line = SGR.sub("", line).strip()
    if line:
        try:
            count, code, name = re.split(r"\t+|\s{2,}", line)
            rows.append([count, code, name])
        except ValueError:
            footer.append(line)

width = max(map(len, rows))
header = ["Count", "Code", "Name"] + [""] * (width - 3)
print("| " + " | ".join(header[:width]) + " |")
print("|---:|" + "---|" * (width - 1))
for r in rows:
    r[-1] = f"`{r[-1]}`"
    r += [""] * (width - len(r))
    print("| " + " | ".join(r) + " |")
for i, f in enumerate(footer):
    if i == 0:
        print()
    print(f)
