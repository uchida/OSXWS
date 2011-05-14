Name:           python-AppTools
Version:        3.4.1
Release:        0%{?_dist_release}
Summary:        Enthough Tool Suite Application Tools
Group:          Development/Libraries
License:        BSD and LGPLv2+
URL:            http://code.enthought.com/projects/app_tools.php
Source0:        http://www.enthought.com/repo/ETS/AppTools-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-distribute, python-devel, python-setupdocs
Requires:       python-TraitsGUI, python-configobj
# EnthoughtBase, Traits[ui] and numpy come with TraitsGUI

%description
The AppTools project includes a set of packages that Enthought has
found useful in creating a number of applications. They implement
functionality that is commonly needed by many applications

    * enthought.appscripting: Framework for scripting applications.

    * enthought.help: Provides a plugin for displaying documents and
      examples and running demos in Envisage Workbench applications.

    * enthought.io: Provides an abstraction for files and folders in a
      file system.

    * enthought.naming: Manages naming contexts, supporting non-string
      data types and scoped preferences

    * enthought.permissions: Supports limiting access to parts of an
      application unless the user is appropriately authorised (not
      full-blown security).

and many more.

%prep
%setup -q -n AppTools-%{version}

rm -rf *.egg-info

# remove exec permission
find examples -type f -exec chmod 0644 {} ";"

%build
python setup.py build
pushd docs
make html
popd

%install
python setup.py install --skip-build --root $RPM_BUILD_ROOT

# remove tests for now
rm -rf $RPM_BUILD_ROOT%{python_sitelib}/integrationtests

%files
%defattr(-,root,wheel)
%doc *.txt examples docs/build/html
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/*

%changelog
* Tue Apr 26 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.0-0
- initial build for Mac OS X WorkShop

