%define modulename pytest
%bcond_with doc

Summary: simple powerful testing with Python
Name: python-%{modulename}
Version: 2.0.0
Release: 6%{?_dist_release}
Source0: http://pypi.python.org/packages/source/p/%{modulename}/%{modulename}-%{version}.zip
License: MIT
Group: Development/Languages
URL: http://pytest.org/

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
Requires: python-py
Requires: python-setuptools
BuildRequires: python-setuptools
%if %{with doc}
BuildRequires: python-sphinx python-py
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
py.test is a simple and popular testing tool for Python.

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build
%if %{with doc}
pushd doc
export PYTHONPATH="../"
make html
make latexpdf
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%doc CHANGELOG LICENSE README.txt
%if %{with doc}
%doc doc/_build/html doc/_build/latex/pytest.pdf
%endif

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.0-6
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.0-5
- remove unnecessary requires

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.0-4
- requires python-setuptools

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.0-3
- fix type in Group

* Fri Apr  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.0-2
- replace setuptools with distribute

* Wed Dec 22 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.0-1
- rebuild with documents

* Wed Dec 22 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.0-0
- initial build for Mac OS X WorkShop 10.6

