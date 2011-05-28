%define alphatag stable

Summary: an event notification library
Summary(ja): イベント通知ライブラリ
Name: libevent
Version: 2.0.11
Release: 0%{?_dist_release}
Source0: http://www.monkey.org/~provos/%{name}-%{version}-%{alphatag}.tar.gz
License: BSD
Group: System Environment/Libraries
URL: http://tmux.sourceforge.net/

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
The libevent API provides a mechanism to execute a callback function when a specific event occurs on a file descriptor or after a timeout has been reached.
Furthermore, libevent also support callbacks due to signals or regular timeouts.
libevent is meant to replace the event loop found in event driven network servers.
An application just needs to call event_dispatch() and then add or remove events dynamically without having to change the event loop.

%package devel
Summary: The development libraries and header files for libevent
Summary(ja): libevent 開発ライブラリ、ヘッダファイル
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n %{name}-%{version}-%{alphatag}

%build
export CFLAGS='-arch i386 -arch x86_64'
export LDFLAGS='-arch i386 -arch x86_64'
%configure CC='/usr/bin/gcc-4.2 -arch i386 -arch x86_64' CPP='/usr/bin/gcc-4.2 -E'
make

%check
make verify

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

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
%{_libdir}/%{name}*.a
%{_libdir}/pkgconfig/%{name}*.pc

%changelog
* Thu May 19 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.11-0
- update to 2.0.11

* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.4.14b-0
- initial build for Mac OS X WorkShop

