Name:           python-AppTools
Version:        3.4.0
Release:        2%{?dist}
Summary:        Enthough Tool Suite Application Tools
Group:          Development/Libraries
License:        BSD and LGPLv2+
URL:            http://code.enthought.com/projects/app_tools.php
Source0:        http://www.enthought.com/repo/ETS/AppTools-%{version}.tar.gz
Source1:        README.fedora.%{name}
BuildArch:      noarch
BuildRequires:  python-setuptools, python2-devel, python-setupdocs
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
cp -p %{SOURCE1} README.fedora

rm -rf *.egg-info

# remove exec permission
find examples -type f -exec chmod 0644 {} ";"

%build
python setup.py build

%install
python setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# remove tests for now
rm -rf $RPM_BUILD_ROOT%{python_sitelib}/integrationtests

%files
%defattr(-,root,root,-)
%doc *.txt examples build/docs/html README.fedora
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/*

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> 3.4.0-1
- Updated to 3.4.0

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> 3.3.2-1
- Update spec to match latest guidelines w.r.t %%clean
- Fix several rpmlint warnings

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> 3.3.0-1
- Updated to 3.3.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-1
- Updated

* Thu Jun 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-4
- Added README.fedora

* Fri Apr 24 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-3
- Removed AppTools.egg-info directory

* Fri Mar 06 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-2
- Included examples in %%doc, added python-TraitsGUI & python-EnthoughtBase
- as Requires. Added html folder.

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-1
- Initial package
