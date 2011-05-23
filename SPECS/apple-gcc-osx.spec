%define apple_version 5666.3
%define gcc_version 4.2.1
%define major_version 4.2
%define gcc_target_platform i686-apple-darwin10

Summary: Apple's version of gcc with gfortran
Name: apple-gcc
Version: %{apple_version}.gf
Release: 1%{?_dist_release}
Source0: http://www.opensource.apple.com/tarballs/gcc/gcc-%{apple_version}.tar.gz
Source1: http://ftp.gnu.org/gnu/gcc/gcc-%{gcc_version}/gcc-fortran-%{gcc_version}.tar.gz
Patch0: apple-gcc-fortran.patch
Patch1: apple-gcc-disable-chgrp.patch
Patch2: apple-gcc-disable-lipo.patch
Patch3: apple-gcc-include-mac-cxx.patch
Patch4: apple-gcc-osxws.patch
License: GPLv2
Group: Development
URL: http://gcc.gnu.org/

Requires(post): alternatives
Requires(postun): alternatives
Requires: alternatives
Requires: OSX-system
BuildRequires: mpfr-devel gmp-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
Apple's version of the GNU compiler collection,
supports C, C++ and Objective-C.
In addition, this package include GNU Fortran compiler
which has universal compiler integration recognize '-arch' option.

%prep
%setup -q -c -a 1
tar cf - -C gcc-%{gcc_version} . | tar xpf - -C gcc-%{apple_version}
rm -rf gcc-%{gcc_version}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%build
if [ -f /usr/include/mach/vm_types.h ]; then
  cat<<EOF
==============================================================================
NOTICE: The definition of a type pointer_t in "/usr/include/mach/vm_types.h"
        conflicts one in the gcc fortran source "gcc/fortran/module.c".
        Therefore rename the system header when you build this package.
==============================================================================
EOF
  exit 1
fi
pushd gcc-%{apple_version}
mkdir -p build/dst build/sym
./build_gcc "i386 x86_64" "i686 x86_64" \
            "`pwd`" "%{_prefix}" "`pwd`/build/dst" "`pwd`/build/sym"
ditto build/dst dst
./build_libgcc "i386 x86_64" "i386 x86_64" \
               "`pwd`" "%{_prefix}" "`pwd`/build/dst"
ditto dst-i686-i686%{_libdir}/libg{fortran,omp}*.dylib build/dst%{_libdir}
mkdir -p build/dst/%{_libdir}/x86_64
ditto dst-i686-i686%{_libdir}/x86_64 build/dst%{_libdir}/x86_64
ditto build/dst dst
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd gcc-%{apple_version}
ditto dst $RPM_BUILD_ROOT/
cp -pf README ChangeLog COPYING COPYING.LIB ../
cp -pf README.Apple ChangeLog.apple CHANGES.Apple ../
mkdir -p ../gfortran
cp -pf gcc/fortran/ChangeLog ../gfortran
mkdir -p ../libgfortran
cp -pf libgfortran/ChangeLog ../libgfortran
popd
rm -rf $RPM_BUILD_ROOT/Developer
rm -f $RPM_BUILD_ROOT%{_libdir}/{,x86_64/}*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/{,x86_64/}*.la
# for alternatives
pushd $RPM_BUILD_ROOT%{_bindir}
    for bin in gcc g++ cpp gfortran; do
        mv -f %{gcc_target_platform}-$bin-%{gcc_version} %{gcc_target_platform}-$bin-%{gcc_version}-osxws
    done
popd
pushd $RPM_BUILD_ROOT%{_libdir}
  for lib in libgcc_s.*.dylib libgfortran*.dylib libgomp*.dylib; do
      mv -f "$lib" "$lib"-%{gcc_version}
  done
popd
pushd $RPM_BUILD_ROOT%{_libdir}/x86_64
  for lib in lib*; do
      mv -f "$lib" "$lib"-%{gcc_version}
  done
popd

find %{buildroot} -type f > list.f
find %{buildroot} -type l > list.l
sed -e "s;%{buildroot};;" list.f > list.new
mv list.new list.f
sed -e "s,%{buildroot},," list.l > list.new
mv list.new list.l
cat list.l >> list.f
cat list.f | sed -e 's;\(%{_mandir}/.*/.*\..*\);\1*;' \
	         -e 's;\(%{_infodir}/.*\..*\);\1*;' > list.new
mv list.new list.f

%clean
rm -rf $RPM_BUILD_ROOT

