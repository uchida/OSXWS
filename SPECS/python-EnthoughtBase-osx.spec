Name:           python-EnthoughtBase
Version:        3.1.0
Release:        3%{?_dist_release}
Summary:        Core packages for the Enthought Tool Suite
Group:          Development/Libraries
# enthought/util/guid.py and images are LGPLv2+
License:        BSD and LGPLv2+
URL:            http://code.enthought.com/projects/enthought_base.php
Source0:        http://www.enthought.com/repo/ETS/EnthoughtBase-%{version}.tar.gz
BuildArch:      noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires:  python-setuptools, python-setupdocs

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
sed -i.bak '/^#!\//, 1d' enthought/util/guid.py enthought/util/updates/info2xml.py
rm -f '/^#!\//, 1d' enthought/util/guid.py enthought/util/updates/info2xml.py.bak

# fix wrong-file-end-of-line-encoding
sed -i.bak 's/\r//' image_LICENSE.txt
rm image_LICENSE.txt.bak

# remove exec permission
find examples -type f -exec chmod 0644 {} ";"

%build
python setup.py build

%install
python setup.py install --skip-build --root $RPM_BUILD_ROOT
 
%files
%defattr(-,root,wheel)
%doc *.txt docs/*.txt examples
%{python_sitelib}/enthought
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.1.0-3
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.1.0-2
- requires python-setuptools

* Sat May 14 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.1.0-1
- fix path to documents

* Thu May 12 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.1.0-0
- update to 3.1.0

* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.0.6-0
- initial build for Mac OS X WorkShop

