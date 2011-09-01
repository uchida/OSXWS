%define python_inc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")
%define python_bin %(%{__python} -c "from distutils.sysconfig import get_config_var; print get_config_var('BINDIR')")
%define python_data %(%{__python} -c "from distutils.sysconfig import get_config_var; print get_config_var('datarootdir')")

%define _qt4_version %(pkg-config --modversion --silence-errors Qt 2>/dev/null || echo 4.7.2)
%define _qt4_prefix %(pkg-config --variable prefix --silence-errors Qt 2>/dev/null || echo %{_libdir}/qt-%{qt4_ver})
%define _qt4_plugindir %(pkg-config --variable plugindir --silence-errors Qt 2>/dev/null || echo %{_qt4_prefix}/plugins)

Name: 	 PyQt4
Summary: Python bindings for Qt4
Summary(ja): Qt4 の Python バインディング
Version: 4.8.4
Release: 3%{?_dist_release}

# GPLv2 exceptions(see GPL_EXCEPTIONS*.txt)
License: GPLv3 or GPLv2 with exceptions
Group: 	 Development/Languages
URL:     http://www.riverbankcomputing.com/software/pyqt/
Source0: http://www.riverbankcomputing.com/static/Downloads/PyQt4/PyQt-mac-gpl-%{version}.tar.gz

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
BuildArch: fat

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

## permissions
# mark examples non-executable
find examples/ -name "*.py" | xargs chmod a-x
chmod a+rx pyuic/uic/pyuic.py

%build
python configure.py --assume-shared \
                    --confirm-license \
                    --no-timestamp \
                    --qmake=%{_bindir}/qmake \
                    --use-arch i386 --use-arch x86_64 \
                    --no-qsci-api \
                    --verbose \
                    CC="/usr/bin/gcc" CXX="/usr/bin/g++"
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL_ROOT=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
for f in pylupdate4 pyrcc4 pyuic4; do
    ln -sf %{python_bin}/$f $RPM_BUILD_ROOT%{_bindir}
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc NEWS README
%doc OPENSOURCE-NOTICE.TXT
%doc LICENSE.GPL2 GPL_EXCEPTION*.TXT
%doc LICENSE.GPL3
%{python_sitearch}/PyQt4/
%exclude %{python_sitearch}/PyQt4/uic/pyuic.py*

%files devel
%defattr(-,root,root,-)
%doc doc/*
%doc examples/
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{python_bin}/pylupdate4
%{python_bin}/pyrcc4
%{python_bin}/pyuic4
%{python_sitearch}/PyQt4/uic/pyuic.py*
%{python_data}/sip/PyQt4/

%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-3
- mofify python requirements for OSXWS

* Sun Jul  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-2
- fix path to qmake
- build with specific compiler

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-1
- make more compatible with Vine Linux

* Wed May  4 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.8.4-0
- initial build for Mac OS X

