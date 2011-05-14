Summary: Example data file for VTK
Name: vtkdata
Version: 5.6.1
Release: 0%{?_dist_release}
# This is a variant BSD license, a cross between BSD and ZLIB.
# For all intents, it has the same rights and restrictions as BSD.
# http://fedoraproject.org/wiki/Licensing/BSD#VTKBSDVariant
# This file tree has no indication of license, but upstream confirms it
# is the same as the vtk code.
License: BSD
Group: Development/Libraries
URL: http://www.vtk.org/
Source0: http://www.vtk.org/files/release/5.6/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
Example data file for VTK

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}
cd $RPM_BUILD_ROOT%{_datadir}
tar -zpxf %{SOURCE0}
mv VTKData %{name}-%{version}

# (Verbosely) fix 0555 permissions
find . -type f -perm 0555 -print0 | xargs -0 echo chmod 0755 | sh -x
# Remove execute bits from not-scripts
for file in `find . -type f -perm 0755`; do
    head -1 $file | grep '^#!' > /dev/null && continue
    chmod 0644 $file
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/*

%changelog
* Sat Apr 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.6.1-0
- initial build for Mac OS X WorkShop

