%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-setupdocs
Version:        1.0.5
Release:        2%{?dist}
Summary:        Setuptools plugin

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/setupdocs
Source0:        http://pypi.python.org/packages/source/s/setupdocs/SetupDocs-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
Requires:       python-setuptools

%description
Python setuptools plugin that automates building of docs from ReST source.

%prep
%setup -q -n SetupDocs-%{version}
sed -i 's/\#\!.*$//' setupdocs/setupdocs.py
rm -rf setupdocs.egg-info

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc *.txt
%{python_sitelib}/*


%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Rakesh Pandit <rakesh@fedoraproject.org> 1.0.5-1
- Updated to 1.0.5

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 03 2010 Rakesh Pandit <rakesh@fedoraproject.org> 1.0.4-1
- Updated to 1.0.4

* Sun Jan 31 2010 Rakesh Pandit <rakesh@fedoraproject.org> 1.0.3-1
- Updated to 1.0.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.0.1-3
- Removed already existing eggs so that new eggs info files are build
- from source.

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.0.1-2
- Improved description and cleaned some futile information
- Corrected URL

* Tue Jan 27 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.0.1-1
- Initial package
