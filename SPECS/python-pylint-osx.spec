%define modulename pylint

Summary: python code static checker
Name: python-%{modulename}
Version: 0.22.0
Release: 2%{?_dist_release}
Source0: http://pypi.python.org/packages/source/p/%{modulename}/%{modulename}-%{version}.tar.gz
License: GPLv2
Group: Development/Languages
URL: http://www.logilab.org/project/pylint

Requires: python
Requires: python-logilab-common python-logilab-astng
BuildRequires: python-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
analyzes Python source code looking for bugs and signs of poor quality.

Pylint is a python tool that checks if a module satisfies a coding standard.
Pylint is similar to PyChecker but offers more features, like checking line-code's length,
checking if variable names are well-formed according to your coding standard,
or checking if declared interfaces are truly implemented, and much more (see the complete check list).

The big advantage with Pylint is that it is highly configurable, customizable, and you can easily write a small plugin to add a personal feature.

Pylint is shipped with Pyreverse which creates UML diagrams for python code

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
emacs_lisp_dir=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/pylint
mkdir -p $emacs_lisp_dir
mkdir -p $emacs_lisp_dir
install elisp/pylint*.el $emacs_lisp_dir
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/emacs/site-lisp/pylint
%{_mandir}/man1/*.1*
%doc examples
%doc ChangeLog COPYING README
%doc doc

%changelog
* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.22.0-2
- remove unnecessary requires

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.22.0-1
- fix type in Group

* Wed Dec 22 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.22.0-0
- initial build for Mac OS X WorkShop 10.6

