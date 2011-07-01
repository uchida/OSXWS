Name: python-markupsafe
Version: 0.12
Release: 1%{?_dist_release}
Summary: Implements a XML/HTML/XHTML Markup safe string for Python

Group: Development/Languages
License: BSD
URL: http://pypi.python.org/pypi/MarkupSafe
Source0: http://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-devel python-setuptools
BuildArch: fat

%description
A library for safe markup escaping.
%prep
%setup -q -n MarkupSafe-%{version}

%build
export CC='/usr/bin/gcc-4.2'
export ARCHFLAGS="-arch i386 -arch x86_64"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root $RPM_BUILD_ROOT
# C code errantly gets installed
rm $RPM_BUILD_ROOT/%{python_sitearch}/markupsafe/*.c

%check
python setup.py test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc AUTHORS LICENSE README.rst
%{python_sitearch}/*

%changelog
* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.12-1
- build with specific compiler

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.12-0
- initial build for Mac OS X WorkShop

