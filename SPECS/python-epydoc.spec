%define __python /usr/osxws/bin/python
%define modulename epydoc

Summary: Edward Loper's API Documentation Generation Tool
Name: python-%{modulename}
Version: 3.0.1
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/e/%{modulename}/%{modulename}-%{version}.tar.gz
# http://sourceforge.net/tracker/?func=detail&aid=3027939&group_id=32455&atid=405620
Patch0: logilab-docutils.patch
License: MIT
Group: Development/Language
URL: http://epydoc.sourceforge.net/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
Epydoc is a tool for generating API documentation documentation for Python modules,
based on their docstrings. For an example of epydoc's output,
see the API documentation for epydoc itself (html, pdf).
A lightweight markup language called epytext can be used to format docstrings,
and to add information about specific fields, such as parameters and instance variables.
Epydoc also understands docstrings written in reStructuredText, Javadoc, and plaintext.
For a more extensive example of epydoc's output, see the API documentation for Python 2.5.

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%{_mandir}/man1/*.1*
%doc doc/*

%changelog
* Wed Dec 22 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.0.1-0
- initial build for Mac OS X WorkShop 10.6

