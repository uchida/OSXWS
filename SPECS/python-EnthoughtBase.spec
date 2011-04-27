Name:           python-EnthoughtBase
Version:        3.0.6
Release:        2%{?dist}
Summary:        Core packages for the Enthought Tool Suite
Group:          Development/Libraries
# enthought/util/guid.py and images are LGPLv2+
License:        BSD and LGPLv2+
URL:            http://code.enthought.com/projects/enthought_base.php
Source0:        http://www.enthought.com/repo/ETS/EnthoughtBase-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-setuptools, python2-devel, python-setupdocs

%description

The EnthoughtBase project includes a few core packages that are used
by many other projects in the Enthought Tool Suite:

    * enthought.etsconfig: Supports configuring settings that need to
      be shared across multiple projects or programs on the same
      system.

    * enthought.logger: Provides convenience functions for creating
      logging handlers.

    * enthought.util: Provides miscellaneous utility functions.


%prep
%setup -q -n EnthoughtBase-%{version}

rm -rf *.egg-info

# remove shebang
sed -i '/^#!\//, 1d' enthought/util/guid.py enthought/util/updates/info2xml.py

# fix wrong-file-end-of-line-encoding
sed -i 's/\r//' image_LICENSE.txt

# remove exec permission
find examples -type f -exec chmod 0644 {} ";"

%build
python setup.py build

%install
python setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
 
%files
%defattr(-,root,root,-)
%doc *.txt docs/*.txt examples build/docs/html
%{python_sitelib}/enthought
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.6-1
- Update to 3.0.6

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> 3.0.5-1
- Update spec to match latest guidelines w.r.t %%clean
- Fix several rpmlint warnings

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-1
- Updated to 3.0.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.2-1
- Updated

* Thu Jun 04 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-3
- Added README.fedora

* Tue Mar 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-2
- Included html & examples, fixed license, and removed egg folder

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-1
- Initial package
