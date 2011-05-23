%define __python /usr/osxws/bin/python
%define modulename distribute
%bcond_with doc

Summary: Easily download, build, install, upgrade, and uninstall Python
Name: python-%{modulename}
Version: 0.6.15
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/d/%{modulename}/%{modulename}-%{version}.tar.gz
License: PSF or ZPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: python = 2.6.6
Requires: python-devel = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
%if %{with doc}
BuildRequires: python-sphinx
%endif
Obsoletes: python-setuptools
URL: http://packages.python.org/distribute

%description
Distribute is a fork of the Setuptools project.
        
Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build
%if %{with doc}
pushd docs
make html
popd
%endif

%install
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/easy_install*
%{python_sitelib}/*
%doc CHANGES.txt CONTRIBUTORS.txt DEVGUIDE.txt README.txt
%if %{with doc}
%doc docs/build/html
%endif


%changelog
* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.15-1
 - build with doc generate only html docs

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.15-0
- initial build for Mac OS X WorkShop

