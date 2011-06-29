%{!?python_sitelib:     %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define ver 0.9.4
%define rel 2

Summary: A collection of tools for internationalizing Python applications
Name: python-babel
Version: %{ver}
Release: %{rel}%{?_dist_release}
Source0: http://ftp.edgewall.com/pub/babel/Babel-%{version}.tar.bz2
License: modified BSD-style License
Group: Development/Libraries
URL: http://babel.edgewall.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

Vendor: Project Vine
Distribution: Vine Linux


%description
Babel is composed of two major parts:

 * tools to build and work with gettext message catalogs
 * a Python interface to the CLDR (Common Locale Data Repository), 
   providing access to various locale display names, localized number 
   and date formatting, etc. 


%prep
%setup -q -n Babel-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf ${RPM_BUILD_ROOT}
%{__python} setup.py install --root=${RPM_BUILD_ROOT} 


%clean
%{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc COPYING ChangeLog README.txt contrib doc scripts
%{_bindir}/pybabel
%{python_sitelib}/Babel-*.egg-info
%{python_sitelib}/babel

%changelog
* Wed Feb  3 2010 Shu KONNO <owa@bg.wakwak.com> 0.9.4-2
- rebuilt with python-2.6.4

* Sun Apr  5 2009 IWAI, Masaharu <iwai@alib.jp> 0.9.4-1
- initial release

