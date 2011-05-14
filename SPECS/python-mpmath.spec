%define __python /usr/osxws/bin/python
%define modulename mpmath
%bcond_with doc

Summary: a Python library for arbitrary-precision floating-point arithmetic
Name: python-%{modulename}
Version: 0.16
Release: 1%{?_dist_release}
Source0: http://%{modulename}.googlecode.com/files/%{modulename}-all-%{version}.tar.gz
License: BSD
Group: Development/Languages
URL: http://code.google.com/p/mpmath/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-pytest
BuildRequires: python-gmpy
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
Mpmath is a pure-Python library for multiprecision floating-point arithmetic.
It provides an extensive set of transcendental functions, unlimited exponent sizes, complex numbers, interval arithmetic, numerical integration and differentiation, root-finding, linear algebra, and much more. Almost any calculation can be performed just as well at 10-digit or 1000-digit precision, and in many cases mpmath implements asymptotically fast algorithms that scale well for extremely high precision work

%if %{with doc}
%package doc
Summary: Documentation files for SuiteSparse
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
BuildRequires: python-sphinx
BuildRequires: python-matplotlib

%description doc
This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n %{modulename}-all-%{version}

%build
python setup.py build
%if %{with doc}
pushd doc
python build.py
mv build html
popd
%endif

%check
export PYTHONPATH='./build/lib/'
python mpmath/tests/runtests.py -strict

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc CHANGES LICENSE README
%doc demo
%if %{with doc}
%files doc
%defattr(-,root,wheel)
%doc doc/html 
%endif

%changelog
* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.16-2
- put documents into a doc subpackage

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.16-1
- fix type in Group

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.16-0
- initial build for Mac OS X WorkShop 10.6

