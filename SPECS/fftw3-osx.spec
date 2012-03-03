%define distname fftw

Summary: Fast Fourier Transform library
Name: fftw3
Version: 3.3
Release: 0%{?_dist_release}
License: GPL
Group: System Environment/Libraries
URL: http://www.fftw.org/

Source: http://www.fftw.org/fftw-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{distname}-%{version}-root
%if "%{?_dist_release}" == "osx10.7"
BuildRequires: gcc >= 4.6.2
%endif

%description
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n %{distname}-%{version}

%build
export CC="/usr/bin/gcc" CXX="/usr/bin/g++" F77="%{_bindir}/gfortran"
./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} \
            --bindir=%{_bindir} --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --sharedstatedir=%{_sharedstatedir} \
            --mandir=%{_mandir} --infodir=%{_infodir} \
            --enable-fortran --enable-shared --enable-threads
make
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%post devel
install-info %{_infodir}/%{name}.info %{_infodir}/dir

%preun devel
install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc AUTHORS ChangeLog COPYING COPYRIGHT NEWS README* TODO
%{_libdir}/lib*.*.*

%files devel
%defattr(-,root,wheel)
%{_bindir}/*
%{_includedir}/*.h
%{_includedir}/*.f
%{_libdir}/lib*.*
%{_libdir}/pkgconfig/*.pc
%doc doc/*.pdf doc/FAQ/fftw-faq.html doc/html
%{_mandir}/man?/*
%{_infodir}/*.info*
%exclude %{_libdir}/lib*.*.*

%changelog
* Sun Mar 04 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.3-0
- update to 3.3
- build x86_64 mono arch

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.2.2-0
- initial build for Mac OS X WorkShop

