from ftplib import FTP
from pprint import pprint
import re
import argparse
import toml
import sys


def get_file(package_name: str) -> None:
    tomldata = toml.load("texpkg.toml")
    ftp = FTP("ftp.core.ring.gr.jp")
    ftp.login()
    ftp.cwd("/pub/text/TeX/ptex-win32/current/")
    file_list = ftp.mlsd()

    for filename, opt in file_list:
        if bool(re.search(package_name, filename)):
            print(filename)
            pprint(opt)
            tomldata["packages"]["packages"].append(filename)
            toml.dump(tomldata, open("texpkg.toml", mode="w"))
            with open(filename, "xb") as f:
                ftp.retrbinary("RETR {}".format(filename), f.write)
    ftp.quit()


def cli_parse():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="wtmgr - Package Manager for W32TeX."
        )
    parser.add_argument(
        "-S",
        action="store",
        help="Install Package",
        nargs=1,
        required=True
        )
    arg = parser.parse_args(sys.argv[1:])
    print(arg)
    return arg


arg = cli_parse()
get_file(arg.S[0])
