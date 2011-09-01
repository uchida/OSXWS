Name:           python-EnvisageCore
Version:        3.2.0
Release:        3%{?_dist_release}
Summary:        Extensible Application Framework
Group:          Development/Libraries
License:        BSD
URL:            http://code.enthought.com/projects/envisage/
Source0:        http://www.enthought.com/repo/ETS/EnvisageCore-%{version}.tar.gz
BuildArch:      noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires:  python-setuptools, python-setupdocs
Requires:       python-AppTools
# EnthoughtBase and Traits come with AppTools

%description
Envisage is a Python-based framework for building extensible applications,
that is, applications whose functionality can be extended by adding "plug-ins".
Envisage provides a standard mechanism for features to be added to an
application, whether by the original developer or by someone else. In fact,
when you build an application using Envisage, the entire application consists
primarily of plug-ins. In this respect, it is similar to the Eclipse and
Netbeans frameworks for Java applications.

%prep
%setup -q -n EnvisageCore-%{version}

rm -rf *.egg-info

%build
python setup.py build
pushd docs
make html
popd

%install
python setup.py install --skip-build --root $RPM_BUILD_ROOT

# fix wrong-file-end-of-line-encoding
for file in `find docs/build -name "*.txt"`; do
    sed "s|\r||g" $file > $file.new && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%files
%defattr(-,root,wheel)
%doc *.txt examples docs/build/html
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/envisage

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.2.0-3
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.2.0-2
- requires python-setuptools

* Sat May 14 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.2.0-1
- fix path of wrong-file-end-of-line-encoding

* Wed Apr 27 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.2.0-0
- update to 3.2.0

* Tue Apr 26 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.1.3-0
- initilal build for Mac OS X WorkShop 10.6

