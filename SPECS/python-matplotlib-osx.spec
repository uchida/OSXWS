%define modulename matplotlib
%bcond_with doc

Summary: Python plotting package
Summary(ja): Python プロットパッケージ
Name: python-%{modulename}
Version: 1.1.0
Release: 0%{?_dist_release}
Source0: http://downloads.sourceforge.net/%{modulename}/%{modulename}-%{version}.tar.gz
Patch0: matplotlib-setup.cfg.patch
License: PSF
Group: Development/Languages
URL: http://matplotlib.sourceforge.net

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
Requires: python-numpy
Requires: python-dateutil
Requires: python-pytz
Requires: freetype libpng
BuildRequires: freetype-devel libpng-devel pkgconfig
BuildRequires: python-pytz
BuildRequires: python-dateutil
BuildRequires: texlive-collection-basic, dvipng
BuildRequires: ghostscript
BuildRoot: %{_tmppath}/%{name}-%{version}-root

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
Summary: Documentation files for %{name}
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

%build
export ARCHFLAGS=''
export CFLAGS='-dynamic -Os -g -pipe -fno-strict-aliasing -fno-common -fwrapv -DENABLE_DTRACE -DMACOSX -DNDEBUG'
export OPT='-DNDEBUG -g -fwrapv -Os'
python setup.py build_ext
%if %{with doc}
pushd doc
python make.py --small html
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
export ARCHFLAGS=''
export CFLAGS='-dynamic -Os -g -pipe -fno-strict-aliasing -fno-common -fwrapv -DENABLE_DTRACE -DMACOSX -DNDEBUG'
export OPT='-DNDEBUG -g -fwrapv -Os'
python setup.py install --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
rm -rf doc/build/html/_sources

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/%{modulename}
%{python_sitelib}/%{modulename}-%{version}-py%{pyver}.egg-info
%{python_sitelib}/mpl_toolkits
%{python_sitelib}/pylab.py*
%defattr(644,root,wheel,755)
%doc CHANGELOG INSTALL README.txt TODO
%doc matplotlibrc.template
%if %{with doc}
%files doc
%defattr(-,root,wheel)
%doc doc/build/html
%endif

%changelog
* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.1.0-0
- update to 1.1.0 
- builx x86_64 mono arch

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.7-3
- mofify python requirements for OSXWS

* Mon Aug 22 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.7-2
- switchover from tetex to texlive

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.1-0
- remove unnecessary requires
- build with specific compiler

* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.0-0
- initial build for Mac OS X WorkShop 10.6

