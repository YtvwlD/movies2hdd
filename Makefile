.PHONY: docs install remove help
help: 
	@echo "Possible targets: docs, install and remove"

docs: 
	doxygen

install:
	mkdir -p /usr/lib/movies2hdd
	cp -R movies2hdd/* /usr/lib/movies2hdd/
	ln -s /usr/lib/movies2hdd /usr/lib/python2.7/dist-packages/movies2hdd
	ln -s /usr/lib/movies2hdd /usr/lib/python3/dist-packages/movies2hdd
	cp bin/movies2hdd /usr/bin/movies2hdd

remove:
	rm /usr/bin/movies2hdd
	rm /usr/lib/python3/dist-packages/movies2hdd
	rm /usr/lib/python2.7/dist-packages/movies2hdd
	rm -r /usr/lib/movies2hdd
