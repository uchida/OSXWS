%define modulename scipy
%bcond_with doc

Summary: Scientific Library for Python
Summary(ja): Python 科学技術計算ライブラリ
Name: python-%{modulename}
Version: 0.9.0
Release: 4%{?_dist_release}
Source0: http://downloads.sourceforge.net/%{modulename}/%{modulename}-%{version}.tar.gz
License: BSD
Group: Development/Languages
URL: http://www.scipy.org

Requires: apple-gcc
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
Requires: python-numpy
Requires: suitesparse-devel
Requires: python-nose
BuildRequires: apple-gcc
BuildRequires: python-numpy
BuildRequires: suitesparse-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
SciPy (pronounced "Sigh Pie") is open-source software for mathematics, science, and engineering. The SciPy library depends on NumPy, which provides convenient and fast N-dimensional array manipulation. The SciPy library is built to work with NumPy arrays, and provides many user-friendly and efficient numerical routines such as routines for numerical integration and optimization. Together, they run on all popular operating systems, are quick to install, and are free of charge. NumPy and SciPy are easy to use, but powerful enough to be depended upon by some of the world's leading scientists and engineers. If you need to manipulate numbers on a computer and display or publish the results, give SciPy a try!

%description -l ja
Scipy ("Sigh Pie" と発音) は数学、科学、工学向けのオープンソースソフトウェアです。
Scipy は使い易い高速な N 次元配列操作ライブラリ Numpy に依存しています。
Scipy は NumPy 配列と共にビルドされ、多くのユーザーフレンドリーで効率の良い数値積分や最適化といったルーチンを提供します。
全ての一般的なな OS で動作し、インストールも高速で、ライセンス料等の支払いの必要もありません。
Numpy と Scipy は簡単に利用できる上に科学、工学の先端をリードするだけのパワーも持っています。
計算機上で数値を操作し、結果を表示し、発表する必要があれば、Scipy を試してみましょう。

%if %{with doc}
%package doc
Summary: Documentation files for SuiteSparse
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
BuildRequires: python-sphinx python-matplotlib

%description doc
This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n %{modulename}-%{version}

%build
export CC='/usr/osxws/bin/gcc-4.2' CXX='/usr/osxws/bin/g++-4.2'
export F77='/usr/osxws/bin/gfortran-4.2' F90='/usr/osxws/bin/gfortran-4.2'
export ARCHFLAGS='-arch i386 -arch x86_64'
python setup.py build

for f in `find $RPM_BUILD_DIR/build -type f -name __config__.py`; do
    sed -i."tmp" "s,# This file is generated by $RPM_BUILD_DIR/%{name}-%{version}/setup.py\n,,g" $f
    rm -f $f.tmp
done

%if %{with doc}
pushd doc
make html latex
pushd build/latex
make all-pdf
popd
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
%if %{with doc}
%files doc
%doc doc/build/html
%doc doc/build/latex/scipy*.pdf
%endif

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.9.0-4
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.9.0-3
- remove unnecessary requires
- build with specific compiler

* Mon Apr 25 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.9.0-2
- put documents into a doc subpackage

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.9.0-1
- fix typo in Group

* Thu Mar  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.9.0-0
- update to 0.9.0

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.8.0-1
- rebuild with documents

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.8.0-0
- initial build for Mac OS X WorkShop 10.6

