all: build upload

clean:
	rm -rf _build

build:
	run-rstblog build

serve:
	run-rstblog serve

upload:
    rsync -a --delete _build/ ../.develop-blog-www/
    git co gh-pages
    rm * -rf
    mv ../.develop-blog-www/develop-notes/* .
    @echo "Done..."