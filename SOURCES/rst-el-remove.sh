#!/bin/sh -e
# /usr/osxws/lib/emacsen-common/packages/remove/rst-el

FLAVOR=$1
PACKAGE=rst-el
STARTDIR=/usr/osxws/etc/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el"

ECHO="/usr/bin/echo"

if [ "X${FLAVOR}" = "X" ]; then
    $ECHO Need argument to determin FLAVOR of emacs;
    exit 1
fi

if [ "X${PACKAGE}" = "X" ]; then
    echo Internal error: need package name;
    exit 1;
fi

ELCDIR=/usr/osxws/share/${FLAVOR}/site-lisp/${PACKAGE}

case "${FLAVOR}" in
    emacs)
    ;;
    *)
    $ECHO -n "remove/${PACKAGE}: Handling removal of emacsen flavor ${FLAVOR} ..."
    rm -rf ${ELCDIR}
    rm -f ${STARTDIR}/95${STARTFILE}*
    $ECHO " done."
    ;;
esac

exit 0
