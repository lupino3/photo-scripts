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

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Directory to process.")
parser.add_argument("--dry_run", action="store_true", default=False,
        help="Only output files to delete, without deleting them.")
parser.add_argument("--verbose", action="store_true", default=False,
        help="Verbose output.")
args = parser.parse_args()

RAW_EXTENSIONS = ("raf", "nef", "RAF", "NEF")
JPEG_EXTENSIONS = ("jpg", "jpeg", "JPG", "JPEG")

def is_raw(filename: str) -> bool:
    return any(filename.endswith("." + ext) for ext in RAW_EXTENSIONS)

def is_jpg(filename: str) -> bool:
    return any(filename.endswith("." + ext) for ext in JPEG_EXTENSIONS)

directory = os.path.expanduser(args.dir)
files = os.listdir(directory)

jpg_basenames = set([os.path.splitext(f)[0] for f in files if is_jpg(f)])
if args.verbose:
    print("JPG: " + ", ".join(jpg_basenames))
    print()

raw_files = [f for f in files if is_raw(f)]
if args.verbose:
    print ("RAW: " + ", ".join(raw_files))
    print()

to_remove = []
for raw_file in raw_files:
    basename = os.path.splitext(raw_file)[0]
    if basename not in jpg_basenames:
        to_remove.append(raw_file)

if args.dry_run:
    print("DRY_RUN. Would remove: " + ", ".join(to_remove))
    print()
else:
    for f in to_remove:
        os.remove(os.path.join(directory, f))

if args.verbose:
    print("Removed " + str(len(to_remove)) + " RAW files.")
    if args.dry_run:
        print("(Not really. DRY_RUN)")