%post
# this package (default)
%{_sbindir}/update-alternatives \
  --install %{_bindir}/gcc gcc %{_bindir}/gcc-%{major_version} 26 \
  --slave   %{_bindir}/cc cc %{_bindir}/gcc-%{major_version} \
  --slave   %{_bindir}/g++ g++ %{_bindir}/g++-%{major_version} \
  --slave   %{_bindir}/c++ c++ %{_bindir}/g++-%{major_version} \
  --slave   %{_bindir}/cpp cpp %{_bindir}/cpp-%{major_version} \
  --slave   %{_bindir}/gfortran gfortran %{_bindir}/gfortran-%{major_version} \
  --slave   %{_bindir}/gcov gcov %{_bindir}/gcov-%{major_version} \
  --slave   %{_bindir}/%{gcc_target_platform}-gcc-%{gcc_version} \
              %{gcc_target_platform}-gcc-%{gcc_version} \
              %{_bindir}/%{gcc_target_platform}-gcc-%{gcc_version}-osxws \
  --slave   %{_bindir}/%{gcc_target_platform}-g++-%{gcc_version} \
              %{gcc_target_platform}-g++-%{gcc_version} \
              %{_bindir}/%{gcc_target_platform}-g++-%{gcc_version}-osxws \
  --slave   %{_bindir}/%{gcc_target_platform}-cpp-%{gcc_version} \
              %{gcc_target_platform}-cpp-%{gcc_version} \
              %{_bindir}/%{gcc_target_platform}-cpp-%{gcc_version}-osxws \
  --slave   %{_bindir}/%{gcc_target_platform}-gfortran-%{gcc_version} \
              %{gcc_target_platform}-gfortran-%{gcc_version} \
              %{_bindir}/%{gcc_target_platform}-gfortran-%{gcc_version}-osxws \
  --slave   %{_libdir}/libgcc_s.1.dylib libgcc_s.1.dylib \
              %{_libdir}/libgcc_s.1.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgcc_s.10.4.dylib libgcc_s.10.4.dylib \
              %{_libdir}/libgcc_s.10.4.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgcc_s.10.5.dylib libgcc_s.10.5.dylib \
              %{_libdir}/libgcc_s.10.5.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgfortran.2.0.0.dylib libgfortran.2.0.0.dylib \
              %{_libdir}/libgfortran.2.0.0.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgfortran.2.dylib libgfortran.2.dylib \
              %{_libdir}/libgfortran.2.0.0.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgfortran.dylib libgfortran.dylib \
              %{_libdir}/libgfortran.2.0.0.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgomp.1.0.0.dylib libgomp.1.0.0.dylib \
              %{_libdir}/libgomp.1.0.0.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgomp.1.dylib libgomp.1.dylib \
              %{_libdir}/libgomp.1.dylib-%{gcc_version} \
  --slave   %{_libdir}/libgomp.dylib libgomp.dylib \
              %{_libdir}/libgomp.dylib-%{gcc_version} \
  --slave   %{_libdir}/libstdc++.6.dylib libstdc++.6.dylib \
              /usr/lib/libstdc++.6.dylib
# Apple 4.0.1
%{_sbindir}/update-alternatives \
  --install %{_bindir}/gcc gcc /usr/bin/gcc-4.0 20 \
  --slave   %{_bindir}/cc  cc  /usr/bin/gcc-4.0 \
  --slave   %{_bindir}/powerpc-apple-darwin10-gcc-4.0.1 \
              powerpc-apple-darwin10-gcc-4.0.1 \
              /usr/bin/powerpc-apple-darwin10-gcc-4.0.1 \
  --slave   %{_bindir}/%{gcc_target_platform}-gcc-4.0.1 \
              %{gcc_target_platform}-gcc-4.0.1 \
              /usr/bin/%{gcc_target_platform}-gcc-4.0.1 \
  --slave   %{_bindir}/g++ g++ /usr/bin/g++-4.0 \
  --slave   %{_bindir}/c++ c++ /usr/bin/g++-4.0 \
  --slave   %{_bindir}/powerpc-apple-darwin10-g++-4.0.1 \
              powerpc-apple-darwin10-g++-4.0.1 \
              /usr/bin/powerpc-apple-darwin10-g++-4.0.1 \
  --slave   %{_bindir}/%{gcc_target_platform}-g++-4.0.1 \
              %{gcc_target_platform}-g++-4.0.1 \
              /usr/bin/%{gcc_target_platform}-g++-4.0.1 \
  --slave   %{_bindir}/cpp cpp /usr/bin/cpp-4.0 \
  --slave   %{_bindir}/gcov gcov /usr/bin/gcov-4.0 \
  --slave   %{_libdir}/libgcc_s.1.dylib libgcc_s.1.dylib \
              /usr/lib/libgcc_s.1.dylib \
  --slave   %{_libdir}/libgcc_s.10.4.dylib libgcc_s.10.4.dylib \
              /usr/lib/libgcc_s.10.4.dylib \
  --slave   %{_libdir}/libgcc_s.10.5.dylib libgcc_s.10.5.dylib \
              /usr/lib/libgcc_s.10.5.dylib \
  --slave   %{_libdir}/libstdc++.6.dylib libstdc++.6.dylib \
              /usr/lib/libstdc++.6.dylib
