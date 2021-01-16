$(shell { grep -l "^[Aa]uthor:" *.md | xargs sed -Ei /^[Aa]uthor:/d ;} 2>/dev/null)

SRC_FILES := $(wildcard *.md)
OBJ_FILES := $(patsubst %.md,%.html,$(SRC_FILES))

.PHONY: all
all: $(OBJ_FILES) index.html rss.xml
	rm index.md

rss.xml: $(OBJ_FILES)
	gen_feed.py $^

index.md: $(SRC_FILES)
	gen_blog.py > $@

index.html: index.md
	pandoc $< \
	    -B ../res/topbar.html \
	    -A ../res/footer.html \
	    --css=../style.css \
	    --highlight-style=haddock \
	    --to=html \
	    --output=$@
	sed -i '/title-block-header/,/^<\/header>$$/d' $@

%.html: %.md
	pandoc $< \
	    -B ../res/topbar.html \
	    -A ../res/footer.html \
	    --css=../style.css \
	    --highlight-style=haddock \
	    --to=html \
	    --output=$@ \
	    --toc
