#!/bin/env python3
#
# Build the amp-mgms tarball for distribution
#

import argparse
import logging
import tempfile
from pathlib import Path
import shutil
import sys
import os
import subprocess
import zipfile
import json
from amp.package import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Turn on debugging")
    parser.add_argument('--package', default=False, action='store_true', help="build a package instead of installing")
    parser.add_argument('--clean', default=False, action='store_true', help="Clean previous build & dependencies")
    parser.add_argument('destdir', help="Output directory for package or webserver path root", nargs='?')
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)

    if args.package and not args.destdir:
        logging.error("You must supply a destdir when building a package")
        exit(1)

    if not args.package:
        logging.info(f"MGM Scoring tools code is in dist directory")
        exit(0)

    if args.package:
        with tempfile.TemporaryDirectory() as builddir:
            version = "1.0"

            pfile = create_package("amp_mgm_scoring_tools", version, "mgm_scoring_tools",
                                Path(args.destdir), Path(builddir),
                                system_defaults='amp_config.system_defaults',
                                depends_on='amp_python')
                                
            logging.info(f"New package is in {pfile}")


if __name__ == "__main__":
    main()