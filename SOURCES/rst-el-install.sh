#! /bin/sh -e
# /usr/osxws/lib/emacsen-common/packages/install/rst-el

FLAVOR=$1
PACKAGE=rst-el

FLAGS="${SITEFLAG} -q -batch -f batch-byte-compile"

ELDIR="/usr/osxws/share/emacs/site-lisp/${PACKAGE}"
ELCDIR="/usr/osxws/share/${FLAVOR}/site-lisp/${PACKAGE}"
STARTDIR=/usr/osxws/etc/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el"

ECHO="/usr/bin/echo"

SOURCES="rst.el"

case "${FLAVOR}" in
    emacs)
    ;;
    *) 
    $ECHO -n "install/${PACKAGE}: Byte-compiling for ${FLAVOR} ..."
    install -m 755 -d ${ELCDIR}
    cd ${ELDIR}
    cp *.el ${ELCDIR}
    FILES="${SOURCES}"
    cd ${ELCDIR}
    ${FLAVOR} ${FLAGS} ${FILES} > ${ELCDIR}/CompilationLog 2>&1
    rm -f ${SOURCES}
    gzip -9 ${ELCDIR}/CompilationLog

    ln -sf ${ELDIR}/${STARTFILE} ${STARTDIR}/95${STARTFILE};
    $ECHO " done."
    ;;
esac

exit 0 ;
