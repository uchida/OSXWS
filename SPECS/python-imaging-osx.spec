%define __python /usr/osxws/bin/python
%define modulename imaging
%define frameworkdir /Library/Frameworks
%define python_inc %{frameworkdir}/Python.framework/Versions/%{python_version}/include/python%{python_version}

Summary: The Python Imaging Library
Summary(ja): Python イメージ処理ライブラリ
Name: python-%{modulename}
Version: 1.1.7
Release: 0%{?_dist_release}
License: MIT
Group: Development/Languages
URL: http://www.pythonware.com/products/pil
Source0: http://effbot.org/downloads/Imaging-%{version}.tar.gz
Patch0: imaging-1.1.6-osxws.patch

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: libjpeg >= 6a
Requires: libpng >= 1.0.12
Requires: zlib >= 1.1.4
Requires: freetype >= 2.1.3
BuildRequires: python-devel = 2.6.6
BuildRequires: lcms-devel
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: XOrg-devel libjpeg-devel libpng-devel zlib-devel freetype-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
The Python Imaging Library (PIL) adds image processing capabilities
to your Python environment.  This library provides extensive file
format support, an efficient internal representation, and fairly
powerful image processing capabilities.

%description -l ja
Python Imaging Library (PIL) は Python 環境にイメージ処理能力を加えます.
このライブラリには広範なファイル型式への対応, 効果的な内部表現, そして
真にパワフルなイメージ処理能力が備わっています.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{modulename}-%{version}
%patch0 -p1

%build
export CC='gcc-4.2' ARCHFLAGS='-arch i386 -arch x86_64'
python setup.py build

%check
python selftest.py

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/Sane
install Sane/*[^\.c$] $RPM_BUILD_ROOT%{python_sitelib}/Sane/
mkdir -p $RPM_BUILD_ROOT%{python_inc}/PIL
install libImaging/*.h $RPM_BUILD_ROOT%{python_inc}/PIL/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%{python_inc}/*
%doc BUILDME CHANGES CONTENTS README
%doc Docs

%changelog
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.1.7-0
- update to 1.1.7

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.1.6-0
- initial build for Mac OS X WorkShop

