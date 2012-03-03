%define modulename readline

Name:		python-%{modulename}
Version:    6.2.2
Release:    0%{?_dist_release}
Summary:	The standard Python readline extension linked against the GNU readline library.

Group:		Development/Languages
License:	GPLv3
URL:		http://github.com/ludwigschwardt/python-readline
Source0:	http://pypi.python.org/packages/source/r/%{modulename}/%{modulename}-%{version}.tar.gz
Patch0:     python-readline-osxws.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires: readline
BuildRequires: python-setuptools
Requires: python-setuptools

%description
The readline extension module in the standard library of Mac "system" Python
uses NetBSD's `editline`_ (libedit) library instead, which is a readline
replacement with a less restrictive software license.

As the alternatives to GNU readline do not have fully equivalent functionality,
it is useful to add proper readline support to these platforms. This module
achieves this by bundling the standard Python readline module with the GNU
readline source code, which is compiled and statically linked to it. The end
result is a package which is simple to install and requires no extra shared
libraries.

%prep
%setup -q -n %{modulename}-%{version}
%patch0 -p1
rm -rf rl

%build
export ARCHFLAGS=''
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
export ARCHFLAGS=''
python setup.py install --skip-build --root=$RPM_BUILD_ROOT \
                        --install-scripts=%{_bindir} --install-data=%{_prefix} \

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc NEWS.rst README.rst
%{python_sitelib}/%{modulename}-%{version}-py%{pyver}.egg-info
%{python_sitelib}/%{modulename}.so

%changelog
* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 6.2.2-0
- initial build for Mac OS X WorkShop 10.6

