%define python_inc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")
Summary: The Visualization Toolkit - A high level 3D visualization library
Name: vtk
Version: 5.6.1
Release: 0%{?_dist_release}
# This is a variant BSD license, a cross between BSD and ZLIB.
# For all intents, it has the same rights and restrictions as BSD.
# http://fedoraproject.org/wiki/Licensing/BSD#VTKBSDVariant
License: BSD
Group: System Environment/Libraries
Source: http://www.vtk.org/files/release/5.6/%{name}-%{version}.tar.gz
Patch0: vtk-5.6.1-netcdf-cxx-version.patch

URL: http://vtk.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: fat
BuildRequires: cmake
BuildRequires: python-devel
BuildRequires: freetype-devel, libjpeg-devel, libpng-devel
BuildRequires: libtiff-devel, zlib-devel
BuildRequires: libxml2-devel
BuildRequires: qt
BuildRequires: doxygen, graphviz
BuildRequires: gnuplot
BuildRequires: wget

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modelling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

%package devel
Summary: VTK header files for building C++ code
Requires: vtk = %{version}-%{release}
Requires: libjpeg-devel, libpng-devel
Requires: libtiff-devel
Group: Development/Libraries

%description devel 
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualisation.

%package tcl
Summary: Tcl bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description tcl
tcl bindings for VTK

%package -n python-%{name}
Summary: Python bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description -n python-%{name}
python bindings for VTK

%package qt
Summary: Qt bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description qt
Qt bindings for VTK

%package testing
Summary: Testing programs for VTK
Requires: vtk = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description testing
Testing programs for VTK

%package examples
Summary: Examples for VTK
Requires: vtk = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description examples
This package contains many well-commented examples showing how to use
VTK. Examples are available in the C++, Tcl, Python and Java
programming languages.

%prep
%setup -q -n VTK

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
export CFLAGS="-D_UNICODE -I%{_includedir}"
export CXXFLAGS="-D_UNICODE -I%{_includedir}"

mkdir build
pushd build
cmake .. \
 -DBUILD_DOCUMENTATION:BOOL=ON \
 -DBUILD_EXAMPLES:BOOL=ON \
 -DBUILD_TESTING:BOOL=ON \
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
 -DCMAKE_OSX_DEPLOYMENT_TARGET=10.6 \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
 -DBUILD_SHARED_LIBS:BOOL=ON \
 -DCMAKE_INSTALL_NAME_DIR:STRING="%{_libdir}/vtk-5.6" \
 -DVTK_PYTHON_SETUP_ARGS="--root=$RPM_BUILD_ROOT"

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

%files -n python-%{name}
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

%files testing -f build/testing.list
%defattr(-,root,wheel)
%{_libdir}/vtk-5.6/testing

%files examples -f build/examples.list
%defattr(-,root,wheel)
%doc vtk-examples-5.6/Examples

%changelog
* Thu May  5 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-1
- fix the version of libvtkNetCDF_cxx

* Wed May  4 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-0
- initial build for Mac OS X WorkShop

