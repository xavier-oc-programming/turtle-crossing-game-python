import os
import sys
import subprocess
from pathlib import Path

from art import LOGO

ORIGINAL = Path(__file__).parent / "original" / "main.py"
ADVANCED = Path(__file__).parent / "advanced" / "main.py"


def main() -> None:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(LOGO)
        print("Select a version:")
        print("  1 — Original  (course build, procedural)")
        print("  2 — Advanced  (OOP rebuild, pause + title screen)")
        print("  q — Quit")
        choice = input("\nEnter choice: ").strip().lower()

        if choice == "1":
            subprocess.run(
                [sys.executable, str(ORIGINAL)],
                cwd=str(ORIGINAL.parent),
            )
        elif choice == "2":
            subprocess.run(
                [sys.executable, str(ADVANCED)],
                cwd=str(ADVANCED.parent),
            )
        elif choice == "q":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
