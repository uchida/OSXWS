#! /bin/sh -e
#  /usr/lib/emacsen-common/packages/install/skk
# [ This particular script hasn't been tested, so be careful. ]

set -e

FLAVOR=$1
PACKAGE="skk"
VERSION=13.1

if [ "X${FLAVOR}" = "X" ]; then
    echo Need argument to determin FLAVOR of emacs;
    exit 1
fi

if [ "X${PACKAGE}" = "X" ]; then
    echo Internal error: need package name;
    exit 1;
fi

ELDIR=/usr/share/emacs/site-lisp/${PACKAGE}
ELCDIR=/usr/share/${FLAVOR}/site-lisp/${PACKAGE}

STARTDIR=/etc/${FLAVOR}/site-start.d
STARTFILE="${PACKAGE}-init.el";

SITELISP=/usr/share/${FLAVOR}/site-lisp
PACKAGEDIR=/usr/share/${FLAVOR}
EMACSTUTDIR=/usr/share/skk
XEMACSTUTDIR=/usr/share/${FLAVOR}/etc/${PACKAGE}
NICOLAELCDIR=/usr/share/${FLAVOR}/site-lisp/nicola-ddskk

EFLAGS="-batch -q -l SKK-MK"
COMPILE="-batch -q -f batch-byte-compile"

STAMP=${ELCDIR}/compile-stamp

case "${FLAVOR}" in
	emacs)
	;;

	*)

	  if [ ! -d ${EMACSTUTDIR} ] ; then
	    echo " exited."
	    echo "W: Please install \`skkdic' package for ${FLAVOR}." ;
	    exit 0;
	  fi

	  echo -n "install/${PACKAGE}: Byte-compiling for ${FLAVOR} ..."

	  case "${FLAVOR}" in
	       xemacs-*)
		 if [ -f /usr/lib/xemacs/mule-packages/lisp/skk/skk.elc ]; then
		   exit
		 fi
	       ;;

	       *)
	       ;;
	  esac

	  if [ -e ${STAMP} ]; then
	    if [ "${VERSION}" = "`cat ${STAMP}`" ]; then
	      echo " exited. (already compiled)" 
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
	  echo ${VERSION} > ${STAMP}

	  install -p -m644 ${ELDIR}/vine-default-${PACKAGE}.el ${ELCDIR}
	  cp -f ${ELDIR}/${STARTFILE} ${STARTDIR}/70${STARTFILE};
	  echo " done."
	;;
esac

exit 0;
