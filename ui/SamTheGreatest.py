import argparse

def main():
    parser = argparse.ArgumentParser(description="MIPS 32-bit Simulator Interface")
    parser.add_argument(
        'program', nargs='?', help="Path to the MIPS assembly program (optional)"
    )
    args = parser.parse_args()

    if args.program:
        print(f"Program file specified: {args.program}")
        # Future integration point: Pass to backend for processing
    else:
        print("No program file specified. This is only the interface.")

if __name__ == "__main__":
    main()

