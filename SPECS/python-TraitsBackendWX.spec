%global srcname TraitsBackendWX

Name:		python-TraitsBackendWX
Version:	3.4.0
Release:	4%{?dist}
Summary:	WxPython backend for Traits and TraitsGUI (Pyface)
Group:		Development/Libraries
License:	BSD and EPL and LGPLv2 and LGPLv3 and Public Domain
URL:		http://code.enthought.com/projects/traits_gui
Source0:	http://www.enthought.com/repo/ETS/%{srcname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python2-devel python-setuptools
# TraitsGUI[dock]
Requires:	python-TraitsGUI
# EnthoughtBase[ui] and Traits come with TraitsGUI
Requires:	wxPython
Provides:	python-TraitsBackend = %{version}-%{release}

%description
The TraitsBackendWX project contains an implementation of TraitsGUI 
using wxPython. It provides wx-based support for visualization and 
editing of Traits-based objects.

%prep
%setup -q -n %{srcname}-%{version}

rm -rf *.egg-info

# Convert encoding to UTF-8
for file in *.txt; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

# Remove DOS line endings
for file in *.txt; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

%build
python setup.py build

%install
python setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc *.txt docs/*
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/traits/ui/wx
%{python_sitelib}/enthought/pyface/ui/wx

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> - 3.4.0-3
- Add Provides:python-TraitsBackend

* Mon Jul 26 2010 Chen Lei <supercyper@163.com> - 3.4.0-2
- Remove Requires:python-TraitsBackendWX

* Mon Jul 26 2010 Chen Lei <supercyper@163.com> - 3.4.0-1
- Initial package
