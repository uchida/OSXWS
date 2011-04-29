%define __python /usr/osxws/bin/python
%define modulename virtualenv
%bcond_with doc

Summary: Virtual Python Environment builder
Name: python-%{modulename}
Version: 1.5.2
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/v/%{modulename}/%{modulename}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: python = 2.6.6
Requires: python-devel = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: python-distribute
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
%if %{with doc}
BuildRequires: python-sphinx
%endif
URL: http://www.virtualenv.org

%description
virtualenv is a tool to create isolated Python environments. virtualenv
is a successor to workingenv, and an extension of virtual-python. It is
written by Ian Bicking, and sponsored by the Open Planning Project. It is
licensed under an MIT-style permissive license.

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/virtualenv
%{python_sitelib}/*
%doc docs/*.txt

%changelog
* Sun Apr  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5.2-0
- initial build for Mac OS X WorkShop

