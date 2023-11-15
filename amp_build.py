#!/bin/env python3

from amp.package import *
import argparse
import logging
from pathlib import Path
import sys
import tempfile
import shutil, os

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")    
    parser.add_argument("--package", default=False, action="store_true", help="Build package instead of install")
    parser.add_argument("destination", help="Destination for build (should be an AMP_ROOT for non-package)")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)

    # Build the software
    # this is a simple script MGM, so there's nothing to really build
    # here, but if there were, here's where it'd be done.
    pass



    # Install the software
    # This is going to copy the files we need to use the MGM -- but not
    # the stuff that goes into the package (like the lifecycle scripts
    # and config defaults).  One assumes that prior to installation the
    # developer has put the configuration in their amp.yaml configuration
    # for testing    
    # Since this is an MGM, the installation path is 'galaxy/tools/sample_mgm' 
    # so it's separate from other MGMs.
    installation_path = "mgm_scoring_tools"

    destdir = Path(args.destination)
    if args.package:
        # create a temporary directory for the build.
        tempdir = tempfile.TemporaryDirectory()
        destdir = Path(tempdir.name)

    # create our installation path
    (destdir / installation_path).mkdir(parents=True, exist_ok=True)
    # we're only going to copy the MGM code and the galaxy interface
    # file to the destination
    try: 
        for folder in ('applause_detection', 'audio_segmentation', 'named_entity_recognition', 'shot_detection', 'speech_to_text', 'video_optical_character_recognition'):
            src = sys.path[0] + "/" + folder
            dst = destdir / installation_path / folder
            logging.info(f"Copying {src!s} -> {dst!s}")
            copy_and_overwrite(src, dst)
            # make sure the permissions get copied too...
            shutil.copystat(src, dst)    
    except Exception as e:
        logging.error(f"Failed to copy files: {e}")
        exit(1)

    # Package it, if needed
    if args.package:
        try:
            new_package = create_package("mgm_scoring_tools", "1.0.1", "mgm_scoring_tools",
                                Path(args.destination), destdir / installation_path,
                                # can also be a list.
                                depends_on='amp_python')
            logging.info(f"New package in {new_package}")    
        except Exception as e:
            logging.error(f"Failed to build backage: {e}")
            exit(1)


if __name__ == "__main__":
    main()