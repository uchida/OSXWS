%define __python /usr/osxws/bin/python
%define modulename pip
%bcond_with doc

Summary: pip installs packages
Name: python-%{modulename}
Version: 0.8.3
Release: 0%{?_dist_release}
Source0: http://pypi.python.org/packages/source/p/%{modulename}/%{modulename}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: python = 2.6.6
Requires: python-devel = 2.6.6
Requires: /usr/osxws/bin/python2.6
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-distribute
URL: http://pip.openplans.org

%description
pip installs packages.  Python packages.

If you use virtualenv -- a tool for installing libraries in a local and isolated manner
-- you'll automatically get a copy of pip.  Free bonus!

Once you have pip, you can use it like this::

    $ pip install SomePackage

SomePackage is some package you'll find on PyPI.
This installs the package and all its dependencies.

pip does other stuff too, with packages, but install is the biggest
one.  You can ``pip uninstall`` too.

You can also install from a URL (that points to a tar or zip file),
install from some version control system (use URLs like
hg+http://domain/repo -- or prefix git+, svn+ etc).  pip
knows a bunch of stuff about revisions and stuff, so if you need to do
things like install a very specific revision from a repository pip can
do that too.

If you've ever used python setup.py develop, you can do something
like that with pip install -e ./ -- this works with packages that
use distutils too (usually this only works with Setuptools
projects).

You can use pip install --upgrade SomePackage to upgrade to a newer version,
or pip install SomePackage==1.0.4 to install a very specific version.

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/pip*
%{python_sitelib}/*
%doc docs/_build/html/*.html

%changelog
* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.8.3-0
- initial build for Mac OS X WorkShop

