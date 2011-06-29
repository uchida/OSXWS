%define __python /usr/osxws/bin/python
%define modulename jinja2
%bcond_with doc

Summary: A small but fast and easy to use stand-alone template engine written in pure python.
Summary(ja): Python で書かれた小さく軽量で易しいスタンドアローンテンプレートエンジン
Name: python-%{modulename}
Version: 2.5.5
Release: 2%{?_dist_release}
Source0: http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
License: BSD
Group: Development/Languages
URL: http://jinja.pocoo.org/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-setuptools
%if %{with doc}
BuildRequires: python-sphinx
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
Jinja2 is a template engine written in pure Python. 
It provides a Django inspired non-XML syntax
but supports inline expressions and an optional sandboxed environment.

%description -l ja
Jinja2 は Python で書かれたテンプレートエンジンです。
Django の影響を受けたインライン表現と
付加的にサンドボックス環境をサポートした、非 XML 構文を提供します。

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
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc AUTHORS CHANGES LICENSE
%if %{with doc}
%doc docs/_build/html
%endif
%doc examples

%changelog
* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.5.5-2
- requires python-setuptools

* Fri Apr  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.5.5-1
- replace setuptools with distribute

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.5.5-0
- initial build for Mac OS X WorkShop 10.6

