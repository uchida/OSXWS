%define modulename sip
%define python_inc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")
%define python_bin %(%{__python} -c "from distutils.sysconfig import get_config_var; print get_config_var('BINDIR')")

Summary: SIP - Python/C++ Bindings Generator
Name: python-sip
Version: 4.12.2
Release: 0%{?_dist_release}
License: GPLv2 or GPLv3
Group: Development/Tools
Url: http://www.riverbankcomputing.com/software/sip/intro 
Source0: http://www.riverbankcomputing.com/static/Downloads/sip4/sip-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python-devel
BuildArch: fat

%description
SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python bindings for any C++
class library.

%prep
%setup -q -n %{modulename}-%{version}

%build
python configure.py -d %{python_sitearch} --arch i386 --arch x86_64
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf %{python_bin}/sip $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc LICENSE LICENSE-GPL2 LICENSE-GPL3
%doc NEWS README
%doc doc/html
%{_bindir}/sip
%{python_bin}/sip
%{python_sitearch}/*
%{python_inc}/*

%changelog
* Sun May  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.12.1-0
- initial build for Mac OS X

