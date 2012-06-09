URL=http://127.0.0.1/wiki
WAIT=1
CHUNKS=50
NAMESPACE=1

DUMPS=$(shell ls splits/names_* | sed 's!names_!dump_!; s!splits!download!;')

all: splits ${DUMPS}

allpages_list.html:
		wget ${URL}/index.php?title=Special:AllPages\&namespace=${NAMESPACE} -O allpages_list.html || rm allpages_list.html

allpages_list.txt: allpages_list.html
		tidy -utf8  -asxml --force-output yes  < allpages_list.html 2> /dev/null | xml2 | grep 'title=Special:AllPages' | grep from | perl -ne '/^[^=]*=(.*)/ and print "${URL}$$1\n"' | sort | uniq > allpages_list.txt

allpages_download.html: allpages_list.txt
		wget -i allpages_list.txt -w ${WAIT} -O allpages_download.html || rm allpages_download.html

allpages.txt: allpages_download.html
		cat allpages_download.html allpages_list.html | tidy -utf8  -asxml --force-output yes 2> /dev/null | xml2 | grep '@title=' | sed 's/^[^=]*=//' | sort | uniq | grep -v 'Special:' > allpages.txt


splits: allpages.txt
		rm -Rf splits
		mkdir -p splits
		split allpages.txt -a 8 -d -l ${CHUNKS} splits/names_
		mkdir -p download
		@echo Now need to download actual dumps. '"make"' again.

download/dump_%: splits/names_%
		cat $< | perl -e '$$_=join("", <STDIN>); use URI::Escape; print "pages=",uri_escape($$_);' | curl --http1.0 -f --data  'curonly=1' --data wpExportTemplates=0 --data wpDownload=1 --data @- '${URL}/index.php?title=Special:Export&action=submit' > $@ || rm $@
		sleep ${WAIT}

dump.xml: ${DUMPS}
		head -n 1 download/dump_00000000 > dump.xml || rm dump.xml
		cat download/dump_* | grep -v '</\?mediawiki' >> dump.xml
		echo '</mediawiki>' >> dump.xml

clean:
		rm -Rf splits download allpages*
