#! /bin/sh -e
#  /usr/osxws/lib/emacsen-common/packages/install/skk
# [ This particular script hasn't been tested, so be careful. ]

set -e

FLAVOR=$1
PACKAGE="skk"
VERSION=13.1

if [ "X${FLAVOR}" = "X" ]; then
    /bin/echo Need argument to determin FLAVOR of emacs;
    exit 1
fi

if [ "X${PACKAGE}" = "X" ]; then
    /bin/echo Internal error: need package name;
    exit 1;
fi

ELDIR=/usr/osxws/share/emacs/site-lisp/${PACKAGE}
ELCDIR=/usr/osxws/share/${FLAVOR}/site-lisp/${PACKAGE}

STARTDIR=/usr/osxws/etc/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el";

SITELISP=/usr/osxws/share/${FLAVOR}/site-lisp
PACKAGEDIR=/usr/osxws/share/${FLAVOR}
EMACSTUTDIR=/usr/osxws/share/skk
XEMACSTUTDIR=/usr/osxws/share/${FLAVOR}/etc/${PACKAGE}
NICOLAELCDIR=/usr/osxws/share/${FLAVOR}/site-lisp/nicola-ddskk

EFLAGS="-batch -q -l SKK-MK"
COMPILE="-batch -q -f batch-byte-compile"

STAMP=${ELCDIR}/compile-stamp

case "${FLAVOR}" in
	emacs)
	;;

	*)

	  if [ ! -d ${EMACSTUTDIR} ] ; then
	    /bin/echo " exited."
	    /bin/echo "W: Please install \`skkdic' package for ${FLAVOR}." ;
	    exit 0;
	  fi

	  /bin/echo -n "install/${PACKAGE}: Byte-compiling for ${FLAVOR} ..."

	  case "${FLAVOR}" in
	       xemacs-*)
		 if [ -f /usr/osxws/lib/xemacs/mule-packages/lisp/skk/skk.elc ]; then
		   exit
		 fi
	       ;;

	       *)
	       ;;
	  esac

	  if [ -e ${STAMP} ]; then
	    if [ "${VERSION}" = "`cat ${STAMP}`" ]; then
	      /bin/echo " exited. (already compiled)" 
	      exit
	    fi
	  fi

	  rm -rf ${ELCDIR}
	  install -m 755 -d ${ELCDIR}
	  rm -rf ${NICOLAELCDIR}
	  install -m 755 -d ${NICOLAELCDIR}

	  # Copy the temp .el files
	  # cp ${ELDIR}/* ${ELCDIR}/

	  # Byte compile them
	  ( cd ${ELDIR}

	    case "${FLAVOR}" in
		 xemacs-*)
		   rm -rf ${XEMACSTUTDIR}
		   make XEMACS=${FLAVOR} package > ${ELCDIR}/CompilationLog 2>&1
		   make XEMACS=${FLAVOR} PACKAGE_LISPDIR=${ELCDIR} \
		        PACKAGE_DATADIR=${XEMACSTUTDIR} install-package \
			  >> ${ELCDIR}/CompilationLog 2>&1
		   ( cd nicola
		     make XEMACS=${FLAVOR} package >> ${ELCDIR}/CompilationLog 2>&1
		     make XEMACS=${FLAVOR} PACKAGEDIR=${PACKAGEDIR} install-package \
			    >> ${ELCDIR}/CompilationLog 2>&1
		   )
		 ;;

		 *)
		   rm -f ${EMACSTUTDIR}/*.tut*
		   make EMACS=${FLAVOR} elc > ${ELCDIR}/CompilationLog 2>&1
		   make EMACS=${FLAVOR} SKK_LISPDIR=${ELCDIR} \
		        SKK_DATADIR=${EMACSTUTDIR} install-elc \
			  >> ${ELCDIR}/CompilationLog 2>&1
		   ( cd nicola
		     make EMACS=${FLAVOR} LISPDIR=${NICOLAELCDIR} install-elc \
			    >> ${ELCDIR}/CompilationLog 2>&1
		   )
	         ;;
	    esac

	    make clean >> ${ELCDIR}/CompilationLog 2>&1
	    rm -fv ${NICOLAELCDIR}/*.el >> ${ELCDIR}/CompilationLog 2>&1
	    ( cd nicola
	      make clean >> ${ELCDIR}/CompilationLog 2>&1
	    )
	  )

	  gzip -9 ${ELCDIR}/CompilationLog
	  /bin/echo ${VERSION} > ${STAMP}

	  install -p -m644 ${ELDIR}/osxws-default-${PACKAGE}.el ${ELCDIR}
	  cp -f ${ELDIR}/${STARTFILE} ${STARTDIR}/70${STARTFILE};
	  /bin/echo " done."
	;;
esac

exit 0;
