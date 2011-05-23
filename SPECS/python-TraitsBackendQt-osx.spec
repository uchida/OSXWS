Name:           python-TraitsBackendQt
Version:        3.6.0
Release:        0%{?_dist_release}
Summary:        PyQt backend for Traits and TraitsGUI (Pyface)
Group:          Development/Libraries
# Confirmed from upstream that some files are BSD and most are GPLed
License:        BSD and (GPLv2 or GPLv3 with exceptions)
URL:            http://code.enthought.com/projects/traits_gui
Source0:        http://www.enthought.com/repo/ETS/TraitsBackendQt-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel, python-distribute
Requires:       python-TraitsGUI
# EnthoughtBase and Traits come with TraitsGUI
Requires:       python-PyQt
Provides:       python-TraitsBackend = %{version}-%{release}

%description
The TraitsBackendQt project contains an implementation of TraitsGUI
using PyQt. It provides Qt-based support for visualization and editing
of Traits-based objects.

%prep
%setup -q -n TraitsBackendQt-%{version}

rm -rf *.egg-info

sed -i.tmp 's/\r//' image_LICENSE.txt
rm -f image_LICENSE.txt.tmp

%build
python setup.py build

%install
python setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc *.txt docs/*.txt
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/traits/ui/qt4
%{python_sitelib}/enthought/pyface/ui/qt4

%changelog
* Thu May 12 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.6.0-0
- update to 3.6.0

* Wed May  4 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.5.0-0
- initial build for Mac OS X WorkShop

