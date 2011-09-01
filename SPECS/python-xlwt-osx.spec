%define modulename xlwt

Summary: Library to create spreadsheet files compatible with MS Excel files
Summary(ja): MS Excel 互換表計算ファイル生成ライブラリ
Name: python-%{modulename}
Version: 0.7.2
Release: 2%{?_dist_release}
Source0: http://pypi.python.org/packages/source/x/%{modulename}/%{modulename}-%{version}.tar.gz
License: BSD
Group: Development/Languages
URL: https://secure.simplistix.co.uk/svn/xlwt/trunk

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
%description
xlwt is a library for generating spreadsheet files that are compatible with Excel 97/2000/XP/2003, OpenOffice.org Calc, and Gnumeric. xlwt has full support for Unicode. Excel spreadsheets can be generated on any platform without needing Excel or a COM server. The only requirement is Python 2.3 to 2.6. xlwt is a fork of pyExcelerator.

%description -l ja
xlwt は Excel 97/2000/XP/2003, OpenOffice.org Calc, Gnumeric 等の表計算ソフト互換性を持つファイルを生成するらライブラリです。
xlwt は Unicode を完全にサポートしています。
Execl 表計算ファイルの生成に Exel や COM サーバーは不要で、
バージョン 2.3 から 2.6 の Python だけを必要とします。
xlwt は pyExcelerator のフォークです。

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc HISTORY.html licences.py README.html

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7.2-2
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7.2-1
- remove unnecessary requires

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7.2-0
- initial build for Mac OS X WorkShop 10.6

