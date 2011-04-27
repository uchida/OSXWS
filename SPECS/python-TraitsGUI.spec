Name:           python-TraitsGUI
Version:        3.5.0
Release:        2%{?dist}
Summary:        Traits-capable windowing framework
Group:          Development/Libraries
# Source code is under BSD but images are under different licenses
# and details are inside image_LICENSE.txt
License:        BSD and EPL and LGPLv2 and LGPLv3 and Public Domain
URL:            http://code.enthought.com/projects/traits_gui/
Source0:        http://www.enthought.com/repo/ETS/TraitsGUI-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel, python-setuptools, python-setupdocs
Requires:       python-EnthoughtBase, python-Traits
Requires:       python-TraitsBackend

%description
The TraitsGUI project contains a toolkit-independent GUI abstraction layer
(known as Pyface), which is used to support the "visualization" features of
the Traits package. Thus, you can write code in terms of the Traits API
(views, items, editors, etc.), and let TraitsGUI and your selected toolkit
and back-end take care of the details of displaying them.
        
To display Traits-based user interfaces, in addition to the TraitsGUI project,
you must install one of the following combinations of packages:
        
    * Traits, TraitsBackendWX, and wxPython
    * Traits, TraitsBackendQt, and PyQt

%prep
%setup -q -n TraitsGUI-%{version}

rm -rf *.egg-info

# fix wrong-file-end-of-line-encoding
sed -i 's/\r//' image_*.txt examples/workbench/*.py \
 examples/workbench/images/image_LICENSE.txt \
 examples/dock/images/image_LICENSE.txt \
 examples/images/image_LICENSE.txt

# file not utf-8
iconv -f iso8859-1 -t utf-8 image_LICENSE_OOo.txt > image_LICENSE_OOo.txt.conv \
 && mv -f image_LICENSE_OOo.txt.conv image_LICENSE_OOo.txt
iconv -f iso8859-1 -t utf-8 image_LICENSE_Eclipse.txt > image_LICENSE_Eclipse.txt.conv \
 && mv -f image_LICENSE_Eclipse.txt.conv image_LICENSE_Eclipse.txt

# remove exec permission
find examples -type f -exec chmod 0644 {} ";"

%build
python setup.py build

%install
python setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc *.txt examples docs/*.txt docs/*.pdf
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/pyface
%{python_sitelib}/enthought/resource
%{python_sitelib}/enthought/traits

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> 3.5.0-1
- Updated to 3.5.0

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> 3.4.0-2
- Add Requires:python-TraitsBackend

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> 3.4.0-1
- Update spec to match latest guidelines w.r.t %%clean
- Remove Requires:python-TraitsBackendQt
- Fix directory ownership

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-1
- Update to 3.1.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.4-4
- Fixed BR: python-setupdocs

* Mon Jun 08 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.4-3
- fixed wrong-file-end-of-line-encoding & spurious-executable-perm
- for files in examples folder

* Sun May 24 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.4-2
- Included examples folder in %%doc
- Changed %%define to %%global and changes %%{__python} to python

* Sat May 02 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.4-1
- Updated to 3.0.4

* Sat May 02 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-2
- Removed egg-info folder already present, removed %%{version}
- from URL.

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-2
- Fixed BuildRequires

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.3-1
- Initial package
