#! /bin/sh -e
# /usr/osxws/lib/emacsen-common/packages/install/mercurial

FLAVOR=$1
PACKAGE=mercurial

STARTDIR=/usr/osxws/etc/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el";

FLAGS="${SITEFLAG} -q -batch -f batch-byte-compile"

ELDIR="/usr/osxws/share/emacs/site-lisp/${PACKAGE}"
ELCDIR="/usr/osxws/share/${FLAVOR}/site-lisp/${PACKAGE}"


ELISP_FILES="*.el"
BYTECOMPILE_FILES="mercurial.el mq.el"
SOURCES=${ELISP_FILES}

case "${FLAVOR}" in
    emacs)
    ;;

    *)
    echo -n "install/${PACKAGE}: Byte-compiling for ${FLAVOR} ..."
    rm -rf ${ELCDIR}
    install -m 755 -d ${ELCDIR}
    cd ${ELDIR}
    cp ${ELISP_FILES} ${ELCDIR}
    cd ${ELCDIR}
    ${FLAVOR} ${FLAGS} ${BYTECOMPILE_FILES} > ${ELCDIR}/CompilationLog 2>&1
    rm -f ${BYTECOMPILE_FILES}
    gzip -9 ${ELCDIR}/CompilationLog
    ln -sf ${ELDIR}/${STARTFILE} ${STARTDIR}/90${STARTFILE}
    echo " done."
    ;;

    *)
    ;;

esac

exit 0 ;
