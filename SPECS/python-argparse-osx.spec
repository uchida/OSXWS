%define modulename argparse
%bcond_with doc

Summary: Python command-line parsing library
Name: python-%{modulename}
Version: 1.2.1
Release: 2%{?_dist_release}
Source0:http://argparse.googlecode.com/files/argparse-%{version}.tar.gz
License: PSL
Group: Development/Languages
URL: http://code.google.com/p/argparse/

Requires: python
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
The argparse module makes it easy to write user friendly command line
interfaces.

The program defines what arguments it requires, and argparse will figure out
how to parse those out of sys.argv. The argparse module also automatically
generates help and usage messages and issues errors when users give the
program invalid arguments.

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build
%if %{with doc}
pushd doc
make html latexpdf
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc LICENSE.txt NEWS.txt README.txt
%if %{with doc}
%doc doc/_build/html doc/_build/latex/argparse.pdf
%endif

%changelog
* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.2.1-2
- remove unnecessary requires

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.2.1-1
- requires python-setuptools

* Sun Apr  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.2.1-0
- initial build for Mac OS X WorkShop 10.6

