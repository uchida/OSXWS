%ifos darwin
%define __cpa %{__cp} -RPp
%else
%define __cpa %{__cp} -a
%endif
%define dist hepx
Name:		cmake
Version:	2.8.4
Release:    0%{?_dist_release}
Summary:	Cross-platform make system

Group:		Development/Tools
License:	BSD
URL:		http://www.cmake.org
Source0:	http://www.cmake.org/files/v2.6/cmake-%{version}.tar.gz
Patch0:		cmake-%{version}-macosx10.6.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
%ifnos darwin
BuildRequires:  ncurses-devel, libX11-devel
BuildRequires:  curl-devel, expat-devel, xmlrpc-c-devel, zlib-devel
%else
BuildArch: fat
%endif
Requires:       rpm


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, pre-processor 
generation, code generation, and template instantiation.


%prep
%setup -q
%patch0 -p1 -b .macosx

%build
%ifnos darwin
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%else
export CC="/usr/bin/gcc-4.2"
export CXX="/usr/bin/g++-4.2"
export CFLAGS="-arch i386 -arch x86_64"
export CXXFLAGS="-arch i386 -arch x86_64"
%endif
./bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
            --docdir=/share/doc/%{name}-%{version} --mandir=/share/man
%ifnos darwin
make VERBOSE=1 %{?_smp_mflags}
%else
make VERBOSE=1
%endif


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
%{__cpa} Example $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%ifos darwin
%defattr(-,root,wheel,-)
%else
%defattr(-,root,root,-)
%endif
%{_datadir}/doc/%{name}-%{version}/
%{_bindir}/*
%{_datadir}/%{name}/
%{_mandir}/man1/*.1*


%changelog
* Thu Apr 28 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.8.4-0
- update to 2.8.4
- support intel universal binary (i386, x86_64)

* Sun Mar 21 2010 Keisuke Fujii <keisuke.fujii@kek.jp> - 2.8.0-10.6hepx1c
- 2nd build on MacOSX
- modified macosx10.6 patch to default to -flat_namespace

* Mon Mar 08 2010 Keisuke Fujii <keisuke.fujii@kek.jp> - 2.8.0-10.6hepx1b
- 1st build on MacOSX

* Fri Mar 20 2009 Keisuke Fujii <keisuke.fujii@kek.jp> - 2.6.2-10.5hepx1b
- 2nd build on MacOSX
- Applied a patch to add '-single_module -undefined dynamic_lookup' to link flags

* Mon Feb 23 2009 Keisuke Fujii <keisuke.fujii@kek.jp> - 2.6.2-10.5hepx1a
- 1st build on MacOSX
