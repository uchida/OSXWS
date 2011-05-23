%define __python /usr/osxws/bin/python
%define modulename execnet
%bcond_with doc

Summary: rapid multi-Python deployment
Name: python-%{modulename}
Version: 1.0.9
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/e/%{modulename}/%{modulename}-%{version}.zip
License: GPLv2+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: python = 2.6.6
Requires: python-devel = 2.6.6
BuildRequires: python-devel = 2.6.6
%if %{with doc}
BuildRequires: python-sphinx
%endif

URL: http://codespeak.net/execnet

%description
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers.
It provides a minimal and fast API targetting the following uses:
                         
- distribute tasks to local or remote CPUs
- write and deploy hybrid multi-process applications
- write scripts to administer a bunch of exec environments

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build
%if %{with doc}
pushd doc
make html
make latex
pushd _build/latex
make all-pdf
popd
popd
%endif

%install
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc CHANGELOG LICENSE README.txt
%if %{with doc}
%doc doc/_build/html doc/_build/latex/execnet.pdf
%endif

%changelog
* Sun Feb  6 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.9
- initial build for Mac OS X WorkShop