# Apple 4.2.1
%{_sbindir}/update-alternatives \
  --install %{_bindir}/gcc gcc /usr/bin/gcc-4.2 25 \
  --slave   %{_bindir}/cc  cc  /usr/bin/gcc-4.2 \
  --slave   %{_bindir}/powerpc-apple-darwin10-gcc-4.2.1 \
              powerpc-apple-darwin10-gcc-4.2.1 \
              /usr/bin/powerpc-apple-darwin10-gcc-4.2.1 \
  --slave   %{_bindir}/%{gcc_target_platform}-gcc-4.2.1 \
              %{gcc_target_platform}-gcc-4.2.1 \
              /usr/bin/%{gcc_target_platform}-gcc-4.2.1 \
  --slave   %{_bindir}/g++ g++ /usr/bin/g++-4.2 \
  --slave   %{_bindir}/c++ c++ /usr/bin/g++-4.2 \
  --slave   %{_bindir}/powerpc-apple-darwin10-g++-4.2.1 \
              powerpc-apple-darwin10-g++-4.2.1 \
              /usr/bin/powerpc-apple-darwin10-g++-4.2.1 \
  --slave   %{_bindir}/%{gcc_target_platform}-g++-4.2.1 \
              %{gcc_target_platform}-g++-4.2.1 \
              /usr/bin/%{gcc_target_platform}-g++-4.2.1 \
  --slave   %{_bindir}/cpp cpp /usr/bin/cpp-4.2 \
  --slave   %{_bindir}/powerpc-apple-darwin10-cpp-4.2.1 \
              powerpc-apple-darwin10-cpp-4.2.1 \
              /usr/bin/powerpc-apple-darwin10-cpp-4.2.1 \
  --slave   %{_bindir}/%{gcc_target_platform}-cpp-4.2.1 \
              %{gcc_target_platform}-cpp-4.2.1 \
              /usr/bin/%{gcc_target_platform}-cpp-4.2.1 \
  --slave   %{_bindir}/gcov gcov /usr/bin/gcov-4.2 \
  --slave   %{_libdir}/libgcc_s.1.dylib libgcc_s.1.dylib \
              /usr/lib/libgcc_s.1.dylib \
  --slave   %{_libdir}/libgcc_s.10.4.dylib libgcc_s.10.4.dylib \
              /usr/lib/libgcc_s.10.4.dylib \
  --slave   %{_libdir}/libgcc_s.10.5.dylib libgcc_s.10.5.dylib \
              /usr/lib/libgcc_s.10.5.dylib \
  --slave   %{_libdir}/libstdc++.6.dylib libstdc++.6.dylib \
              /usr/lib/libstdc++.6.dylib
# fix broken symlink if it's there
if [ ! -f %{_bindir}/gcc ] ; then
  echo "%{_sbindir}/update-alternatives --auto gcc"
  %{_sbindir}/update-alternatives --auto gcc
fi

%postun
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove gcc %{_bindir}/gcc-%{major_version}
  %{_sbindir}/update-alternatives --auto gcc
fi

%triggerpostun -- gcc < %{version}-%{release}
%{_sbindir}/update-alternatives --auto gcc

%files -f list.f
%defattr(-,root,wheel)
%doc README ChangeLog COPYING COPYING.LIB
%doc README.Apple ChangeLog.apple CHANGES.Apple
%doc gfortran/ChangeLog libgfortran/ChangeLog

%changelog
* Mon Apr 25 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5666.3.gf-1
- fix the filename problem with update-alternatives

* Sun Apr  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5666.3.gf-0
- update to Apple build 5666.3

* Sun Feb  6 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5664.gf-1
- modified gcc version and bug report url for Mac OS X WorkShop

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5664.gf-0
- initial build for Mac OS X WorkShop

