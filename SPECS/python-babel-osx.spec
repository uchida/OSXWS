Summary: A collection of tools for internationalizing Python applications
Name: python-babel
Version: 0.9.4
Release: 1%{?_dist_release}
Source0: http://ftp.edgewall.com/pub/babel/Babel-%{version}.tar.bz2
License: modified BSD-style License
Group: Development/Libraries
URL: http://babel.edgewall.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif

%description
Babel is composed of two major parts:

 * tools to build and work with gettext message catalogs
 * a Python interface to the CLDR (Common Locale Data Repository), 
   providing access to various locale display names, localized number 
   and date formatting, etc. 

%prep
%setup -q -n Babel-%{version}

%build
python setup.py build

%install
rm -rf ${RPM_BUILD_ROOT}
python setup.py install --skip-build --root=${RPM_BUILD_ROOT} --install-scripts=%{_bindir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,wheel)
%doc COPYING ChangeLog README.txt contrib doc scripts
%{_bindir}/pybabel
%{python_sitelib}/Babel-*.egg-info
%{python_sitelib}/babel

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.9.4-1
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.9.4-0
- initial build for Mac OS X WorkShop

