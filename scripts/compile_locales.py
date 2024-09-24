import argparse
from pathlib import Path

import polib


def create_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile .po files to .mo files")
    parser.add_argument(
        "locales_dir",
        type=str,
        help="Path to the locales directory",
        nargs="?",
        default="locales",
    )
    return parser


def get_locales_dir_sysarg():
    parser = create_argparse()
    args = parser.parse_args()
    return args.locales_dir


def compile_translations(path):
    script_path = Path(__file__).parent.parent
    locales_path = script_path / path

    for po_file in locales_path.rglob("*.po"):
        mo_file = po_file.with_suffix(".mo")
        po = polib.pofile(str(po_file))
        po.save_as_mofile(str(mo_file))
        print(f"Compiled {po_file} to {mo_file}")

    print("Done")


if __name__ == "__main__":
    locales_dir = get_locales_dir_sysarg()
    compile_translations(locales_dir)
