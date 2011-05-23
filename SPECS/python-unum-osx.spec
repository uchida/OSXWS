%define __python /usr/osxws/bin/python
%define modulename Unum

Summary: Units in Python
Name: python-%{modulename}
Version: 4.1.1
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/U/Unum/Unum-%{version}.zip
Patch1: Unum-no-ez_setup.patch
License: LGPL
Group: Development/Languages
URL: http://bitbucket.org/kiv/unum/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-distribute
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
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.1.1-0
- initial build for Mac OS X WorkShop 10.6

