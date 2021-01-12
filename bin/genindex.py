#!/usr/bin/env python3
"""
    genindex.py
    blog/

    Author: Roberto Polverelli Monti <rpolverelli at gmail>
    Created on: 2021 Jan 12
    Description:
"""
import os

header = """---
lang: en-US
title: 'Recent items'
..."""


def main():
    ls = os.listdir()

    items = {}
    for i in ls:
        i_split = i.split(".")
        ext = i_split[-1]
        url = i_split[0] + ".html"
        if ext != "md" or i_split[0] == "index":
            continue

        with open(i) as f:
            f = f.read().splitlines()
            for l in f:
                if "title: " in l:
                    title = l.split(":")[-1].lstrip()[1:-1]
                if "    First created: " in l:
                    date = l.split(":")[-1].lstrip()
                if "    Timestamp: " in l:
                    secs = int(l.split(":")[-1].lstrip())
                if l == "...":
                    break

        items[secs] = {"url": url, "date": date, "title": title}

    print(header)

    for i in sorted(items, reverse=True):
        k = "\n"
        k += "- **{}:** [{}]({})".format(
            items[i]["date"],
            items[i]["title"],
            items[i]["url"],
        )
        print(k)


if __name__ == "__main__":
    main()
