Name:           python-TraitsGUI
Version:        3.5.0
Release:        0%{?_dist_release}
Summary:        Traits-capable windowing framework
Group:          Development/Libraries
# Source code is under BSD but images are under different licenses
# and details are inside image_LICENSE.txt
License:        BSD and EPL and LGPLv2 and LGPLv3 and Public Domain
URL:            http://code.enthought.com/projects/traits_gui/
Source0:        http://www.enthought.com/repo/ETS/TraitsGUI-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel, python-distribute, python-setupdocs
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
for f in image_*.txt examples/workbench/*.py examples/workbench/images/image_LICENSE.txt \
         examples/dock/images/image_LICENSE.txt examples/images/image_LICENSE.txt; do
    sed -i.bak 's/\r//' $f && rm -f $f.bak
done

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
python setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc *.txt examples docs/*.txt docs/*.pdf
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/pyface
%{python_sitelib}/enthought/resource
%{python_sitelib}/enthought/traits

%changelog
* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.5.0-0
- initial build for Mac OS X WorkShop

