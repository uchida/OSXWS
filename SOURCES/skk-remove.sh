#!/bin/sh
# /usr/osxws/lib/emacsen-common/packages/remove/skk
# [ This particular script hasn't been tested either, so be careful. ]
set -e

FLAVOR=$1
PACKAGE="skk"

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
STARTFILE="${PACKAGE}-init.el";

SITELISP=/usr/osxws/share/${FLAVOR}/site-lisp
EMACSTUTDIR=/usr/osxws/share/skk
XEMACSTUTDIR=/usr/osxws/share/${FLAVOR}/etc/${PACKAGE}
NICOLAELCDIR=/usr/osxws/share/${FLAVOR}/site-lisp/nicola-ddskk

case "${FLAVOR}" in
	emacs)
	;;

	xemacs-*)
	if [ -d ${ELCDIR} ]; then
	  echo -n "remove/${PACKAGE}: Handling removal of emacsen flavor ${FLAVOR} ..."
	  rm -rf ${ELCDIR}
	  rm -rf ${NICOLAELCDIR}
	  rm -rf ${XEMACSTUTDIR}
	  echo " done."
	fi
	;;

	*)
	if [ -d ${ELCDIR} ]; then
	  echo -n "remove/${PACKAGE}: Handling removal of emacsen flavor ${FLAVOR} ..."
	  rm -rf ${ELCDIR}
	  rm -rf ${NICOLAELCDIR}
	  rm -f ${EMACSTUTDIR}/*.tut*
	  echo " done."
	fi
	;;
esac
	rm -f ${STARTDIR}/70${STARTFILE}*;

exit 0;