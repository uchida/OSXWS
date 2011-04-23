%define alphatag stable

Summary: an event notification library
Summary(ja): イベント通知ライブラリ
Name: libevent
Version: 1.4.14b
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
./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} \
            --bindir=%{_bindir} --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --sharedstatedir=%{_sharedstatedir} \
            --mandir=%{_mandir} --infodir=%{_infodir} \
            CC='gcc-4.2 -arch i386 -arch x86_64' \
            CPP="gcc-4.2 -E"
make

%check
make verify

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
make install-man DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc README CHANGELOG
%{_libdir}/%{name}-*.dylib
%{_libdir}/%{name}_core-*.dylib
%{_libdir}/%{name}_extra-*.dylib

%files devel
%defattr(-,root,wheel)
%{_bindir}/*
%{_includedir}/*
%{_mandir}/man3/*.3*
%{_libdir}/%{name}.dylib
%{_libdir}/%{name}_core.dylib
%{_libdir}/%{name}_extra.dylib
%{_libdir}/%{name}*.a

%changelog
* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.4.14b-0
- initial build for Mac OS X WorkShop

