Summary: The Cython compiler for writing C extensions for the Python language 
Name: Cython
Version: 0.15.1
Release: 2%{?_dist_release}
Source0: http://cython.org/release/%{name}-%{version}.tar.gz
Patch1: Cython-mac-python.patch
License: Apache
Group: Development/Languages
URL: http://numpy.scipy.org/

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
%else
Requires: python
%endif
%if "%{?_dist_release}" == "osx10.6"
BuildRequires: python-devel > 2.6.1
%else
BuildRequires: python-devel
%endif
BuildRequires: python-numpy
Obsoletes: python-Cython
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: x86_64

%description
The Cython language makes writing C extensions for the Python language as
easy as Python itself.  Cython is a source code translator based on the
well-known Pyrex, but supports more cutting edge functionality and
optimizations.

The Cython language is very close to the Python language (and most Python
code is also valid Cython code), but Cython additionally supports calling C
functions and declaring C types on variables and class attributes. This
allows the compiler to generate very efficient C code from Cython code.

This makes Cython the ideal language for writing glue code for external C
libraries, and for fast C modules that speed up the execution of Python
code.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
export ARCHFLAGS=''
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
export ARCHFLAGS=''
python setup.py install --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/cygdb
%{_bindir}/cython
%{python_sitelib}/Cython*
%{python_sitelib}/cython.py*
%{python_sitelib}/pyximport
%doc Demos Doc
%doc COPYING.txt INSTALL.txt LICENSE.txt README.txt ToDo.txt USAGE.txt

%changelog
* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.15.1-1
- build x86_64 mono arch

* Fri Oct 21 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.15.1-0
- update to 0.15.1

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.14.1-2
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.14.1-1
- remove unnecessary requires
- build with specific compiler

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.14.1-0
- initial build for Mac OS X WorkShop 10.6

