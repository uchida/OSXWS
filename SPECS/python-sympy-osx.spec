%define __python /usr/osxws/bin/python
%define modulename sympy
%bcond_with doc
%bcond_with ipython

Summary: Python library for symbolic mathematics
Name: python-%{modulename}
Version: 0.6.7
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/s/%{modulename}/%{modulename}-%{version}.tar.gz
License: BSD
Group: Development/Languages
URL: http://code.google.com/p/sympy/

Requires: python
%if %{with ipython}
Requires: ipython
%endif
BuildRequires: python-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
SymPy is a Python library for symbolic mathematics.
It aims to become a full-featured computer algebra system (CAS) while keeping
the code as simple as possible in order to be comprehensible and easily extensible.
SymPy is written entirely in Python and does not require any external libraries.

%if %{with doc}
%package doc
Summary: Documentation files for SuiteSparse
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
BuildRequires: python-sphinx
BuildRequires: python-mpmath

%description doc
This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%if %{with doc}
pushd doc
make html
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT \
                        --install-scripts=%{_bindir} --install-data=%{_prefix}
%if %{with ipython}
# install ipython conf
ipython_conf_dir=$RPM_BUILD_ROOT%{python_sitelib}/IPython/UserConfig
mkdir -p $ipython_conf_dir
install -m 644 data/IPython/ipythonrc-sympy $ipython_conf_dir
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{_mandir}/man1/*
%{python_sitelib}/%{modulename}
%if %{with ipython}
%{python_sitelib}/IPython/UserConfig/ipythonrc-sympy
%endif
%doc AUTHORS LICENSE README TODO
%doc examples
%if %{with doc}
%files doc
%doc doc/_build/html doc/_build/sympy.pdf
%endif

%changelog
* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.7-1
- requires ipython

* Tue Apr 26 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.7-0
- initial build for Mac OS X WorkShop 10.6

