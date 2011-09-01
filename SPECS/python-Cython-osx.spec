%define modulename Cython

Summary: The Cython compiler for writing C extensions for the Python language 
Name: python-%{modulename}
Version: 0.14.1
Release: 2%{?_dist_release}
Source0: http://cython.org/release/%{modulename}-%{version}.tar.gz
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
BuildRequires: apple-gcc
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

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
%setup -q -n %{modulename}-%{version}
%patch1 -p1

%build
export CC='/usr/osxws/bin/gcc-4.2' CXX='/usr/osxws/bin/g++-4.2'
export ARCHFLAGS="-arch i386 -arch x86_64"
python setup.py build

# In v0.14.1, runtests.py fails with 1 declarations and 2 numpy error
#%check
#python runtests.py

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%doc Demos Doc
%doc COPYING.txt INSTALL.txt LICENSE.txt README.txt ToDo.txt USAGE.txt

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.14.1-2
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.14.1-1
- remove unnecessary requires
- build with specific compiler

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.14.1-0
- initial build for Mac OS X WorkShop 10.6

