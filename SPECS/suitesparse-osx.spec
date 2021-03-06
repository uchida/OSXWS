Name: suitesparse
Version: 3.4.0
Release: 3%{?_dist_release}
Summary: A collection of sparse matrix libraries

Group: System Environment/Libraries
License: GPLv2+ and LGPLv2+
URL: http://www.cise.ufl.edu/research/sparse/SuiteSparse
Source0: http://www.cise.ufl.edu/research/sparse/%{name}/%{name}-%{version}.tar.gz
Patch0: SuiteSparse-UFconfig.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
suitesparse is a collection of libraries for computations involving sparse
matrices.  The package includes the following libraries:
  AMD         approximate minimum degree ordering
  BTF         permutation to block triangular form (beta)
  CAMD        constrained approximate minimum degree ordering
  COLAMD      column approximate minimum degree ordering
  CCOLAMD     constrained column approximate minimum degree ordering
  CHOLMOD     sparse Cholesky factorization
  CSparse     a concise sparse matrix package
  CXSparse    CSparse extended: complex matrix, int and long int support
  KLU         sparse LU factorization, primarily for circuit simulation
  LDL         a simple LDL' factorization
  SQPR        a multithread, multifrontal, rank-revealing sparse QR
              factorization method
  UMFPACK     sparse LU factorization
  UFconfig    configuration file for all the above packages.


%package devel
Summary: headers for SuiteSparse
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The suitesparse-devel package contains files needed for developing
applications which use the suitesparse libraries.


%package static
Summary: Static version of SuiteSparse libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The suitesparse-static package contains the statically linkable
version of the suitesparse libraries.

%package doc
Summary: Documentation files for SuiteSparse
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.


%prep
%setup -q -n SuiteSparse
%patch0 -p1

%build
%define amd_version 2.2.0
%define amd_version_major 2
%define btf_version 1.1.0
%define btf_version_major 1
%define camd_version 2.2.0
%define camd_version_major 2
%define ccolamd_version 2.7.1
%define ccolamd_version_major 2
%define cholmod_version 1.7.1
%define cholmod_version_major 1
%define colamd_version 2.7.1
%define colamd_version_major 2
%define csparse_version 2.2.3
%define csparse_version_major 2
%define cxsparse_version 2.2.3
%define cxsparse_version_major 2
%define klu_version 1.1.0
%define klu_version_major 1
%define ldl_version 2.0.1
%define ldl_version_major 2
%define umfpack_version 5.4.0
%define umfpack_version_major 5
%define spqr_version 1.1.2
%define spqr_version_major 1
### CHOLMOD can also be compiled to use the METIS library, but it is not
### used here because its licensing terms exclude it from Fedora Extras.
### To compile with METIS, define enable_metis as 1 below.
%define enable_metis 0
### CXSparse is a superset of CSparse, and the two share common header
### names, so it does not make sense to build both. CXSparse is built
### by default, but CSparse can be built instead by defining
### enable_csparse as 1 below.
%define enable_csparse 0

mkdir -p Doc/{AMD,BTF,CAMD,CCOLAMD,CHOLMOD,COLAMD,KLU,LDL,UMFPACK,SPQR} Lib Include

