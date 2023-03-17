ifeq ($(PREFIX),)
	PREFIX := /usr/local
endif

APPDIR := $(DESTDIR)$(PREFIX)/share/k1manager/

install:
	install -d $(APPDIR)
	install -m 644 k1manager.py $(APPDIR)
	install -m 644 k1data.py $(APPDIR)
	install -m 644 k1filereader.py $(APPDIR)
	install -m 644 k1midi.py $(APPDIR)
	install -m 644 k1window.ui $(APPDIR)
	cp -r banks $(APPDIR)
	echo '#!/bin/sh\npython3 $(APPDIR)k1manager.py "$$@"' > K1Manager.sh
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 K1Manager.sh $(DESTDIR)$(PREFIX)/bin
