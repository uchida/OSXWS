%define alphatag stable

Summary:        Abstract asynchronous event notification library
Summary(ja):	非同期イベント通知ライブラリ
Name:           libevent
Version:        2.0.11
Release:        2%{?_dist_release}
Group:          System Environment/Libraries
License:        BSD
URL:            http://monkey.org/~provos/libevent/
Source0:        http://www.monkey.org/~provos/%{name}-%{version}-%{alphatag}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildArch:      fat
BuildRequires:	openssl-devel

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(ja): libevent 開発ライブラリ、ヘッダファイル、ドキュメント
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},

%prep
%setup -q -c %{name}-%{version}-%{alphatag}

mv %{name}-%{version}-%{alphatag} INTEL
cp -Rp  INTEL X86_64

%build
pushd INTEL
export CFLAGS="-O3 -arch i386 -mtune=pentium-m"
export CXXFLAGS="$CFLAGS" \
%configure \
           --host=%{_rpm_platform32} \
           --build=%{_rpm_platform32} \
           --target=%{_rpm_platform32} \
           --disable-static \
           --disable-dependency-tracking
make
popd

pushd X86_64
export CFLAGS="-O3 -arch x86_64 -mtune=core2"
export CXXFLAGS="$CFLAGS" \
%configure \
           --host=%{_rpm_platform64} \
           --build=%{_rpm_platform64} \
           --target=%{_rpm_platform64} \
           --disable-static \
           --disable-dependency-tracking
make
cp -fRP README CHANGELOG ..
popd

%check
for arch in INTEL X86_64; do
    pushd $arch
    make verify
    popd
done

%install
rm -rf $RPM_BUILD_ROOT

PWD=`pwd`
for arch in INTEL X86_64; do
    pushd $arch
    rm -rf ${PWD}-root
    make install DESTDIR=${PWD}-root
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
tar cf - -C INTEL-root . | tar xpf - -C $RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc README CHANGELOG
%{_libdir}/%{name}-*.dylib
%{_libdir}/%{name}_core-*.dylib
%{_libdir}/%{name}_extra-*.dylib
%{_libdir}/%{name}_pthreads-*.dylib
%{_libdir}/%{name}_openssl-*.dylib

%files devel
%defattr(-,root,wheel)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/%{name}.dylib
%{_libdir}/%{name}_core.dylib
%{_libdir}/%{name}_extra.dylib
%{_libdir}/%{name}_openssl.dylib
%{_libdir}/%{name}_pthreads.dylib
%{_libdir}/pkgconfig/%{name}*.pc
%doc INTEL/sample/*.c

%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.11-2
- make more compatible with Vine Linux

* Sat May 28 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.11-1
- make libevent headers architecture-independent

* Thu May 19 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.11-0
- update to 2.0.11

* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.4.14b-0
- initial build for Mac OS X WorkShop

