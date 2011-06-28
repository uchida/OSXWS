%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: lcms
Version: 1.19
Release: 0%{?_dist_release}
Summary: Color Management System
Group: Applications/Productivity
License: MIT
URL: http://www.littlecms.com/
Source0: http://www.littlecms.com/lcms-%{version}.tar.gz
Patch0: lcms-1.19-rhbz675186.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: fat
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig
BuildRequires: python-devel
BuildRequires: zlib-devel
Requires: %{name}-libs = %{version}-%{release}
%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form.

%package libs
Summary: Library for %{name}
Group: System Environment/Libraries
%description libs
The %{name}-libs package contains library for %{name}.

%package -n python-%{name}
Summary: Python interface to LittleCMS
Group: Development/Libraries
Requires: python
%description -n python-%{name}
Python interface to LittleCMS.

%package devel
Summary: Development files for LittleCMS
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
%description devel
Development files for LittleCMS.


%prep
%setup -q -c %{name}-%{version}
pushd %{name}-%{version}
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
%defattr(-,root,root,-)
%doc README.1ST TUTORIAL.TXT
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_libdir}/*.*.dylib

%files devel
%defattr(-,root,root,-)
%doc LCMSAPI.TXT
%{_includedir}/*
%{_libdir}/*.dylib
%{_libdir}/pkgconfig/%{name}.pc

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/lcms.py*
%{python_sitearch}/_lcms.so


%changelog
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp>
- initial build for Mac OS X WorkShop