export RPM_OPT_FLAGS="-O2 -arch i386 -arch x86_64 -fasynchronous-unwind-tables -fno-strict-aliasing -fno-schedule-insns2"
pushd AMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libamd.dylib \
        -compatibility_version %{amd_version_major} \
        -current_version %{amd_version} \
        -o libamd.%{amd_version}.dylib \
        ../AMD/Lib/*.o
    ln -sf libamd.%{amd_version}.dylib libamd.%{amd_version_major}.dylib
    ln -sf libamd.%{amd_version}.dylib libamd.dylib
    cp -p ../AMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/License Doc/ChangeLog Doc/*.pdf ../Doc/AMD
popd

pushd BTF
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libbtf.dylib \
        -compatibility_version %{btf_version_major} \
        -current_version %{btf_version} \
        -o libbtf.%{btf_version}.dylib \
        ../BTF/Lib/*.o
    ln -sf libbtf.%{btf_version}.dylib libbtf.%{btf_version_major}.dylib
    ln -sf libbtf.%{btf_version}.dylib libbtf.dylib
    cp -p ../BTF/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/BTF
popd

pushd CAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common" 
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libcamd.dylib \
        -compatibility_version %{camd_version_major} \
        -current_version %{camd_version} \
        -o libcamd.%{camd_version}.dylib \
        ../CAMD/Lib/*.o -lm
    ln -sf libcamd.%{camd_version}.dylib libcamd.%{camd_version_major}.dylib
    ln -sf libcamd.%{camd_version}.dylib libcamd.dylib
    cp -p ../CAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/ChangeLog Doc/License Doc/*.pdf ../Doc/CAMD
popd

pushd CCOLAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common" 
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libccolamd.dylib \
        -compatibility_version %{ccolamd_version_major} \
        -current_version %{ccolamd_version} \
        -o libccolamd.%{ccolamd_version}.dylib \
        ../CCOLAMD/Lib/*.o -lm
    ln -sf libccolamd.%{ccolamd_version}.dylib libccolamd.%{ccolamd_version_major}.dylib
    ln -sf libccolamd.%{ccolamd_version}.dylib libccolamd.dylib
    cp -p ../CCOLAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/CCOLAMD
popd

pushd COLAMD
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libcolamd.dylib \
        -compatibility_version %{colamd_version_major} \
        -current_version %{colamd_version} \
        -o libcolamd.%{colamd_version}.dylib \
        ../COLAMD/Lib/*.o
    ln -sf libcolamd.%{colamd_version}.dylib libcolamd.%{colamd_version_major}.dylib
    ln -sf libcolamd.%{colamd_version}.dylib libcolamd.dylib
    cp -p ../COLAMD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/* ../Doc/COLAMD
popd

%if "%{?enable_metis}" == "1"
CHOLMOD_FLAGS="$RPM_OPT_FLAGS -I%{_includedir}/metis -fno-common"
%else
CHOLMOD_FLAGS="$RPM_OPT_FLAGS -DNPARTITION -fno-common"
%endif
pushd CHOLMOD
  pushd Lib
    make CFLAGS="$CHOLMOD_FLAGS"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libcholmod.dylib \
        -compatibility_version %{cholmod_version_major} \
        -current_version %{cholmod_version} \
        -o libcholmod.%{cholmod_version}.dylib \
        ../CHOLMOD/Lib/*.o \
        -framework Accelerate \
        libamd.%{amd_version_major}.dylib \
        libcamd.%{camd_version_major}.dylib libcolamd.%{colamd_version_major}.dylib \
        libccolamd.%{ccolamd_version_major}.dylib
    ln -sf libcholmod.%{cholmod_version}.dylib libcholmod.%{cholmod_version_major}.dylib
    ln -sf libcholmod.%{cholmod_version}.dylib libcholmod.dylib
    cp -p ../CHOLMOD/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/*.pdf ../Doc/CHOLMOD
  cp -p Cholesky/License.txt ../Doc/CHOLMOD/Cholesky_License.txt
  cp -p Core/License.txt ../Doc/CHOLMOD/Core_License.txt
  cp -p MatrixOps/License.txt ../Doc/CHOLMOD/MatrixOps_License.txt
  cp -p Partition/License.txt ../Doc/CHOLMOD/Partition_License.txt
  cp -p Supernodal/License.txt ../Doc/CHOLMOD/Supernodal_License.txt
popd

%if "%{?enable_csparse}" == "1"
pushd CSparse
  pushd Source
    make CFLAGS="$RPM_OPT_FLAGS -fno-common"
    cp -p cs.h ../../Include
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libcsparse.dylib \
        -compatibility_version %{csparse_version_major} \
        -current_version %{csparse_version} \
        -o libcsparse.%{csparse_version}.dylib \
        ../CSparse/Source/*.o
    ln -sf libcsparse.%{csparse_version}.dylib libcsparse.%{csparse_version_major}.dylib
    ln -sf libcsparse.%{csparse_version}.dylib libcsparse.dylib
    cp -p ../CSparse/Source/*.a ./
  popd
  mkdir ../Doc/CSparse/
  cp -p Doc/* ../Doc/CSparse
popd
%else
pushd CXSparse
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libcxsparse.dylib \
        -compatibility_version %{cxsparse_version_major} \
        -current_version %{cxsparse_version} \
        -o libcxsparse.%{cxsparse_version}.dylib \
        ../CXSparse/Lib/*.o
    ln -sf libcxsparse.%{cxsparse_version}.dylib libcxsparse.%{cxsparse_version_major}.dylib
    ln -sf libcxsparse.%{cxsparse_version}.dylib libcxsparse.dylib
    cp -p ../CXSparse/Lib/*.a ./
  popd
  cp -p Include/cs.h ../Include
  mkdir ../Doc/CXSparse/
  cp -p Doc/* ../Doc/CXSparse
popd
%endif

pushd KLU
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libklu.dylib \
        -compatibility_version %{klu_version_major} \
        -current_version %{klu_version} \
        -o libklu.%{klu_version}.dylib \
        ../KLU/Lib/*.o \
        libamd.%{amd_version_major}.dylib libcolamd.%{colamd_version_major}.dylib \
        libbtf.%{btf_version_major}.dylib libcholmod.%{cholmod_version_major}.dylib
    ln -sf libklu.%{klu_version}.dylib libklu.%{klu_version_major}.dylib
    ln -sf libklu.%{klu_version}.dylib libklu.dylib
    cp -p ../KLU/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/lesser.txt ../Doc/KLU
popd

pushd LDL
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libldl.dylib \
        -compatibility_version %{ldl_version_major} \
        -current_version %{ldl_version} \
        -o libldl.%{ldl_version}.dylib \
        ../LDL/Lib/*.o
    ln -sf libldl.%{ldl_version}.dylib libldl.%{ldl_version_major}.dylib
    ln -sf libldl.%{ldl_version}.dylib libldl.dylib
    cp -p ../LDL/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/ChangeLog Doc/lesser.txt Doc/*.pdf ../Doc/LDL
popd

pushd UMFPACK
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -fno-common" 
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libumfpack.dylib \
        -compatibility_version %{umfpack_version_major} \
        -current_version %{umfpack_version} \
        -o libumfpack.%{umfpack_version}.dylib \
        ../UMFPACK/Lib/*.o \
        -framework Accelerate \
        libamd.%{amd_version_major}.dylib
    ln -sf libumfpack.%{umfpack_version}.dylib libumfpack.%{umfpack_version_major}.dylib
    ln -sf libumfpack.%{umfpack_version}.dylib libumfpack.dylib
    cp -p ../UMFPACK/Lib/*.a ./
  popd
  cp -p Include/*.h ../Include
  cp -p README.txt Doc/License Doc/ChangeLog Doc/gpl.txt Doc/*.pdf ../Doc/UMFPACK
popd

pushd SPQR
  pushd Lib
    make CFLAGS="$RPM_OPT_FLAGS -DNPARTITION -fno-common"
  popd
  pushd ../Lib
    gcc -dynamiclib -arch i386 -arch x86_64 \
        -install_name %{_libdir}/%{name}/libspqr.dylib \
        -compatibility_version %{spqr_version_major} \
        -current_version %{spqr_version} \
        -o libspqr.%{spqr_version}.dylib \
        ../SPQR/Lib/*.o \
        -framework Accelerate \
        -lstdc++ \
        libcholmod.%{cholmod_version_major}.dylib
    ln -sf libspqr.%{spqr_version}.dylib libspqr.%{spqr_version_major}.dylib
    ln -sf libspqr.%{spqr_version}.dylib libspqr.dylib
    cp -p ../SPQR/Lib/*.a ./
  popd
  cp -p Include/*.h* ../Include
  cp -p README{,_SPQR}.txt
  cp -p README_SPQR.txt Doc/* ../Doc/SPQR
popd

cp -p UFconfig/UFconfig.h Include

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
pushd Lib
  for f in *.a *.dylib*; do
    cp -a $f ${RPM_BUILD_ROOT}%{_libdir}/$f
  done
popd
pushd Include
  for f in *.h;  do
    cp -a $f ${RPM_BUILD_ROOT}%{_includedir}/%{name}/$f
  done
popd


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,wheel)
%{_libdir}/lib*.*.dylib

%files devel
%defattr(-,root,wheel)
%{_includedir}/%{name}
%{_libdir}/lib*.dylib

%files static
%defattr(-,root,wheel)
%{_libdir}/lib*.a

%files doc
%defattr(-,root,wheel)
%doc Doc/*

%changelog
* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.0-3
- modified for Mac OS X WorkShop 10.6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 27 2009 Deji Akingunola <dakingun@gmail.com> - 3.4.0-1
- Update to version 3.4.0.

* Tue May 19 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 3.3.0-2
- Split documentation into separate -doc subpackage (resolves BZ#492451).

* Mon Apr 27 2009 Deji Akingunola <dakingun@gmail.com> - 3.3.0-1
- Update to release 3.3.0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Deji Akingunola <dakingun@gmail.com> - 3.2.0-5
- More fixes for the undefined symbol issue (BZ #475411)

* Sat Dec 20 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-4
- Also build SPQR
- Further fixes for BZ #475411

* Wed Dec 17 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-3
- Rearrange the spec
- Link in necessary libs when making shared CHOLMOD lib (BZ #475411)
- Link with ATLAS' blas and lapack libs

* Wed Dec 17 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-2
- Rebuild for updated atlas

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 3.2.0-1
- New upstream version

* Mon Mar  3 2008 Quentin Spencer <qspencer@users.sourceforge.net> 3.1.0-1
- Update to release 3.1.0. 

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.0-4
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-3
- Update license tag. Fix minor issues found by rpmlint.

* Fri Aug 24 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-2
- Rebuild for F8.

* Tue Jul  3 2007 Quentin Spencer <qspencer@users.sourceforge.net> 3.0.0-1
- Change package name to match upstream, including provides and obsoletes.
- New release. Numerous changes in build to reflect source reorganization.
- Moved static libs into separate package.

* Mon Oct 16 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.1-1
- New release, and package name change from UFsparse to SuiteSparse. Fixes
  bug #210846. Keep the ufsparse package name for now.

* Thu Sep  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.0-1
- New release. Increment versions of some libraries.
- Rearrange and clean up spec file so all definitions are in one place.

* Mon Aug  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.0.0-1
- New release.
- Build newly added CAMD library.
- Misc minor spec changes.

* Tue Mar  7 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.2-1
- New release.
- Build newly added library CXSparse (but not CSparse--see comments
  in build section).

* Wed Feb 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 0.93-2
- Rebuild for Fedora Extras 5.

* Thu Feb  9 2006 Quentin Spencer <qspencer@users.sourceforge.net> 0.93-1
- New release. Remove old patch.

* Wed Dec 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.92-2
- Add patch0--fixes LDL/Makefile so CFLAGS are used when compiling ldl.a.

* Wed Dec 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.92-1
- Update to Dec 8 2005 version.

* Tue Oct 25 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.91-2
- Rebuild.

* Tue Oct 18 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.91-1
- New upstream release, incorporating previous patches
- chmod the build directory to ensure all headers are world readable

* Fri Oct 07 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.9-3
- Build cholmod, but disable METIS using -DNPARTITION flag.

* Sat Oct 01 2005 Quentin Spencer <qspencer@users.sourceforge.net> 0.9-2
- Modify description, other modifications for import into FE.
- Add dist tag, cosmetic changes.

* Tue Sep 08 2005 David Bateman <dbateman@free.fr> 0.9-1
- First version.
