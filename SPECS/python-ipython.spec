%define __python /usr/osxws/bin/python
%define modulename ipython
%bcond_with doc

Summary: An interactive computing environment for Python
Name: python-%{modulename}
Version: 0.10.2
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/i/ipython/%{modulename}-%{version}.tar.gz
License: BSD
Group: Development/Languages
URL: http://ipython.scipy.org/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-sphinx
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
The goal of IPython is to create a comprehensive environment for interactive and exploratory computing.
To support this goal, IPython has two main components:

- An enhanced interactive Python shell.
- An architecture for interactive parallel computing.

%if %{with doc}
%package doc
Summary: Documentation files for SuiteSparse
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build \
                        --root=$RPM_BUILD_ROOT \
                        --install-scripts=%{_bindir} --install-data=%{_prefix}
emacs_lisp_dir=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
mkdir -p $emacs_lisp_dir
install docs/emacs/ipython.el $emacs_lisp_dir
# decompress man files for rpm brz-compress, not necessally
pushd $RPM_BUILD_ROOT%{_mandir}/man1
for gzman in *.1.gz; do
    gzip -d $gzman && rm -f $gzman
done
popd
# remove documents, for docs rpm 
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%{_mandir}/*
%{_datadir}/emacs/site-lisp/ipython.el
%doc README.txt
%if %{with doc}
%files doc
%defattr(-,root,wheel)
%doc docs/dist/html docs/dist/ipython.pdf
%doc docs/examples IPython/Extensions/igrid_help.*
%endif

%changelog
* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.10.2-0
- initial build for Mac OS X WorkShop

