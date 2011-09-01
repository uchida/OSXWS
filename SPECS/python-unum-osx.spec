%define modulename Unum

Summary: Units in Python
Name: python-%{modulename}
Version: 4.1.1
Release: 3%{?_dist_release}
Source0: http://pypi.python.org/packages/source/U/Unum/Unum-%{version}.zip
Patch1: Unum-no-ez_setup.patch
License: LGPL
Group: Development/Languages
URL: http://bitbucket.org/kiv/unum/

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires: python-setuptools
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description

%prep
%setup -q -n %{modulename}-%{version}
%patch1 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc README.txt

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.1.1-3
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.1.1-2
- remove unnecessary requires

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.1.1-1
- requires python-setuptools

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.1.1-0
- initial build for Mac OS X WorkShop 10.6

