%global srcname pip

Summary:        Pip installs Python packages.  An easy_install replacement
Summary(ja):    Pip は easy_install を置き換える Python パッケージインストーラです。
Name:           python-%{srcname}
Version:        0.8.3
Release:        1%{?_dist_release}

Group:          Development/Libraries
License:        MIT
URL:            http://pip.openplans.org
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-setuptools

%description

Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

pip is meant to improve on easy_install.bulletin boards, etc.).

%prep
%setup -q -n %{srcname}-%{version}
sed -i.tmp '1d' pip/__init__.py
rm -f pip/__init__.py.tmp

%build
python setup.py build

%install
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

rm -rf $RPM_BUILD_ROOT%{_bindir}/pip-*
mv $RPM_BUILD_ROOT%{_bindir}/pip $RPM_BUILD_ROOT%{_bindir}/pip-python

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc PKG-INFO docs/_build/html/*.html
%attr(755,root,wheel) %{_bindir}/pip-python
%{python_sitelib}/pip*

%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.8.3-1
- make more compatible with Vine Linux

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.8.3-0
- initial build for Mac OS X WorkShop

