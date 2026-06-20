server:
	hugo server --config .hugo/hugo.toml --port 3003

sync:
	rm -fr .hugo && cp -a ../notes/.hugo . && rm -fr .hugo/public
	git add . && git commit -m "test" && git push
