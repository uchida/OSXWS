%define __python /usr/osxws/bin/python
%define modulename logilab-astng

Summary: rebuild a new abstract syntax tree from Python's ast
Name: python-%{modulename}
Version: 0.21.0
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/l/%{modulename}/%{modulename}-%{version}.tar.gz
License: LGPLv2+
Group: Development/Language
URL: http://www.logilab.org/project/%{name}

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: python-logilab-common
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
The aim of this module is to provide a common base representation of python source code
for projects such as pychecker, pyreverse, pylint...
Well, actually the development of this library is essentially governed by pylint's needs.

It provides a compatible representation which comes from the _ast module.
It rebuilds the tree generated by the builtin _ast module
by recursively walking down the AST and building an extended ast (let's call it astng ;).
The new node classes have additional methods and attributes for different usages.
They include some support for static inference and local name scopes.
Furthermore, astng builds partial trees by inspecting living objects.

Main modules are:

- bases, node_classses and scoped_nodes contain the classes for the different type of nodes of the tree.
- the manager contains a high level object to get astng trees from source files and living objects. It maintains a cache of previously constructed tree for quick access

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{python_sitelib}/*
%doc ChangeLog COPYING COPYING.LESSER README

%changelog
* Wed Dec 22 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.21.0-0
- initial build for Mac OS X WorkShop 10.6

