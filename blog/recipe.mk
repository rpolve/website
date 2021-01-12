$(shell { grep -l "^[Aa]uthor:" *.md | xargs sed -Ei /^[Aa]uthor:/d ;} 2>/dev/null)

SRC_FILES := $(wildcard *.md)
OBJ_FILES := $(patsubst %.md,%.html,$(SRC_FILES))

.PHONY: all
all: $(OBJ_FILES) index.html feed
	rm index.md

index.md: $(OBJ_FILES)
	genindex.py >$@

index.html: index.md
	pandoc $< \
	    -B ../topbar.html \
	    -A ../footer.html \
	    --css=../style.css \
	    --highlight-style=haddock \
	    --to=html \
	    --output=$@
	sed -i '/title-block-header/,/^<\/header>$$/d' $@

%.html: %.md
	pandoc $< \
	    -B ../topbar.html \
	    -A ../footer.html \
	    --css=../style.css \
	    --highlight-style=haddock \
	    --to=html \
	    --output=$@ \
	    --toc

.PHONY: feed
feed: index.md $(SRC_FILES)
	genfeed.py $^
