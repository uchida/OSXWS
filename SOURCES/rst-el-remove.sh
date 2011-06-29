#!/bin/sh -e
# /usr/lib/emacsen-common/packages/remove/rst-el

FLAVOR=$1
PACKAGE=rst-el
STARTDIR=/etc/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el"

if [ "X${FLAVOR}" = "X" ]; then
    echo Need argument to determin FLAVOR of emacs;
    exit 1
fi

if [ "X${PACKAGE}" = "X" ]; then
    echo Internal error: need package name;
    exit 1;
fi

ELCDIR=/usr/share/${FLAVOR}/site-lisp/${PACKAGE}

case "${FLAVOR}" in
    emacs)
    ;;
    *)
    echo -n "remove/${PACKAGE}: Handling removal of emacsen flavor ${FLAVOR} ..."
    rm -rf ${ELCDIR}
    rm -f ${STARTDIR}/95${STARTFILE}*
    echo " done."
    ;;
esac

exit 0
