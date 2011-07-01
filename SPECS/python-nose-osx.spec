%define modulename nose
%bcond_with doc

Name:		python-nose
Version:    0.11.3
Release:    2%{?_dist_release}
Summary:	A discovery-based unittest extension for Python
Summary(ja):	Python 用の発見型ユニットテスト・エクステンション

Group:		Development/Languages
License:	LGPLv2
URL:		http://somethingaboutorange.com/mrl/projects/nose/
Source0:	http://somethingaboutorange.com/mrl/projects/nose/nose-%{version}.tar.gz
Patch0:     nose-0.11.3-osxws.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
BuildRequires: python-devel, python-setuptools
%if %{with doc}
BuildRequires: python-sphinx
%endif
Requires: python-setuptools


%description
nose: a discovery-based unittest extension.

nose provides an alternate test discovery and running process for unittest,
one that is intended to mimic the behavior of py.test as much as is
reasonably possible without resorting to too much magic.


%prep
%setup -q -n %{modulename}-%{version}
%patch0 -p1

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
                        --install-scripts=%{_bindir} --install-data=%{_prefix} \
                        --single-version-externally-managed

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc AUTHORS CHANGELOG NEWS README.txt lgpl.txt
%doc examples
%if %{with doc}
%doc doc/.build/html
%endif
%{_bindir}/nosetests
%{_mandir}/man1/nosetests.1.gz
%{python_sitelib}/nose-%{version}-py%{pyver}.egg-info
%{python_sitelib}/nose

%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.11.3-2
- make more compatible with Vine Linux

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.11.3-1
- rebuild with documents

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.11.3-0
- initial build for Mac OS X WorkShop 10.6

