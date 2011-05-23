Summary: GNU Troff
Name: groff
Version: 1.18.1.1
Release: 0%{?_dist_release}
Source0: http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1: groff-man.conf.osxws
Patch0: http://ftp.debian.org/debian/pool/main/g/groff/groff_1.18.1.1-21.diff.gz
Patch1: groff-1.18.1.1-info.patch
License: GPLv2
Group: System Environment/Libraries
URL: http://www.libgd.org/

Requires: libpng libjpeg freetype zlib
BuildRequires: libpng-devel libjpeg-devel freetype-devel zlib-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
The groff (GNU troff) software is a typesetting package which reads plain text mixed with formatting commands and produces formatted output.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%build
export LDFLAGS='-liconv'
./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} \
            --bindir=%{_bindir} --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --sharedstatedir=%{_sharedstatedir} \
            --mandir=%{_mandir} --infodir=%{_infodir} \
            --without-x \
            --enable-multibyte \
            CC='gcc-4.2 -arch i386 -arch x86_64' \
            CXX='g++-4.2 -arch i386 -arch x86_64' \
            CPP='gcc-4.2 -E'
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}
%makeinstall
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/man.conf
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
install-info %{_infodir}/groff.info %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
  install-info --delete %{_infodir}/groff.info %{_infodir}/dir
fi

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{_libdir}/groff
%{_sysconfdir}/man.conf
%{_sharedstatedir}/groff
%{_sharedstatedir}/doc/groff/*
%{_mandir}/man?/*.?*
%{_infodir}/groff*
%doc COPYING FDL
%doc INSTALL INSTALL.gen README README.jp
%doc MORE.STUFF NEWS TODO TODO.jp VERSION
%doc ChangeLog ChangeLog.jp PROBLEMS

%changelog
* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.18.1.1-0
- initial build for Mac OS X WorkShop

