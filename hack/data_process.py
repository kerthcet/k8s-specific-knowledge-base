"""
This script helps to remove commented-out sentences in markdowns.
Raw contents should be placed under k8s-specific-knowledge-base/_contents.
"""

import os

prefix = "<!--"
suffix = "-->"


def walk_files(path: str):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if not filename.endswith(".md"):
                continue

            destPath = dirpath.replace("../_", "../")
            if not os.path.exists(destPath):
                os.makedirs(destPath)

            with open(destPath + "/" + filename, "w") as f:
                with open(dirpath + "/" + filename) as r:
                    lines = r.readlines()
                    continue_write = True
                    for line in lines:
                        if prefix in line:
                            continue_write = False

                        if continue_write:
                            f.write(line)

                        if suffix in line:
                            continue_write = True


walk_files("../_contents")
