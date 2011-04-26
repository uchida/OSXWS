%define modulename wxPython
%define buildflags WXPORT=mac UNICODE=1
Name:           python-wxPython
Version:        2.8.8.1
Release:        0%{?_dist_release}
Summary:        GUI toolkit for the Python programming language
Group:          Development/Languages
License:        LGPLv2+ and wxWidgets 
URL:            http://www.wxpython.org/
Source0:        http://downloads.sourceforge.net/wxpython/%{modulename}-src-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel

%description
wxPython is a GUI toolkit for the Python programming language. It allows
Python programmers to create programs with a robust, highly functional
graphical user interface, simply and easily. It is implemented as a Python
extension module (native code) that wraps the popular wxWindows cross
platform GUI library, which is written in C++.

%package        doc
Group:          Documentation
Summary:        Documentation and samples for wxPython
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation, samples and demo application for wxPython.

%prep
%setup -q -n %{modulename}-src-%{version}

%build
# Just build the wxPython part, use Mac OS X built-in wxWidget
cd wxPython
# included distutils is not multilib aware; use normal
rm -rf distutils
python setup.py %{buildflags} build

%install
rm -rf $RPM_BUILD_ROOT
cd wxPython
python setup.py %{buildflags} install --root=$RPM_BUILD_ROOT

# remove extraneous files
rm -rf $RPM_BUILD_ROOT/usr/include/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc wxPython/licence
%{python_sitelib}/*

%files doc
%defattr(-,root,wheel)
%doc wxPython/docs wxPython/demo wxPython/samples

%changelog
* Tue Apr 26 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.8.8.1-0
- initial build for Mac OS X WorkShop

