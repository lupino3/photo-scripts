#!/usr/bin/env python3
#
# remove-unneeded-raws.py
#
# Removes the RAW files that are not needed after the first selection is done
# in JPGs. It simply removes any RAW files for which there is no corresponding
# JPG file.
#
# This is useful because I typically shoot in RAW+JPG and then do the first
# selection with JPGs only using EOG (Eye Of Gnome).

import argparse
import os

# Constants
RAW_EXTENSIONS = ("raf", "nef", "RAF", "NEF")
JPEG_EXTENSIONS = ("jpg", "jpeg", "JPG", "JPEG")

# Utility functions.
def is_raw(filename: str) -> bool:
    return any(filename.endswith("." + ext) for ext in RAW_EXTENSIONS)

def is_jpg(filename: str) -> bool:
    return any(filename.endswith("." + ext) for ext in JPEG_EXTENSIONS)

# Main body of the script.
if __name__ == "__main__":
    # Command-line options.
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Directory to process.")
    parser.add_argument("--dry_run", action="store_true", default=False,
            help="Only output files to delete, without deleting them.")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
            help="Verbose output.")
    args = parser.parse_args()

    directory = os.path.expanduser(args.dir)
    files = os.listdir(directory)

    # Get the sets of RAW files and JPG basenames.
    jpg_basenames = set(os.path.splitext(f)[0] for f in files if is_jpg(f))
    raw_files = [f for f in files if is_raw(f)]

    if args.verbose:
        print("JPG: " + ", ".join(sorted(jpg_basenames)))
        print()
        print ("RAW: " + ", ".join(sorted(raw_files)))
        print()

    # Find files to remove.
    to_remove = []
    for raw_file in raw_files:
        basename = os.path.splitext(raw_file)[0]
        if basename not in jpg_basenames:
            to_remove.append(raw_file)

    # Remove files or, if it's a dry run, output files to remove.
    if not args.dry_run:
        for f in to_remove:
            os.remove(os.path.join(directory, f))
    else:
        print("DRY_RUN. Would remove:\n " + "\n ".join(sorted(to_remove)))
        print()

    # Additional output.
    if args.verbose:
        print("Removed " + str(len(to_remove)) + " RAW files.")
        if args.dry_run:
            print("(Not really. DRY_RUN)")
