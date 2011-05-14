%define _qt4_prefix %{_libdir}/qt4
%define _qt4_plugindir %{_qt4_prefix}/plugins
%define python_inc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")
%define python_bin %(%{__python} -c "from distutils.sysconfig import get_config_var; print get_config_var('BINDIR')")
%define python_data %(%{__python} -c "from distutils.sysconfig import get_config_var; print get_config_var('datarootdir')")

Summary: Python bindings for Qt4
Name: python-PyQt
Version: 4.8.4
Release: 0%{?_dist_release}
# GPLv2 exceptions(see GPL_EXCEPTIONS*.txt)
License: GPLv3 or GPLv2 with exceptions
Group:   Development/Languages
Url:     http://www.riverbankcomputing.com/software/pyqt/
Source0: http://www.riverbankcomputing.com/static/Downloads/PyQt4/PyQt-mac-gpl-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python-devel
BuildRequires: qt
BuildRequires: python-sip
BuildArch: fat

%description
These are Python bindings for Qt4.

%prep
%setup -q -n PyQt-mac-gpl-%{version}

# change permissions of examples to non-executable
find examples/ -name "*.py" | xargs chmod a-x
chmod a+rx pyuic/uic/pyuic.py

%build
python configure.py --assume-shared \
                    --confirm-license \
                    --no-timestamp \
                    --qmake=%{_bindir}/qmake \
                    --use-arch i386 --use-arch x86_64 \
                    --verbose 
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
%defattr(-,root,wheel)
%doc NEWS README
%doc OPENSOURCE-NOTICE.TXT
%doc LICENSE.GPL2 GPL_EXCEPTION*.TXT
%doc LICENSE.GPL3
%{python_sitearch}/PyQt4/
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{python_bin}/pylupdate4
%{python_bin}/pyrcc4
%{python_bin}/pyuic4
%{python_data}/sip/PyQt4/
%doc doc/*
%doc examples/

%changelog
* Wed May  4 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.12.1-0
- initial build for Mac OS X

