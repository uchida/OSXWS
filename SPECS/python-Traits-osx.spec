Name:           python-Traits
Version:        3.6.0
Release:        3%{?_dist_release}
Summary:        Explicitly typed attributes for Python
Group:          Development/Libraries
# Images have different licenses. For image license breakdown check
# image_LICENSE.txt file. Except enthought/traits/ui/editors_gen.py
# which is GPLv2+ all remaining source or image files are in BSD
# 3-clause license. Confirmed from upstream.
License:        BSD and EPL and LGPLv2 and GPLv2+
URL:            http://code.enthought.com/projects/traits/
Source0:        http://www.enthought.com/repo/ETS/Traits-%{version}.tar.gz
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires:  python-setupdocs, python-setuptools
Requires:       python-numpy
BuildArch:      fat

%description
The traits package developed by Enthought provides a special type
definition called a trait. Although they can be used as normal Python object 
attributes, traits also have several additional characteristics: 

* Initialization: A trait can be assigned a default value.
* Validation: A trait attribute's type can be explicitly declared.
* Delegation: The value of a trait attribute can be contained either
  in another object.
* Notification: Setting the value of a trait attribute can trigger
  notification of other parts of the program.
* Visualization: User interfaces that permit the interactive
  modification of a trait's value can be automatically constructed
  using the trait's definition.

%prep
%setup -q -n Traits-%{version}

rm -rf *.egg-info

# fix wrong-file-end-of-line-encoding
OLDIFS=$IFS
IFS=:
for file in `find examples \( -name "*.py" -o -name "*.desc" -o -name \
 "*.txt" \) -printf "%p$IFS"`; do 
    sed "s|\r||g" $file > $file.new && \
    touch -r $file $file.new && \
    mv $file.new $file
done
IFS=$OLDIFS

for file in *.txt; do
    sed "s|\r||g" $file > $file.new && \
    touch -r $file $file.new && \
    mv $file.new $file
done

# file not utf-8
iconv -f iso8859-1 -t utf-8 image_LICENSE_Eclipse.txt \
 > image_LICENSE_Eclipse.txt.conv && mv -f \
 image_LICENSE_Eclipse.txt.conv image_LICENSE_Eclipse.txt

%build
python setup.py build

%install
python setup.py install --skip-build --root $RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{python_sitearch}/enthought/traits/protocols/_speedups.c
rm $RPM_BUILD_ROOT%{python_sitearch}/enthought/traits/ctraits.c

%files
%defattr(-,root,wheel)
%doc *.txt docs/*.pdf examples
%doc docs/traitsdocreadme.txt docs/CHANGES.txt
%dir %{python_sitearch}/enthought
%{python_sitearch}/*.egg-info
%{python_sitearch}/*.pth
%{python_sitearch}/enthought/traits

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.6.0-3
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.6.0-2
- requires python-setuptools

* Sat May 14 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.6.0-1
- remove absent documents

* Thu May 12 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.6.0-0
- update to 3.6.0

* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.5.0-0
- initial build for Mac OS X WorkShop

