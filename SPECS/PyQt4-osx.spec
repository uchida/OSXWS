%define _qt4_version %(pkg-config --modversion --silence-errors Qt 2>/dev/null || echo 4.7.2)
%define _qt4_prefix %(pkg-config --variable prefix --silence-errors Qt 2>/dev/null || echo %{_libdir}/qt-%{qt4_ver})
%define _qt4_plugindir %(pkg-config --variable plugindir --silence-errors Qt 2>/dev/null || echo %{_qt4_prefix}/plugins)

Name: 	 PyQt4
Summary: Python bindings for Qt4
Summary(ja): Qt4 の Python バインディング
Version: 4.9.1
Release: 0%{?_dist_release}

# GPLv2 exceptions(see GPL_EXCEPTIONS*.txt)
License: GPLv3 or GPLv2 with exceptions
Group: 	 Development/Languages
URL:     http://www.riverbankcomputing.com/software/pyqt/
Source0: http://www.riverbankcomputing.com/static/Downloads/PyQt4/PyQt-mac-gpl-%{version}.tar.gz
Patch0: PyQt-4.9.1-fix-py_verion.patch
Patch1: PyQt-4.9.1-fix-QtNetwork.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires: qt4-devel >= 4.5.0
BuildRequires: sip-devel >= 4.12.1
Requires: sip >= 4.12.1
Requires: qt4

%description
These are Python bindings for Qt4.

%package devel
Summary: Files needed to build other bindings based on Qt4
Group:	 Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: sip-devel >= 4.12.1

%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt4 classes (e.g. KDE or your own).


%prep
%setup -q -n PyQt-mac-gpl-%{version}
%patch0 -p1
%patch1 -p1

## permissions
# mark examples non-executable
find examples/ -name "*.py" | xargs chmod a-x
chmod a+rx pyuic/uic/pyuic.py

%build
python configure.py --assume-shared \
                    --confirm-license \
                    --no-timestamp \
                    --qmake=%{_bindir}/qmake \
                    --no-designer-plugin \
                    --verbose
sed -i.gcc 's|gcc|/usr/bin/gcc|g' Makefile
sed -i.gcc 's|g++|/usr/bin/g++|g' Makefile
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel,-)
%doc NEWS README
%doc OPENSOURCE-NOTICE.TXT
%doc LICENSE.GPL2 GPL_EXCEPTION*.TXT
%doc LICENSE.GPL3
%{python_sitearch}/PyQt4/
%exclude %{python_sitearch}/PyQt4/uic/pyuic.py*

%files devel
%defattr(-,root,wheel,-)
%doc doc/*
%doc examples/
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{python_sitearch}/PyQt4/uic/pyuic.py*
%{_datadir}/sip/PyQt4/

%changelog
* Tue Feb 21 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.9.1-0
- update to 4.9.1
- build x86_64 mono arch

* Fri Oct 21 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.5-0
- updat to 4.8.5

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-3
- mofify python requirements for OSXWS

* Sun Jul  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-2
- fix path to qmake
- build with specific compiler

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-1
- make more compatible with Vine Linux

* Wed May  4 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-0
- initial build for Mac OS X

