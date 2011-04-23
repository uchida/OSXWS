%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: lcms
Version: 1.19
Release: 0%{?dist}
Summary: Color Management System
Group: Applications/Productivity
License: MIT
URL: http://www.littlecms.com/
Source0: http://www.littlecms.com/lcms-%{version}.tar.gz
Patch0: lcms-1.19-rhbz675186.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: fat
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig
BuildRequires: python-devel
BuildRequires: zlib-devel
Requires: %{name}-libs = %{version}-%{release}
%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form.

%package libs
Summary: Library for %{name}
Group: System Environment/Libraries
%description libs
The %{name}-libs package contains library for %{name}.

%package -n python-%{name}
Summary: Python interface to LittleCMS
Group: Development/Libraries
Requires: python
%description -n python-%{name}
Python interface to LittleCMS.

%package devel
Summary: Development files for LittleCMS
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
%description devel
Development files for LittleCMS.


%prep
%setup -q
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
./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} \
            --bindir=%{_bindir} --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --sharedstatedir=%{_sharedstatedir} \
            --mandir=%{_mandir} --infodir=%{_infodir} \
            --with-python --disable-static \
            CC='gcc-4.2 -arch i386 -arch x86_64' \
            CPP="gcc-4.2 -E" \
            CXX='g++-4.2 -arch i386 -arch x86_64' \
            CXXCPP="g++-4.2 -E" \

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

pushd python
./swig_lcms
popd

make


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
# remove extraneous
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README.1ST doc/TUTORIAL.TXT
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_libdir}/*.*.dylib

%files devel
%defattr(-,root,root,-)
%doc doc/LCMSAPI.TXT
%{_includedir}/*
%{_libdir}/*.dylib
%{_libdir}/pkgconfig/%{name}.pc

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/lcms.py*
%{python_sitearch}/_lcms.so


%changelog
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp>
- initial build for Mac OS X WorkShop

