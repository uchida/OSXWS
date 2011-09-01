%define python_inc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")
%define vtkdata_dir %{_datadir}/vtk-data-%{version}

Summary: The Visualization Toolkit - A high level 3D visualization library
Summary: The Visualization Toolkit - ハイレベル3D可視化ライブラリ
Group: System Environment/Libraries
Name: vtk
Version: 5.6.1
Release: 5%{?_dist_release}
Source0: http://www.vtk.org/files/release/5.6/%{name}-%{version}.tar.gz
Source1: http://www.vtk.org/files/release/5.6/%{name}data-%{version}.tar.gz
Patch0: vtk-5.6.1-netcdf-cxx-version.patch
# This is a variant BSD license, a cross between BSD and ZLIB.
# For all intents, it has the same rights and restrictions as BSD.
# http://fedoraproject.org/wiki/Licensing/BSD#VTKBSDVariant
License: BSD
URL: http://vtk.org/

BuildRequires: cmake >= 2.0.0
%if "%{?_dist_release}" == "osx10.6"
BuildRequires: python-devel > 2.6.1
%else
BuildRequires: python-devel
%endif
BuildRequires: freetype-devel, libjpeg-devel, libpng-devel
BuildRequires: libtiff-devel, zlib-devel
BuildRequires: libxml2-devel
BuildRequires: qt4-devel
BuildRequires: doxygen, graphviz
BuildRequires: gnuplot
BuildRequires: wget

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: fat

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modelling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

%description
VTK - the Visualization Toolkit is an object oriented, high
level library that allows one to easily write C++ programs, Tcl,
Python and Java scripts that do 3D visualization.  This package
provides the shared libraries needed to run C++ programs that use VTK.
To compile C++ code that uses VTK you have to install vtk-devel.

VTK enables users to concentrate on their work by providing a
large number of excellent and feature packed high level functions that
do visualization.  The library needs OpenGL to render the graphics and
for Linux machines Mesa is necessary. The terms/copyright can be read
in %{_docdir}/vtk-%{version}-%{release}/README.html. VTK-Linux-HOWTO has
information about using vtk, getting documentataion or help and
instructions on building VTK. This package is relocatable.

%package devel
Summary: VTK header files for building C++ code.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libjpeg-devel, libpng-devel
Requires: libtiff-devel

%description devel
This provides the VTK header files required to compile C++
programs that use VTK to do 3D visualisation.


%package tcl
Summary: Tcl bindings for VTK.
Group: Applications/Edutainment
Requires: %{name} = %{version}-%{release}
Requires: tcl

%description tcl
VTK - the Visualization Toolkit is an object oriented, high level
library that allows one to easily write C++ programs, Tcl, Python and Java
scripts that do 3D visualization.  This package provides the shared
libraries that enable one to use VTK via Tcl scripts.  This version also
provides the vtkTkRenderWindow class. This package does not require the vtk
package to be installed.  The library needs OpenGL to render the graphics and
for Linux machines Mesa is necessary.

The terms/copyright can be read in
%{datadir}/doc/vtk-tcl-%{version}-%{release}/README.html. VTK-Linux-HOWTO has
information about using vtk, getting documentation or help and instructions on
building VTK. This package is relocatable.

%package python
Summary: Python bindings for VTK.
Group: Applications/Edutainment
Requires: %{name} = %{version}-%{release}
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
%else
Requires: python
%endif

%description python 
This provides the shared libraries that enable one to use VTK from
python scripts.  You will need python and vtk installed to use this.
Remember to set your PYTHONPATH variable properly before running your
scripts.

%package qt
Summary: QT VTK widget
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: qt4

%description qt
The vtkQt classes combine VTK and Qt(TM) for X11.

%package examples
Summary: C++, Tcl and Python example programs/scripts for VTK.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description examples
This package contains all the examples from the VTK source.
To compile the C++ examples you will need to install the vtk-devel
package as well. The Python and Tcl examples can be run with the
corresponding packages (vtk-python, vtk-tcl).

%package testing-progs
Summary: Tests programs for VTK.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description testing-progs
This package contains all testing programs from the VTK
source. The source code of these programs can be found in the
vtk-examples package.


%package data
Summary: Data for VTK.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description data
This package contains all the data from the VTKData repository.
These data are required to run various examples from the examples package.

%prep
%setup -q -n VTK
%patch0 -p1

