.PHONY: all
all: cv.pdf

%.pdf: cv.mom
	groff -k -mom -Tpdf < $< > $@
