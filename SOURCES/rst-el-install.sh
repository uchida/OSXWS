#! /bin/sh -e
# /usr/lib/emacsen-common/packages/install/rst-el

FLAVOR=$1
PACKAGE=rst-el

FLAGS="${SITEFLAG} -q -batch -f batch-byte-compile"

ELDIR="/usr/share/emacs/site-lisp/${PACKAGE}"
ELCDIR="/usr/share/${FLAVOR}/site-lisp/${PACKAGE}"
STARTDIR=/etc/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el"

SOURCES="rst.el"

case "${FLAVOR}" in
    emacs)
    ;;
    *) 
    echo -n "install/${PACKAGE}: Byte-compiling for ${FLAVOR} ..."
    install -m 755 -d ${ELCDIR}
    cd ${ELDIR}
    cp *.el ${ELCDIR}
    FILES="${SOURCES}"
    cd ${ELCDIR}
    ${FLAVOR} ${FLAGS} ${FILES} > ${ELCDIR}/CompilationLog 2>&1
    rm -f ${SOURCES}
    gzip -9 ${ELCDIR}/CompilationLog

    ln -sf ${ELDIR}/${STARTFILE} ${STARTDIR}/95${STARTFILE};
    echo " done."
    ;;
esac

exit 0 ;