# Replace relative path ../../../VTKData with %{_datadir}/vtkdata-%{version}
# otherwise it will break on symlinks.
grep -rl '\.\./\.\./\.\./\.\./VTKData' . | xargs \
    perl -pi -e's,\.\./\.\./\.\./\.\./VTKData,%{_datadir}/vtkdata-%{version},g'

# Save an unbuilt copy of the Example's sources for %doc
mkdir vtk-examples-5.6
cp -a Examples vtk-examples-5.6
# Don't ship Win32 examples
rm -rf vtk-examples-5.6/Examples/GUI/Win32
find vtk-examples-5.6 -type f | xargs chmod -R a-x

%build
export CC="/usr/bin/gcc-4.2"
export CXX="/usr/bin/g++-4.2"
export CFLAGS="-D_UNICODE -I%{_includedir}"
export CXXFLAGS="-D_UNICODE -I%{_includedir}"

mkdir build
pushd build
cmake .. \
 -DBUILD_DOCUMENTATION:BOOL=ON \
 -DBUILD_EXAMPLES:BOOL=ON \
 -DBUILD_TESTING:BOOL=ON \
 -DVTK_USE_RPATH:BOOL=ON \
 -DCMAKE_INSTALL_RPATH:STRING="%{_libdir}/vtk-5.6" \
 -DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON \
 -DVTK_INSTALL_PREFIX:PATH=%{_prefix} \
 -DCMAKE_BUILD_WITH_INSTALL_RPATH:BOOL=ON \
 -DVTK_INSTALL_INCLUDE_DIR:PATH=/include/vtk \
 -DVTK_INSTALL_LIB_DIR:PATH=/%{_lib}/vtk-5.6 \
 -DVTK_INSTALL_QT_DIR=/%{_lib}/qt4/plugins/designer \
 -DVTK_WRAP_PYTHON:BOOL=ON \
 -DVTK_WRAP_JAVA:BOOL=OFF \
 -DVTK_WRAP_TCL:BOOL=ON \
 -DVTK_USE_QVTK=ON \
 -DVTK_USE_QT=ON \
 -DVTK_USE_CARBON:BOOL=OFF \
 -DVTK_USE_COCOA:BOOL=ON \
 -DCMAKE_OSX_ARCHITECTURES:STRING="i386;x86_64" \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
 -DBUILD_SHARED_LIBS:BOOL=ON \
 -DCMAKE_INSTALL_NAME_DIR:STRING="%{_libdir}/vtk-5.6" \
 -DVTK_PYTHON_SETUP_ARGS="--root=$RPM_BUILD_ROOT" \
 -DPYTHON_EXECUTABLE=%{_bindir}/python2.6 \
 -DPYTHON_INCLUDE_DIR=%{python_inc} \
 -DPYTHON_LIBRARY=%{_libdir}/libpython2.6.dylib \

export DYLD_LIBRARY_PATH=`pwd`/bin
export ARCHFLAGS='-arch i386 -arch x86_64'
make

# Remove executable bits from sources (some of which are generated)
find . -name \*.c -or -name \*.cxx -or -name \*.h -or -name \*.hxx -or \
       -name \*.gif | xargs chmod -x

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT

