%global oname virtualenv

Summary:        Tool to create isolated Python environments
Summary(ja):    隔離されたPython環境を構築するためのツール
Name:           python-%{oname}
Version:        1.6.1
Release:        2%{?_dist_release}

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/%{oname}
Source0:        http://pypi.python.org/packages/source/v/%{oname}/%{oname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif

BuildRequires:  python-setuptools
Requires:       python-setuptools


%description
virtualenv is a tool to create isolated Python environments. virtualenv
is a successor to workingenv, and an extension of virtual-python. It is
written by Ian Bicking, and sponsored by the Open Planning Project. It is
licensed under an MIT-style permissive license.


%prep
%setup -q -n %{oname}-%{version}
sed -i.tmp -e "1s|#!/usr/bin/env python||" virtualenv.py 
rm -f virtualenv.py.tmp

%build
python setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc docs/*.txt
# For noarch packages: sitelib
%{python_sitelib}/*
%attr(755,root,root) %{_bindir}/virtualenv

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.6.1-2
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.6.1-1
- make more compatible with Vine Linux

* Thu May  5 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.6.1-0
- update to 1.6.1

* Sun Apr  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5.2-0
- initial build for Mac OS X WorkShop

