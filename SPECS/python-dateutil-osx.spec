%define modulename dateutil
%bcond_with doc

Name:           python-dateutil
Version:        1.5
Release:        2%{?_dist_release}
Summary:        Powerful extensions to the standard datetime module

Group:          Development/Languages
License:        PSF
URL:            http://labix.org/python-dateutil
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
%if %{with doc}
BuildRequires: python-sphinx
%endif

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

%prep
%setup -q

# Reencode this as utf8
iconv -f ISO-8859-1 -t utf8 NEWS

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
%doc LICENSE NEWS README

%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5-2
- make more compatible with Vine Linux

* Fri Apr  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5-1
- replace setuptools with distribute

* Fri Nov 26 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5-0
- initial build for Mac OS X WorkShop 10.6

