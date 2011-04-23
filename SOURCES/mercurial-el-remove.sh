#!/bin/sh -e
# /usr/osxws/lib/emacsen-common/packages/remove/mercurial

FLAVOR=$1
PACKAGE=mercurial

if [ "X${FLAVOR}" = "X" ]; then
    echo Need argument to determin FLAVOR of emacs;
    exit 1
fi

if [ "X${PACKAGE}" = "X" ]; then
    echo Internal error: need package name;
    exit 1;
fi

ELCDIR=/usr/osxws/share/${FLAVOR}/site-lisp/${PACKAGE}
STARTDIR=/etc/osxws/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el";


case "${FLAVOR}" in
    emacs)
    ;;
    *)
    echo -n "remove/${PACKAGE}: Handling removal of emacsen flavor ${FLAVOR} ..."
    rm -rf ${ELCDIR}
    rm -f ${STARTDIR}/90${STARTFILE}*
    echo " done."
    ;;
esac

exit 0
