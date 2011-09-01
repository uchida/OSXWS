%define modulename pytz

Summary: World timezone definitions, modern and historical of python
Summary(ja): Python 版の世界同時帯の現代的、歴史的な定義
Name: python-%{modulename}
Version: 2010l
Release: 3%{?_dist_release}
Source0: http://pypi.python.org/packages/source/p/pytz/pytz-%{version}.tar.gz
License: MIT
Group: Development/Languages
URL: http://pytz.sourceforge.net

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
pytz brings the Olson tz database into Python. This library allows accurate and cross platform timezone calculations using Python 2.3 or higher. It also solves the issue of ambiguous times at the end of daylight savings, which you can read more about in the Python Library Reference (datetime.tzinfo).

Amost all of the Olson timezones are supported.

Note that this library differs from the documented Python API for tzinfo implementations; if you want to create local wallclock times you need to use the localize() method documented in this document. In addition, if you perform date arithmetic on local times that cross DST boundaries, the results may be in an incorrect timezone (ie. subtract 1 minute from 2002-10-27 1:00 EST and you get 2002-10-27 0:59 EST instead of the correct 2002-10-27 1:59 EDT). A normalize() method is provided to correct this. Unfortunatly these issues cannot be resolved without modifying the Python datetime implementation.

%prep
%setup -q -n %{modulename}-%{version}

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
%doc CHANGES.txt LICENSE.txt README.txt

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2010l-3
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2010l-2
- remove unnecessary requires

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2010l-1
- fix type in Group

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2010l-0
- initial build for Mac OS X WorkShop 10.6

