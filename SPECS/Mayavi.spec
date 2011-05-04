Name:           Mayavi
Version:        3.4.0
Release:        2%{?dist}
Summary:        Scientific data 3-dimensional visualizer
Group:          Applications/Engineering
License:        BSD and EPL and LGPLv2+ and LGPLv2 and LGPLv3
URL:            http://code.enthought.com/projects/mayavi/
Source0:        http://www.enthought.com/repo/ETS/%{name}-%{version}.tar.gz
Source1:        mayavi2.desktop
BuildRequires:  python2-devel, python-setuptools, python-setupdocs
BuildRequires:  numpy, vtk-python, desktop-file-utils 
Requires:       vtk-python, python-AppTools
# EnthoughtBase, Traits[ui] and numpy come with TraitsGUI
# TraitsGUI comes with AppTools
Requires:       python-EnvisageCore, python-EnvisagePlugins

%description
The Mayavi project includes two related packages for 3-dimensional 
visualization:

 * Mayavi2: A tool for easy and interactive visualization of data.
 * TVTK: A Traits-based wrapper for the Visualization Toolkit, a
   popular open-source visualization library.

These operate at different levels of abstraction. TVTK manipulates
visualization objects, while Mayavi2 lets you operate on your data,
and then see the results. Most users either use the Mayavi user
interface or program to its scripting interface; you probably don't
need to interact with TVTK unless you want to create a new Mayavi
module.

%prep
%setup -q -n %{name}-%{version}

rm -rf *.egg-info

# fix wrong-file-end-of-line-encoding
for file in *.txt examples/mayavi/data/room_vis.wrl examples/tvtk/dscene.py \
 examples/mayavi/interactive/wx_mayavi_embed*.py ; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

# file-not-utf8
for file in *.txt docs/*.txt; do
 iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
 touch -r $file $file.new && \
 mv $file.new $file
done

# remove shebang
for file in enthought/mayavi/scripts/*.py; do
 sed '/^#!\//, 1d' $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

# remove exec permission
find examples -type f -exec chmod 0644 {} ";"
chmod 0644 enthought/mayavi/tests/data/cellsnd.ascii.inp

%build
CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
python setup.py install --skip-build --root $RPM_BUILD_ROOT

# remove useless files
rm -f $RPM_BUILD_ROOT%{python_sitearch}/enthought/tvtk/setup.py*
find $RPM_BUILD_ROOT%{python_sitearch}/enthought -name \.buildinfo \
 -type f -print | xargs rm -f -

# fix wrong-file-end-of-line-encoding
for file in $RPM_BUILD_ROOT%{python_sitearch}/enthought/mayavi/html/_downloads/wx_mayavi*.py; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

# non-executable-script
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/enthought/mayavi/tests/runtests.py

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
cp -p docs/mayavi2.man $RPM_BUILD_ROOT/%{_mandir}/man1/mayavi2.1

desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/
install -p -m 644 ./docs/source/mayavi/images/mayavi2-48x48.png \
 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/mayavi2.png

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%doc *.txt docs/*.txt examples/
#doc build/docs/html
%dir %{python_sitearch}/enthought/mayavi
%dir %{python_sitearch}/enthought/tvtk
%doc %{python_sitearch}/enthought/mayavi/html
%doc %{python_sitearch}/enthought/tvtk/html
%{python_sitearch}/enthought/mayavi/[_a-gi-z]*
%{python_sitearch}/enthought/tvtk/[_a-gi-z]*
%{python_sitearch}/*.egg-info
%{python_sitearch}/*.pth
%{_bindir}/mayavi2
%{_bindir}/tvtk_doc
%{_mandir}/man1/mayavi2.1.*
%{_datadir}/applications/mayavi2.desktop
%{_datadir}/icons/hicolor/48x48/apps/mayavi2.png

%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> 3.4.0-1
- Updated to 3.4.0

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> 3.3.2-1
- Update spec to match latest guidelines w.r.t %%clean
- Remove explict dependency on python-TraitsBackendQt.spec
- Rename man page(Mayavi -> mayavi2)
- Remove docs src
- Remove tvtk_doc.desktop to avoid confusion
- Fix timestampes for example files

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> 3.3.0-1
- Updated to 3.2.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-6
- Fixed BR, and removed .template & .static directories from docs/source
- Included missing icon from .desktop

* Fri Jun 26 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-5
- Using mayavi2-48x48.png has icons for both .desktop files
- Added Categories to .desktop files

* Thu Jun 25 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-4
- Removed wrong scriplets and corrected 'commets' in
-  tvtk_doc.desktop file.

* Wed Jun 24 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-3
- Fixed license issue and group tag
- Added a .desktop file

* Mon Jun 15 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-3
- included man page, adjusted description, removed useless BR's,
- fixed owned directory issue, cleaned up spec

* Fri Jun 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-2
- Saving timestamp, and fixed indentation

* Fri Jun 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.2.0-1
- Updated

* Wed Jun 10 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-3
- Changed name to Mayavi

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-2
- Fixed description.

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-1
- Initial package
