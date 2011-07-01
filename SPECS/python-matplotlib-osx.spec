%define __python /usr/osxws/bin/python
%define modulename matplotlib
%bcond_with doc

Summary: Python plotting package
Summary(ja): Python プロットパッケージ
Name: python-%{modulename}
Version: 1.0.1
Release: 0%{?_dist_release}
Source0: http://downloads.sourceforge.net/%{modulename}/%{modulename}-%{version}.tar.gz
Patch0: matplotlib-setup.cfg.patch
# sphinx >= 1.0.6 compatible patch
# http://sourceforge.net/tracker/?func=detail&aid=3165692&group_id=80706&atid=560722
Patch1: matplotlib-doc-small.patch
License: PSF
Group: Development/Languages
URL: http://matplotlib.sourceforge.net

Requires: python
Requires: python-numpy
Requires: python-dateutil
Requires: python-pytz
Requires: freetype libpng
BuildRequires: python-devel
BuildRequires: freetype-devel libpng-devel pkgconfig
BuildRequires: python-pytz
BuildRequires: python-dateutil
BuildRequires: tetex ghostscript dvipng
BuildRequires: apple-gcc
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
matplotlib strives to produce publication quality 2D graphics
for interactive graphing, scientific publishing,
user interface development and web application servers
targeting multiple user interfaces and hardcopy output formats.
There is a 'pylab' mode which emulates matlab graphics

%description -l ja
matplotlib は出版に耐えうる品質の二次元グラフィックの生成を志しています。
用途としてはインタラクティブな図作成、科学技術出版はもちろん、
さらに多数のユーザーインターフェース、出力フォーマットに対応し、
ユーザーインターフェース開発や Web アプリケーションサーバーに利用できます。
matlab のグラフィックをエミュレートする 'pylab' モードがあります。

%if %{with doc}
%package doc
Summary: Documentation files for SuiteSparse
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
BuildRequires: python-sphinx
BuildRequires: python-xlwt
BuildRequires: python-matplotlib
BuildRequires: graphviz

%description doc
This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n %{modulename}-%{version}
%patch0 -p1
%patch1 -p1

%build
export CC='/usr/osxws/bin/gcc-4.2' CXX='/usr/osxws/bin/g++-4.2'
export ARCHFLAGS='-arch i386 -arch x86_64'
python setup.py build
%if %{with doc}
pushd doc
python make.py --small html latex
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
rm -rf doc/build/html/_sources

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%defattr(644,root,wheel,755)
%doc CHANGELOG INSTALL INTERACTIVE KNOWN_BUGS README.txt TODO
%doc license matplotlibrc.template
%if %{with doc}
%files doc
%defattr(-,root,wheel)
%doc doc/build/html doc/build/latex/matplotlib.pdf
%endif

%changelog
* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.1-0
- remove unnecessary requires
- build with specific compiler

* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.0-0
- initial build for Mac OS X WorkShop 10.6

