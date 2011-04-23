%define __python /usr/osxws/bin/python
%define modulename dateutil
%bcond_with doc

Summary: provides extensions to the standard datetime module
Name: python-%{modulename}
Version: 1.5
Release: 1%{?_dist_release}
Source0: http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
License: PSF
Group: Development/Languages
URL: http://labix.org/python-dateutil

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-distribute
%if %{with doc}
BuildRequires: python-sphinx
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
The dateutil module provides powerful extensions to the standard datetime module, available in Python 2.3+.
Features
  - Computing of relative deltas (next month, next year, next monday, last week of month, etc);
  - Computing of relative deltas between two given date and/or datetime objects;
  - Computing of dates based on very flexible recurrence rules, using a superset of the
  - iCalendar specification. Parsing of RFC strings is supported as well.
  - Generic parsing of dates in almost any string format;
  - Timezone (tzinfo) implementations for tzfile(5) format files (/etc/localtime, /usr/share/zoneinfo, etc), TZ environment string (in all known formats), iCalendar format files, given ranges (with help from relative deltas), local machine timezone, fixed offset timezone, UTC timezone, and Windows registry-based time zones.
  - Internal up-to-date world timezone information based on Olson's database.
  - Computing of Easter Sunday dates for any given year, using Western, Orthodox or Julian algorithms;
  - More than 400 test cases.

%prep
%setup -q

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
* Fri Apr  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5-1
- replace setuptools with distribute

* Fri Nov 26 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5-0
- initial build for Mac OS X WorkShop 10.6

