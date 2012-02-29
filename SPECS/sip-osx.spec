Name:        sip
Summary:     SIP - Python/C++ Bindings Generator
Summary(ja): Python/C++ インターフェイス生成ツール
Version:     4.13.2
Release:     0%{?_dist_release}

License:     GPL
Group:       Development/Tools
URL:         http://www.riverbankcomputing.co.uk/software/sip/intro
Source:      http://www.riverbankcomputing.co.uk/static/Downloads/sip4/%{name}-%{version}.tar.gz
Patch0:      sip-4.13.2-fix-defaultbindir.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
Provides: python-sip = %{version}-%{release}
Obsoletes: python-sip

%description
SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python bindings for any C++
class library.


%package devel
Summary:     Files needed to generate Python bindings for any C++ class library
Summary(ja): Python/C++ インタフェース作成に必要なライブラリやヘッダファイル
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
%if "%{?_dist_release}" == "osx10.6"
Requires: python-devel > 2.6.1
%else
Requires: python-devel
%endif
Provides:    libsip-devel = %{version}-%{release}

%description devel
This package contains files needed to generate Python bindings for any C++
classes library.


%prep
%setup -q
%patch0 -p1

%build
python configure.py -d %{python_sitearch} \
    -b %{_bindir} \
    -e %{_includedir} \
    -v %{_datadir}/%{name} \
    CC='/usr/bin/gcc' \
    CXX='/usr/bin/g++' \
    --arch x86_64 \
    --deployment-target 10.5
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT 

install sipconfig.pyc $RPM_BUILD_ROOT%{python_sitearch}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sip

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel,755)
%doc LICENSE LICENSE-GPL2 LICENSE-GPL3 NEWS README 
%doc doc/html
%{_bindir}/sip
%{python_sitearch}/*

%files devel
%defattr(-,root,wheel,755)
%{_includedir}/sip.h
%dir %{_datadir}/sip

%changelog
* Sat Feb 18 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.13.2-0
- update to 4.13.2
- build x86_64 mono arch

* Fri Oct 21 2011 Akihiro Uchida	<uchida@ike-dyn.ritsumei.ac.jp> 4.12.4-0
- update to 4.12.4

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.12.1-3
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.12.1-2
- fix build section

* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.12.1-1
- make more compatible with Vine Linux

* Sun May  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.12.1-0
- initial build for Mac OS X

