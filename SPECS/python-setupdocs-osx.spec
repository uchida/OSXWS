%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-setupdocs
Version:        1.0.5
Release:        1%{?_dist_release}
Summary:        Setuptools plugin
Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/setupdocs
Source0:        http://pypi.python.org/packages/source/s/setupdocs/SetupDocs-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel, python-setuptools
Requires:       python-setuptools
Requires:       python-sphinx

%description
Python setuptools plugin that automates building of docs from ReST source.

%prep
%setup -q -n SetupDocs-%{version}
sed -i.bak 's/\#\!.*$//' setupdocs/setupdocs.py
rm -f setupdocs/setupdocs.py.bak
rm -rf setupdocs.egg-info

%build
python setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,wheel)
%doc *.txt
%{python_sitelib}/*


%changelog
* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.5-1
- requires python-setuptools

* Tue Apr 26 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.5-0
- initial build for Mac OS X WorkShop

