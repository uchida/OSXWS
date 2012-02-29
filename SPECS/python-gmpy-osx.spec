%define modulename gmpy

Summary: MPIR/GMP interface to Python
Name: python-%{modulename}
Version: 1.15
Release: 0%{?_dist_release}
Source0: http://gmpy.googlecode.com/files/%{modulename}-%{version}.zip
License: LGPLv2+
Group: Development/Languages
URL: http://code.google.com/p/gmpy/

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires: gmp-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
A C-coded Python extension module
that wraps the GMP library to provide to Python code
fast multiprecision arithmetic (integer, rational, and float),
random number generation, advanced number-theoretical functions,
and more.

%prep
%setup -q -n %{modulename}-%{version}

%build
export CFLAGS='-I%{_includedir}'
export LDFLAGS='-L%{_libdir}'
export ARCHFLAGS="-arch x86_64"
python setup.py build_ext

%check
export PYTHONPATH=`ls -d ./build/lib*`
python test/gmpy_test.py

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc doc/*
%doc changes.txt lgpl-2.1.txt mac_build.txt mutable_mpz.txt README

%changelog
* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.15-0
- update to 1.15

* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.14-4
- build x86_64 mono arch

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.14-3
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.14-2
- remove unnecessary requires
- build with specific compiler

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.14-1
- fix type in Group

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.14-0
- initial build for Mac OS X WorkShop 10.6

