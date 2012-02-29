Name: jansson
Version: 2.3
Release: 0%{?_dist_release}
Summary: C library for working with JSON dataColor Management System
Group: Development/Libraries
License: MIT
URL: http://www.digip.org/jansson/
Source0: http://www.digip.org/jansson/releases/jansson-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Jansson is a C library for encoding, decoding and manipulating JSON data. It features:

- Simple and intuitive API and data model
- Comprehensive documentation
- No dependencies on other libraries
- Full Unicode support (UTF-8)
- Extensive test suite

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
%configure
make

pushd doc
make html
popd

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_libdir}/*.*.dylib
%doc CHANGES LICENSE README.rst

%files devel
%defattr(-,root,wheel)
%{_includedir}/*.h
%{_libdir}/*.dylib
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%doc doc/_build/html/*

%changelog
* Mon Feb 20 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.3-0
- update to 2.3

* Thu Feb 16 2012 Akihiro Uchida	<uchida@ike-dyn.ritsumei.ac.jp> 2.2.1-1
- build x86_64 mono arch

* Fri Oct 21 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.2.1-0
- update to 2.2.1

* Fri Jun  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.1-0
- initial build for Mac OS X WorkShop

