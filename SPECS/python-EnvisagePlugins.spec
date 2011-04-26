Name:           python-EnvisagePlugins
Version:        3.1.3
Release:        2%{?dist}
Summary:        Plug-ins for the Envisage framework
Group:          Development/Libraries
License:        BSD and CC-BY-SA and Python and LGPLv2+
URL:            http://code.enthought.com/projects/envisage_plugins.php
Source0:        http://www.enthought.com/repo/ETS/EnvisagePlugins-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-setuptools, python2-devel, python-setupdocs
Requires:       python-EnvisageCore

%description
The EnvisagePlugins project includes a number of plug-ins for the Envisage
framework that Enthought has found useful for building scientific applications.
Envisage does not require that you use these plug-ins, but you may find them
useful to avoid having to reinvent these particular wheels.

    * Workbench: Provides an application GUI window that supports views and 
      perspectives, similar to the Eclipse IDE.
    * Action: Supports user-interaction command mechanisms, such as toolbars,
      menus, and buttons.
    * Single Project: Supports a project paradigm for saving application data,
      assuming an interaction model in which only one project can be open in 
      the application at a time.
    * Text Editor: Provides a rudimentary text editor interface.
    * Python Shell: Provides an interactive Python shell within a 
      Workbench-based application.
    * Debug: Provides the Frame Based Inspector from the ETSDevTools project as
      an Envisage plug-in.

%prep
%setup -q -n EnvisagePlugins-%{version}

rm -rf *.egg-info

# fix wrong-file-end-of-line-encoding
sed -i 's/\r//' image_LICENSE.txt

for file in `find examples/single_project -name "*.py"`; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc *.txt examples
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/envisage/developer
%{python_sitelib}/enthought/envisage/ui
%{python_sitelib}/enthought/plugins

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.3-1
- Updated to 3.1.3

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> 3.1.2-1
- Update spec to match latest guidelines w.r.t %%clean

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.1-1
- updated to 3.1.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-1
- Updated

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-1
- Initial package
