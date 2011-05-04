Name:           python-TraitsBackendQt
Version:        3.5.0
Release:        2%{?dist}
Summary:        PyQt backend for Traits and TraitsGUI (Pyface)
Group:          Development/Libraries
# Confirmed from upstream that some files are BSD and most are GPLed
License:        BSD and (GPLv2 or GPLv3 with exceptions)
URL:            http://code.enthought.com/projects/traits_gui
Source0:        http://www.enthought.com/repo/ETS/TraitsBackendQt-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel, python-setuptools
Requires:       python-TraitsGUI
# EnthoughtBase and Traits come with TraitsGUI
Requires:       PyQt4
Provides:       python-TraitsBackend = %{version}-%{release}

%description
The TraitsBackendQt project contains an implementation of TraitsGUI
using PyQt. It provides Qt-based support for visualization and editing
of Traits-based objects.

%prep
%setup -q -n TraitsBackendQt-%{version}

rm -rf *.egg-info

sed -i 's/\r//' image_LICENSE.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc *.txt docs/*.txt
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/traits/ui/qt4
%{python_sitelib}/enthought/pyface/ui/qt4

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> - 3.5.0-1
- Updated to 3.5.0

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> - 3.4.0-1
- Update spec to match latest guidelines w.r.t %%clean
- Add Provides:python-TraitsBackend

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 3.2.0-1
- Updated to 3.2.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-1
- Updated

* Tue Mar 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-4
- Egg-info directory deleted

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-3
- Fix BuildRequires

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-2
- Fixed the license and confimed by upstream

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-1
- Initial package
