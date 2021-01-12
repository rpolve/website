$(shell { grep -l "^[Aa]uthor:" *.md | xargs sed -Ei /^[Aa]uthor:/d ;} 2>/dev/null)

SRC_FILES := $(wildcard *.md)
OBJ_FILES := $(patsubst %.md,%.html,$(SRC_FILES))

.PHONY: all
all: $(OBJ_FILES) blog cv

style.css:
	cp $$XDG_DATA_HOME/pandoc/style.css .

index.html: index.md style.css
	pandoc $< \
	    -H header.html \
	    --css=style.css \
	    --highlight-style=haddock \
	    --to=html \
	    --output=$@

%.html: %.md style.css
	pandoc $< \
	    -H header.html \
	    -B topbar.html \
	    -A footer.html \
	    --css=style.css \
	    --highlight-style=haddock \
	    --to=html \
	    --output=$@ \
	    --toc

.PHONY: cv
cv:
	$(MAKE) -C cv -f recipe.mk

.PHONY: blog
blog:
	$(MAKE) -C blog -f recipe.mk
	mkdir -p feed
	mv -v blog/*.xml feed/

.PHONY: clean
clean:
	rm -f $(OBJ_FILES) style.css blog/*.html feed/*.xml
