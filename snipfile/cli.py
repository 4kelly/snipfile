import argparse

from snipfile.commands import snipfiles


def main():
    parser = argparse.ArgumentParser(description="Inject snippets from other files.")

    parser.add_argument("--input-dir", type=str)
    parser.add_argument("--output-dir", type=str)
    parser.add_argument("--pattern", type=str, default="*")

    args = parser.parse_args()

    if args.input_dir == args.output_dir:
        raise ValueError("setting --input-dir == --output-dir will cause the original files to be overwritten.")

    snipfiles(args.input_dir, args.output_dir, args.pattern)


if __name__ == "__main__":
    main()
