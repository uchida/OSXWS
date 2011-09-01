%define modulename virtualenvwrapper

Summary: Enhancements to virtualenv
Name: python-%{modulename}
Version: 2.7.1
Release: 2%{?_dist_release}
Source0: http://www.doughellmann.com/downloads/%{modulename}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1, python-devel > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python, python-devel
BuildRequires: python-devel
%endif
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
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.7.1-2
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.7.1-1
- remove unnecessary requires

* Thu May 19 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.7.1-0
- update to 2.7.1

* Sun Apr  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.3-0
- initial build for Mac OS X WorkShop

