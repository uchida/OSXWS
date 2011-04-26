Name:           python-EnvisageCore
Version:        3.1.3
Release:        2%{?dist}
Summary:        Extensible Application Framework
Group:          Development/Libraries
License:        BSD
URL:            http://code.enthought.com/projects/envisage/
Source0:        http://www.enthought.com/repo/ETS/EnvisageCore-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-setuptools, python2-devel, python-setupdocs
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
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# fix wrong-file-end-of-line-encoding
for file in `find build/docs -name "*.txt"`; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

%files
%defattr(-,root,root,-)
%doc *.txt examples build/docs/html
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.pth
%{python_sitelib}/enthought/envisage

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.3-1
- Updated to latest release.

* Fri Aug 13 2010 Chen Lei <supercyper@163.com> 3.1.2-1
- Update spec to match latest guidelines w.r.t %%clean

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.1-1
- Updated to 3.1.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.1.0-1
- Updated

* Sat May 02 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-2
- Added examples directory to %%doc, Added python-configobj &
- python-AppTools in Requires field.

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.0.1-1
- Initial package
