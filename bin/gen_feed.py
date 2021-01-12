#!/usr/bin/env python3
"""
    genfeed.py
    blog/

    Author: Roberto Polverelli Monti <rpolverelli at gmail>
    Created on: 2021 Jan 12
    Description:
"""
import sys
from feedgen.feed import FeedGenerator


fg = FeedGenerator()
fg.id("https://roberto.pm/blog/")
fg.title("Roberto PM")
fg.author({"name": "Roberto"})
fg.subtitle("My latest blog posts.")
fg.link(href="https://roberto.pm/feed/rss.xml", rel="self", type="application/rss+xml")
fg.language("en")


def main():
    items = sys.argv[1:]

    for i in items:
        with open(i) as f:
            f = f.read().splitlines()
            for l in f:
                if "..." == l:
                    break
                elif "title: " in l:
                    title = l.split(":")[-1].lstrip()[1:-1]
        k = i.split(".")[0]
        fe = fg.add_entry()
        fe.id("https://roberto.pm/blog/{}.html".format(k))
        fe.title(title)
        fe.link(href="https://roberto.pm/blog/{}.html".format(k))

        d = "<p>"
        c = False
        for l in f:
            if l == "":
                if not c:
                    c = True
                    continue
                else:
                    d = d.rstrip()
                    d += "</p><p>"
            else:
                if c:
                    d += l
                    d += " "
        else:
            d = d.rstrip()
            d += "</p>"

        fe.description(d)

    fg.rss_file("rss.xml")


if __name__ == "__main__":
    main()