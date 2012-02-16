%define alphatag stable

Summary:        Abstract asynchronous event notification library
Summary(ja):	非同期イベント通知ライブラリ
Name:           libevent
Version:        2.0.15
Release:        0%{?_dist_release}
Group:          System Environment/Libraries
License:        BSD
URL:            http://monkey.org/~provos/libevent/
Source0:        http://www.monkey.org/~provos/%{name}-%{version}-%{alphatag}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-root
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
%setup -q -n %{name}-%{version}-%{alphatag}

%build
%configure --disable-static \
           --disable-dependency-tracking
make

%check
make verify

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}*.la

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
* Thu Feb 16 2012 Akihiro Uchida	<uchida@ike-dyn.ritsumei.ac.jp> 2.0.15-1
- build x86_64 mono arch

* Fri Oct 21 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.15-0
- update to 2.0.15

* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.11-2
- make more compatible with Vine Linux

* Sat May 28 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.11-1
- make libevent headers architecture-independent

* Thu May 19 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.11-0
- update to 2.0.11

* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.4.14b-0
- initial build for Mac OS X WorkShop

