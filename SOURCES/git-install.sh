#! /bin/sh -e
#  /usr/osxws/lib/emacsen-common/packages/install/git

set -e

FLAVOR=$1
PACKAGE="git"

SOURCES="git.el git-blame.el"

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

case "${FLAVOR}" in
    emacs|emacs19|mule)
        ;;
    *)
	echo -n "install/${PACKAGE}: Byte-compiling for ${FLAVOR} ..."
        rm -rf ${ELCDIR}
        install -m 755 -d ${ELCDIR}

        # Copy the temp .el files
        cp -a ${ELDIR}/* ${ELCDIR}/

        # Byte compile them
        (cd ${ELCDIR}
            ${FLAVOR} -batch -q -no-site-file \
                      -f batch-byte-compile ${SOURCES} > CompilationLog 2>&1
            rm -f ${SOURCES}
        )
        gzip -9 ${ELCDIR}/CompilationLog
        ln -sf ${ELDIR}/${STARTFILE} ${STARTDIR}/55${STARTFILE}
        echo " done."
        #
        ;;
esac

exit 0;
