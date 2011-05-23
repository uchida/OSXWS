%define __python /usr/osxws/bin/python
%define modulename gmpy

Summary: MPIR/GMP interface to Python
Name: python-%{modulename}
Version: 1.14
Release: 1%{?_dist_release}
Source0: http://gmpy.googlecode.com/files/%{modulename}-%{version}.zip
License: LGPLv2+
Group: Development/Languages
URL: http://code.google.com/p/gmpy/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: gmp-devel
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

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
export ARCHFLAGS="-arch i386 -arch x86_64"
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
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.14-1
- fix type in Group

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.14-0
- initial build for Mac OS X WorkShop 10.6