# Gather list of non-python/tcl libraries
ls $RPM_BUILD_ROOT%{_libdir}/vtk-5.6/*.*.dylib \
  | grep -Ev "(Java|QVTK|PythonD|TCL)" | sed -e"s,^$RPM_BUILD_ROOT,," > libs.list
ls $RPM_BUILD_ROOT%{_libdir}/vtk-5.6/lib*cxx.dylib \
  | grep -Ev "(Java|QVTK|PythonD|TCL)" | sed -e"s,^$RPM_BUILD_ROOT,," >> libs.list

pushd $RPM_BUILD_ROOT%{python_sitelib}/vtk
for l in *.so; do
     for old in `otool -L $l|grep $RPM_BUILD_DIR/VTK/build/bin|cut -f1 -d' '`; do
         new=`echo $old|sed -e "s,$RPM_BUILD_DIR/VTK/build/bin,%{_libdir}/vtk-5.6/,g"`
         install_name_tool -change $old $new $l
     done
done
popd

tar zxvf %{SOURCE1}
install -d $RPM_BUILD_ROOT%{_datadir}
cp -r VTKData $RPM_BUILD_ROOT/%{vtkdata_dir}
# (Verbosely) fix 0555 permissions
find $RPM_BUILD_ROOT%{vtkdata_dir} -type f -perm 0555 -print0 | xargs -0 echo chmod 0755 | sh -x
# Remove execute bits from not-scripts
for file in `find $RPM_BUILD_ROOT%{vtkdata_dir} -type f -perm 0755`; do
    head -1 $file | grep '^#!' > /dev/null && continue
    chmod 0644 $file
done

# List of executable utilities
cat > utils.list << EOF
vtkEncodeString
lproj
EOF

# List of executable examples
cat > examples-bin.list << EOF
HierarchicalBoxPipeline
MultiBlock
Arrays
Cube
RGrid
SGrid
Medical1
Medical2
Medical3
finance
Cone
Cone2
Cone3
Cone4
Cone5
Cone6
EOF

# List of executable example, these are Mac Application
cat > examples-app.list << EOF
AmbientSpheres.app
Cylinder.app
DiffuseSpheres.app
SpecularSpheres.app
EOF

# List of executable test binaries
cat > testing.list << EOF
CommonCxxTests
TestCxxFeatures
TestInstantiator
FilteringCxxTests
GraphicsCxxTests
GenericFilteringCxxTests
ImagingCxxTests
IOCxxTests
RenderingCxxTests
VTKBenchMark
VolumeRenderingCxxTests
WidgetsCxxTests
EOF

# Install utils, too
for filelist in utils.list examples-bin.list testing.list; do
  for file in `cat $filelist`; do
    cp -a bin/$file $RPM_BUILD_ROOT%{_bindir}
  done
  perl -pi -e's,^,%{_bindir}/,' $filelist
done

mkdir -p $RPM_BUILD_ROOT%{_appdirmac}/VTK-examples
for file in `cat examples-app.list`; do
   cp -a bin/$file $RPM_BUILD_ROOT%{_appdirmac}/VTK-examples
done
perl -pi -e's,^,%{_appdirmac}/VTK-examples/,' examples-app.list

cat examples-bin.list examples-app.list > examples.list

# Main package contains utils and core libs
cat libs.list utils.list > main.list
popd

# Remove exec bit from non-scripts and %%doc
for file in `find $RPM_BUILD_ROOT -type f -perm 0755 -print0\
  | xargs -0 file | grep ASCII | awk -F: '{print $1}'`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done
find Utilities/Upgrading -type f | xargs chmod -x

# Verdict places the docs in the false folder
rm -fr $RPM_BUILD_ROOT%{_libdir}/vtk-5.6/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files -f build/main.list
%defattr(-,root,wheel)
%doc Copyright.txt README.html vtkLogo.jpg vtkBanner.gif Wrapping/*/README*

%files devel
%defattr(-,root,wheel)
%doc Utilities/Upgrading
%{_libdir}/vtk-5.6/doxygen
%{_includedir}/vtk
%{_libdir}/vtk-5.6/*.dylib
%{_libdir}/vtk-5.6/CMake
%{_libdir}/vtk-5.6/*.cmake
%{_libdir}/vtk-5.6/hints

%files tcl
%defattr(-,root,wheel)
%{_libdir}/vtk-5.6/*TCL*.dylib
%{_bindir}/vtk
%{_bindir}/vtkWrapTcl
%{_bindir}/vtkWrapTclInit
%{_libdir}/vtk-5.6/pkgIndex.tcl
%{_libdir}/vtk-5.6/tcl

%files python
%defattr(-,root,wheel)
%{python_sitearch}/*
%{_libdir}/vtk-5.6/*PythonD*.dylib
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit

%files qt
%defattr(-,root,wheel)
%{_libdir}/vtk-5.6/libQVTK.*.dylib
%{_libdir}/qt4/plugins/designer

%files testing-progs -f build/testing.list
%defattr(-,root,wheel)
%{_libdir}/vtk-5.6/testing

%files examples -f build/examples.list
%defattr(-,root,wheel)
%doc vtk-examples-5.6/Examples

%files data
%defattr(-,root,wheel)
%{vtkdata_dir}


%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-5
- mofify python requirements for OSXWS

* Wed Aug 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-4
- use RPATH for dynamic linking

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-3
- change Group: Applications/Edutainment instead of Applications/Engineering

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-2
- make more compatible with Vine Linux

* Thu May  5 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-1
- fix the version of libvtkNetCDF_cxx

* Wed May  4 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-0
- initial build for Mac OS X WorkShop

