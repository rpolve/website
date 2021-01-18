#!/usr/bin/env python3
"""
    genfeed.py
    blog/

    Author: Roberto Polverelli Monti <rpolverelli at gmail>
    Created on: 2021 Jan 12
    Description:
"""
import re
import sys
from datetime import datetime
from email.utils import format_datetime
from feedgen.feed import FeedGenerator

title_RE = re.compile("<title>(.*)</title>$")
para_RE = re.compile("<p>(.*)</p>$")
heading_RE = re.compile("<h\d id=[^>]+>(.*)</h\d>$")
img_RE = re.compile('<img src=[^>]+ />')


fg = FeedGenerator()
fg.id("https://roberto.pm/blog/")
fg.title("Roberto PM")
fg.author({"name": "Roberto"})
fg.subtitle("My latest blog posts.")
fg.link(href="https://roberto.pm/blog/rss.xml", rel="self", type="application/rss+xml")
fg.language("en")


def main():
    items = sys.argv[1:]

    for i in items:
        if i == "index.html":
            continue

        src = i.split(".")[0] + ".md"
        with open(src) as f:
            f = f.read().splitlines()

            for l in f:
                if l == "...":
                    break
                elif "    Timestamp: " in l:
                    timestamp = int(l.split(":")[-1])
                    pub_date = format_datetime(datetime.fromtimestamp(timestamp))

        with open(i) as f:
            f = f.read().splitlines()

            d = ""
            for l in f:
                is_title = title_RE.search(l)
                is_heading = heading_RE.search(l)
                is_para = para_RE.search(l)
                is_img = img_RE.search(l)
                if is_para:
                    d += is_para[0]
                    d += "<br />"
                elif is_img:
                    d += is_img[0]
                    d += "<br />"
                elif is_heading:
                    d += is_heading[0]
                    d += "<br />"
                elif is_title:
                    title = is_title[1]

            if d[-6:] == '<br />':
                d = d[:-6]

        k = i.split(".")[0]
        fe = fg.add_entry()
        fe.id("https://roberto.pm/blog/{}.html".format(k))
        fe.title(title)
        fe.link(href="https://roberto.pm/blog/{}.html".format(k))
        fe.description(d)
        fe.pubDate(pub_date)

    fg.rss_file("rss.xml")


if __name__ == "__main__":
    main()
