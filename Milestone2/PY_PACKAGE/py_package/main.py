import time
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: hello <name>")
        return

    name = sys.argv[1]

    while True:
        print(f"Hello {name}")
        time.sleep(1)

if __name__ == "__main__":
    main()