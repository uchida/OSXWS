%define __python /usr/osxws/bin/python
%define modulename virtualenvwrapper
%bcond_with doc

Summary: Enhancements to virtualenv
Name: python-%{modulename}
Version: 2.6.3
Release: 0%{?_dist_release}
Source0: http://www.doughellmann.com/downloads/%{modulename}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: python = 2.6.6
Requires: python-devel = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
URL: http://www.virtualenv.org

%description
virtualenvwrapper is a set of extensions to virtualenv tool.
The extensions include wrappers for creating and deleting virtual environments
and otherwise managing your development workflow, making it easier to work on more
than one project at a time without introducing conflicts in their dependencies.

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
%{_bindir}/virtualenvwrapper.sh
%{python_sitelib}/*
%doc README.txt
%doc docs/html/*

%changelog
* Sun Apr  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.5.2-0
- initial build for Mac OS X WorkShop

