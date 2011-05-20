%define __python /usr/osxws/bin/python
%define modulename logilab-common

Summary: collection of low-level Python packages and modules used by Logilab projects
Name: python-%{modulename}
Version: 0.55.2
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/l/%{modulename}/%{modulename}-%{version}.tar.gz
License: LGPLv2+
Group: Development/Languages
URL: http://www.logilab.org/project/%{name}

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-epydoc
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
This package contains some modules used by differents Logilab's projects.
There is no documentation available yet but the source code should be clean and well documented.
Designed to ease:

- handling command line options and configuration files
- writing interactive command line tools
- manipulation of files and character strings
- manipulation of common structures such as graph, tree, and pattern such as visitor
- generating text and HTML reports
- accessing some external libraries such as OmniORB, Pyro...
- more...


%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build
pushd doc
make
popd

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp doc/pytest.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%{_bindir}/*
%{_mandir}/man1/*
%doc ChangeLog COPYING COPYING.LESSER README
%doc doc/apidoc

%changelog
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.55.2
- update to 0.55.2

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.53.0-1
- initial build for Mac OS X WorkShop 10.6

