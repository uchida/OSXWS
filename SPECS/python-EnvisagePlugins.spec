Name:           python-EnvisagePlugins
Version:        3.2.0
Release:        0%{?_dist_release}
Summary:        Plug-ins for the Envisage framework
Group:          Development/Libraries
License:        BSD and CC-BY-SA and Python and LGPLv2+
URL:            http://code.enthought.com/projects/envisage_plugins.php
Source0:        http://www.enthought.com/repo/ETS/EnvisagePlugins-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-distribute, python-devel, python-setupdocs
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
sed -i.bak 's/\r//' image_LICENSE.txt
rm -f image_LICENSE.txt.bak

for file in `find examples/single_project -name "*.py"`; do
    sed "s|\r||g" $file > $file.new && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
python setup.py build

%install
python setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc *.txt examples
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/envisage/developer
%{python_sitelib}/enthought/envisage/ui
%{python_sitelib}/enthought/plugins

%changelog
* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.2.0-0
- update to 3.2.0

* Tue Apr 26 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.1.3-0
- initial build for Mac OS X WorkShop

