%bcond_with doc

Name:           python-setuptools
Version:        0.6.15
Release:        4%{?_dist_release}
Summary:        Download, build, install, upgrade, and uninstall Python packages
Summary(ja):     Python パッケージのダウンロード、ビルド、インストール、アップグレードおよびアンインストール用ツール
Group:          Development/Tools
License:        PSFL/ZPL
URL:            http://packages.python.org/distribute
Source0:        http://pypi.python.org/packages/source/d/distribute/distribute-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildArch:      noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1, python-devel > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python, python-devel
BuildRequires: python-devel
%endif
%if %{with doc}
BuildRequires: python-sphinx
%endif

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

%description -l ja
setuptools は Python distutils の拡張機能を集めたツールです。
このツールにより Python パッケージの構築や配布が簡単に行えるように
なります。特に他のパッケージに依存しているパッケージを扱う際に便利
です。
%prep
%setup -q -n distribute-%{version}

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
* Tue Sep  6 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.15-4
- add python-devel requirements

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.15-3
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.15-2
- rename python-distribute to python-setuptools

* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.15-1
- build with doc generate only html docs

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.6.15-0
- initial build for Mac OS X WorkShop

