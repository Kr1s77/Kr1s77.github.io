all: build upload

clean:
	rm -rf _build

build:
	run-rstblog build

serve:
	run-rstblog serve
