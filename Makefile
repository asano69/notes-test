sync:
	rm -fr .hugo && cp -a ../computer/.hugo . && rm -fr .hugo/public

server: sync
	hugo server --config .hugo/hugo.toml --port 3004 --bind 0.0.0.0 --baseURL http://spica.home.arpa


push: sync
	git add . && git commit -m "test" && git push
