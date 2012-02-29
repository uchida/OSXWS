Name: lcms
Summary: Little CMS - color management engine
Summary(ja): Little CMS - カラーマネージメントエンジン
Version: 1.19
Release: 3%{?_dist_release}

Group: System Environment/Libraries
License: MIT
URL: http://www.littlecms.com/

Source0: http://www.littlecms.com/%{name}-%{version}.tar.gz
Patch0: lcms-1.19-rhbz675186.patch
Patch100: lcms-1.18_cmsxfrom_CVE-2009-0793.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: zlib-devel
BuildRequires: libtiff-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig
BuildRequires: swig
%if "%{?_dist_release}" == "osx10.6"
BuildRequires: python-devel > 2.6.1
%else
BuildRequires: python-devel
%endif

%description
Little cms intends to be a small-footprint, speed optimized color management
engine in open source form.

%package devel
Summary: Header files and library for development with LCMS
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files for development with LCMS

%package utils
Summary: Additional Command Line Utilities for littlecms
Group: Applications/Graphics
Requires: %{name} = %{version}-%{release}

%description utils
Command line utilities which can perform icc transforms and provide info 
about icc profiles.

%package -n python-%{name}
Summary: Python interface to LittleCMS
Group: Development/Libraries
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
%else
Requires: python
%endif
%description -n python-%{name}
Python interface to LittleCMS.

%prep
%setup -q -n %{name}-%{version}
%patch100 -p1 -b .CVE-2009-0793
pushd samples
%patch0 -p0
popd

find . -name \*.[ch] | xargs chmod -x
chmod 0644 AUTHORS COPYING ChangeLog NEWS README.1ST doc/TUTORIAL.TXT doc/LCMSAPI.TXT

# Convert not UTF-8 files
pushd doc
mkdir -p __temp
for f in LCMSAPI.TXT TUTORIAL.TXT ;do
cp -p $f __temp/$f
iconv -f ISO-8859-1 -t UTF-8 __temp/$f > $f
touch -r __temp/$f $f
done
rm -rf __temp
popd

%build
%configure --with-python --disable-static
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
pushd python
./swig_lcms
popd
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove extraneous
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,wheel)
%doc AUTHORS COPYING ChangeLog README.1ST TUTORIAL.TXT NEWS
%{_libdir}/*.*.dylib

%files devel
%defattr(-,root,wheel)
%{_includedir}/*
%{_libdir}/*.dylib
%{_libdir}/pkgconfig/lcms.pc
%doc LCMSAPI.TXT doc/ 

%files utils
%defattr(-,root,wheel)
%{_bindir}/*
%{_mandir}/man1/*

%files -n python-%{name}
%defattr(-,root,wheel)
%{python_sitearch}/lcms.py*
%{python_sitearch}/_lcms.so

%changelog
* Sat Feb 18 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.19-2
- build x86_64 mono arch

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.19-2
- mofify python requirements for OSXWS

* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.19-1
- make more compatible with Vine Linux

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.19-0
- initial build for Mac OS X WorkShop

