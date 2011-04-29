%define __python /usr/osxws/bin/python
%define modulename nose
%bcond_with doc

Summary: A unittest-based testing framework for python
Summary(ja): Python 用ユニットテストフレームワーク
Name: python-%{modulename}
Version: 0.11.3
Release: 1%{?_dist_release}
Source0: http://somethingaboutorange.com/mrl/projects/nose/nose-%{version}.tar.gz
Patch0: nose-0.11.3-osxws.patch
License: LGPLv2
Group: Development/Languages
URL: http://somethingaboutorange.com/mrl/projects/nose/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: python-distribute
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
A unittest-based testing framework for python that makes writting and running tests easier.

nose provides an alternate test discovery and running process for unittest,
one that is intended to mimic the behavior of py.test as much as is reasonably possible without resorting to too much magic.

%prep
%setup -q -n %{modulename}-%{version}
%patch0 -p1

%build
python setup.py build
%if %{with doc}
pushd doc
make html latex
pushd .build/latex
make all-pdf
popd
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT \
                        --install-scripts=%{_bindir} --install-data=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%{_mandir}/*
%doc AUTHORS CHANGELOG NEWS README.txt lgpl.txt
%doc examples
%if %{with doc}
%doc doc/.build/html doc/.build/latex/nose.pdf
%endif

%changelog
* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.11.3-1
- rebuild with documents

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.11.3-0
- initial build for Mac OS X WorkShop 10.6

