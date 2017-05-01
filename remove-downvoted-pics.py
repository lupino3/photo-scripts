#!/usr/bin/env python3
#
# remove-downvoted-pics.py
#
# Removes all the pictures for which both RAW and JPG were marked as removed
# in Darktable (rating is -1), and the corresponding sidecar files. The
# removal is done by iterating on a given directory, finding all sidecar files
# (.xmp), finding the rating and removing the image + sidecar if the rating is
# -1.

import argparse
import glob
import os
import xml.etree.ElementTree as ET

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
    xmp_files = glob.glob(os.path.join(directory, "*.xmp"))

    if args.verbose:
        print("Found %d xmp files: %s." % (len(xmp_files), ", ".join(xmp_files)))

    low_rating = []
    high_rating = []  # used just for logging.
    for xmp in xmp_files:
        tree = ET.parse(xmp)

        # The description tag is the child of the child of the root.
        desc = list(list(tree.getroot())[0])[0]
        attr = desc.attrib
        rating = [v for k, v in desc.attrib.items() if k.endswith('Rating')][0]
        f = [v for k, v in desc.attrib.items() if k.endswith('DerivedFrom')][0]

        if rating == "-1":
            low_rating.append(f)
        else:
            high_rating.append(f)

    if args.verbose:
        print("low rating: " + ", ".join(low_rating))
        print("high rating: " + ", ".join(high_rating))

    # Get only the base names of the files stored in low_rating and
    # high_rating, and find all the basenames which only have a low rating.
    # This is necessary because in my workflow I typically remove one of the
    # RAW or JPG files, depending on which one I process, and in this case I
    # don't want to remove the corresponding JPG or RAW file. But if a
    # basename is only in low_ratings, then both RAW and JPG were removed
    # during the Darktable processing.
    #
    # These are the files we want to remove.
    lr_basenames = set(os.path.splitext(f)[0] for f in low_rating)
    hr_basenames = set(os.path.splitext(f)[0] for f in high_rating)
    basenames_to_remove = lr_basenames - (lr_basenames & hr_basenames)

    if args.verbose:
        print(sorted(basenames_to_remove))

    files_to_remove = []
    for basename in basenames_to_remove:
        for f in low_rating + high_rating:
            if f.startswith(basename):
                files_to_remove.append(os.path.join(directory, f))
                # Also add the corresponding XMP file.
                files_to_remove.append(os.path.join(directory, f + ".xmp"))

    if args.verbose:
        print(sorted(files_to_remove))

    # Remove files or, if it's a dry run, output files to remove.
    if not args.dry_run:
        for f in files_to_remove:
            os.remove(f)
    else:
        print("DRY_RUN. Would remove:\n " + "\n ".join(sorted(files_to_remove)))
        print()

    # Additional output.
    if args.verbose:
        print("Removed " + str(len(files_to_remove)) + " files.")
        if args.dry_run:
            print("(Not really. DRY_RUN)")
