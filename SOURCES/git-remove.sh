#!/bin/sh
# /usr/osxws/lib/emacsen-common/packages/remove/git
set -e

FLAVOR=$1
PACKAGE="git"

if [ "X${FLAVOR}" = "X" ]; then
    echo Need argument to determin FLAVOR of emacs;
    exit 1
fi

if [ "X${PACKAGE}" = "X" ]; then
    echo Internal error: need package name;
    exit 1;
fi

ELDIR=/usr/osxws/share/emacs/site-lisp/${PACKAGE}
ELCDIR=/usr/osxws/share/${FLAVOR}/site-lisp/${PACKAGE}
STARTDIR=/usr/osxws/etc/${FLAVOR}/site-start.d
STARTFILE="$PACKAGE-init.el";

SITELISP=/usr/osxws/share/${FLAVOR}/site-lisp

case "${FLAVOR}" in
	emacs|emacs19|mule)
	;;
	*)
	echo -n "remove/${PACKAGE}: Handling removal of emacsen flavor ${FLAVOR} ..."
	rm -rf ${ELCDIR}
	rm -f ${STARTDIR}/55${STARTFILE}*;
	echo " done."
	;;
esac

exit 0;
