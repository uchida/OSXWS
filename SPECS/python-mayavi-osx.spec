Name:           python-mayavi
Version:        3.4.1
Release:        5%{?_dist_release}
Summary:        Scientific data 3-dimensional visualizer
Group:          Applications/Edutainment
License:        BSD and EPL and LGPLv2+ and LGPLv2 and LGPLv3
URL:            http://code.enthought.com/projects/mayavi/
Source0:        http://www.enthought.com/repo/ETS/Mayavi-%{version}.tar.gz
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires:  python-setuptools, python-setupdocs
BuildRequires:  python-numpy, vtk-python
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

%package doc
Summary: Documentation files for %{name}
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation files for %{name}.

%prep
%setup -q -n Mayavi-%{version}

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
    iconv -f ISO-8859-1 -t UTF-8 $file > $file.new && \
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

# extract html documents
unzip docs/html.zip

%build
export ARCHFLAGS=""
python setup.py build

%install
export ARCHFLAGS=""
python setup.py install --skip-build --root $RPM_BUILD_ROOT \
                        --install-scripts=%{_bindir} --install-data=%{_prefix}

# remove useless files
rm -f $RPM_BUILD_ROOT%{python_sitearch}/enthought/tvtk/setup.py*
find $RPM_BUILD_ROOT%{python_sitearch}/enthought -name \.buildinfo \
    -type f -print | xargs rm -f -

# remove mayavi2 script
rm -rf $RPM_BUILD_ROOT%{_bindir}/mayavi2

# non-executable-script
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/enthought/mayavi/tests/runtests.py

# move documents
mkdir -p build/docs
mv docs/build/mayavi/html build/docs/mayavi
mv docs/build/tvtk/html build/docs/tvtk

%files
%defattr(-,root,wheel)
%doc *.txt docs/*.txt examples/
%dir %{python_sitearch}/enthought/mayavi
%dir %{python_sitearch}/enthought/tvtk
%{python_sitearch}/enthought/mayavi/[_a-gi-z]*
%{python_sitearch}/enthought/tvtk/[_a-gi-z]*
%{python_sitearch}/*.egg-info
%{python_sitearch}/*.pth
%{_bindir}/tvtk_doc

%files doc
%doc build/docs/*

%changelog
* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.1-5
- build x86_64 mono arch

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.1-4
- mofify python requirements for OSXWS

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.1-3
- build with specific compiler

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.1-2
- change Group: Applications/Edutainment instead of Applications/Engineering

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.1-1
- requires python-setuptools

* Sat May 14 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.1-0
- update to 3.4.1
- remove mayavi2 script does not work with qt4 backend
- fix path to documents

* Thu May  5 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.4.0-0
- initial build for Mac OS X

