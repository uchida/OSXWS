Name: lcms
Summary: Little CMS - color management engine
Summary(ja): Little CMS - カラーマネージメントエンジン
Version: 1.19
Release: 2%{?_dist_release}

Group: System Environment/Libraries
License: MIT
URL: http://www.littlecms.com/

Source0: http://www.littlecms.com/%{name}-%{version}.tar.gz
Patch0: lcms-1.19-rhbz675186.patch
Patch100: lcms-1.18_cmsxfrom_CVE-2009-0793.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: zlib-devel
BuildRequires: libtiff-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig
%if "%{?_dist_release}" == "osx10.6"
BuildRequires: python-devel > 2.6.1
%else
BuildRequires: python-devel
%endif
BuildArch: fat

%description
Little cms intends to be a small-footprint, speed optimized color management
engine in open source form.

%package devel
Summary: Header files and library for development with LCMS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files for development with LCMS

%package utils
Summary: Additional Command Line Utilities for littlecms
Group: Applications/Graphics
Requires: %{name} = %{version}-%{release}

%description utils
Command line utilities which can perform icc transforms and provide info 
about icc profiles.

%package -n python-%{name}
Summary: Python interface to LittleCMS
Group: Development/Libraries
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
%else
Requires: python
%endif
%description -n python-%{name}
Python interface to LittleCMS.

%prep
%setup -q -c %{name}-%{version}
pushd %{name}-%{version}
%patch100 -p1 -b .CVE-2009-0793
pushd samples
%patch0 -p0
popd

find . -name \*.[ch] | xargs chmod -x
chmod 0644 AUTHORS COPYING ChangeLog NEWS README.1ST doc/TUTORIAL.TXT doc/LCMSAPI.TXT

# Convert not UTF-8 files
pushd doc
mkdir -p __temp
for f in LCMSAPI.TXT TUTORIAL.TXT ;do
cp -p $f __temp/$f
iconv -f ISO-8859-1 -t UTF-8 __temp/$f > $f
touch -r __temp/$f $f
done
rm -rf __temp
popd

popd

mv %{name}-%{version} INTEL
cp -Rp  INTEL X86_64

%build
pushd INTEL
export CFLAGS="-O3 -arch i386 -mtune=pentium-m"
export CXXFLAGS="$CFLAGS" \
%configure --with-python --disable-static \
           --host=%{_rpm_platform32} \
           --build=%{_rpm_platform32} \
           --target=%{_rpm_platform32}
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
pushd python
./swig_lcms
popd
make
popd

pushd X86_64
export CFLAGS="-O3 -arch x86_64 -mtune=core2"
export CXXFLAGS="$CFLAGS" \
%configure --with-python --disable-static \
           --host=%{_rpm_platform64} \
           --build=%{_rpm_platform64} \
           --target=%{_rpm_platform64}
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
pushd python
./swig_lcms
popd
make
cp -fRP README.1ST AUTHORS COPYING NEWS ..
cp -fRP doc/TUTORIAL.TXT doc/LCMSAPI.TXT ..
popd

%install
rm -rf $RPM_BUILD_ROOT
PWD=`pwd`
for arch in INTEL X86_64; do
    pushd $arch
    rm -rf ${PWD}-root
    make install DESTDIR=${PWD}-root INSTALL="install -p"
    popd
done

## Make Universal Binaries
filelist=$(find ./INTEL-root -type f | xargs file | sed -e 's,^\./INTEL-root/,,g' | \
        grep -E \(Mach-O\)\|\(ar\ archive\) |sed -e 's,:.*,,g' -e '/\for\ architecture/d')
for i in $filelist; do
    /usr/bin/lipo -create INTEL-root/$i X86_64-root/$i -output `basename $i`
    cp -f `basename $i` INTEL-root/$i
done

# check header files
for i in `find INTEL-root -name "*.h" -type f`; do
    TARGET=`echo $i | sed -e "s,.*INTEL-root,,"`
    TEMP=`diff -u INTEL-root/$TARGET X86_64-root/$TARGET > /dev/null || echo different`
    if [ -n "$TEMP" ]; then
        mv X86_64-root/$TARGET INTEL-root/${TARGET%.*}-x86_64.h
        mv INTEL-root/$TARGET INTEL-root/${TARGET%.*}-i386.h
        FILE=${TARGET##*/}
        FILE=${FILE%.*}
        cat <<EOF > INTEL-root/$TARGET
#if defined (__i386__)
#include "${FILE}-i386.h"
#elif defined( __x86_64__ )
#include "${FILE}-x86_64.h"
#endif
EOF
    fi
done

# install
mkdir -p %{buildroot}
tar cf - -C INTEL-root . | tar xpf - -C %{buildroot}

# remove extraneous
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,wheel)
%doc AUTHORS COPYING ChangeLog README.1ST TUTORIAL.TXT NEWS
%{_libdir}/*.*.dylib

%files devel
%defattr(-,root,wheel)
%{_includedir}/*
%{_libdir}/*.dylib
%{_libdir}/pkgconfig/lcms.pc
%doc LCMSAPI.TXT doc/ 

%files utils
%defattr(-,root,wheel)
%{_bindir}/*
%{_mandir}/man1/*

%files -n python-%{name}
%defattr(-,root,wheel)
%{python_sitearch}/lcms.py*
%{python_sitearch}/_lcms.so

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.19-2
- mofify python requirements for OSXWS

* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.19-1
- make more compatible with Vine Linux

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.19-0
- initial build for Mac OS X WorkShop


