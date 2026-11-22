# One aligned log line per step,
# so the output reads like the code.
import textwrap


def step(n, name, *what):
    print(f"{n}. {name:<7}", *what)


def sample(*what):
    print(" " * 10, *what)


def reply(text):
    text = " ".join(text.split())
    for line in textwrap.wrap(text, 40):
        print("  " + line)
