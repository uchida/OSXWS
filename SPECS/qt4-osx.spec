# See http://bugzilla.redhat.com/196901
%define _qt4 %{name}
%define _qt4_prefix %{_libdir}/qt4
%define _qt4_bindir %{_qt4_prefix}/bin
# _qt4_datadir is not multilib clean, and hacks to workaround that breaks stuff.
%define _qt4_datadir %{_qt4_prefix}
%define _qt4_demosdir %{_qt4_prefix}/demos
%define _qt4_docdir %{_docdir}/qt4
%define _qt4_examplesdir %{_qt4_prefix}/examples
%define _qt4_headerdir %{_includedir}
%define _qt4_importdir %{_qt4_prefix}/imports
%define _qt4_libdir %{_libdir}
%define _qt4_plugindir %{_qt4_prefix}/plugins
%define _qt4_sysconfdir %{_sysconfdir}
%define _qt4_translationdir %{_datadir}/qt4/translations

# check root File system is case sensitive or not
%define case_sensitive %(diskutil info / | grep 'Case-sensitive')

Summary: Qt Tool Kit
Name: qt4
Version: 4.7.2
Release: 3%{?_dist_release}
Source0: http://get.qt.nokia.com/qt/source/qt-everywhere-opensource-src-%{version}.tar.gz
# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and ASL 2.0 and BSD and FTL and MIT
Group: System Environment/Libraries
URL: http://www.qtsoftware.com/
BuildRequires: zlib-devel, libtiff-devel, libpng-devel, libjpeg-devel
# For Mac OS X non-Case sensitive HFS+ system,
# conflicts with event.h in libevent and Event.h in qt4
%if "%{case_sensitive}" == ""
BuildConflicts: libevent-devel
%endif
BuildConflicts: pcre-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat
# Provides packages for compatibility
Provides: qt %{name}-devel %{name}-config %{name}-Designer %{name}-tools
Provides: WebKit-qt WebKit-qt-devel
# Provides framework
Provides: QtCore QtGui QtNetwork QtMultimedia 
Provides: QtScript QtScriptTools
Provides: QtOpenGL QtTest QtSvg
Provides: QtXml QtXmlPatterns QtSql
Provides: QtDesigner QtDesignerComponents
Provides: QtHelp QtDeclarative Qt3Support
Provides: QtWebKit

%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package demos
Summary: Demonstration applications for %{name}
Group:   Documentation 
Requires: %{name} = %{version}-%{release}
%description demos
%{summary}.

%package doc
Summary: API documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch 
%description doc
%{summary}.

%package examples
Summary: Programming examples for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
%description examples
%{summary}.

%package sqlite
Summary: SQLite driver for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description sqlite
%{summary}.

%prep
%setup -q -n qt-everywhere-opensource-src-%{version}

%build
export CC='/usr/bin/gcc-4.2'
export CXX='/usr/bin/g++-4.2'
./configure -confirm-license -release -opensource -shared \
            -prefix %{_qt4_prefix} -bindir %{_qt4_bindir} \
            -datadir %{_qt4_datadir} -demosdir %{_qt4_demosdir} \
            -docdir %{_qt4_docdir} -examplesdir %{_qt4_examplesdir} \
            -headerdir %{_qt4_headerdir} -libdir %{_qt4_libdir} \
            -plugindir %{_qt4_plugindir} -sysconfdir %{_qt4_sysconfdir} \
            -translationdir %{_qt4_translationdir} \
            -openssl-linked -xmlpatterns \
            -arch "i386 x86_64" \
            -I/usr/X11/include -L/usr/X11/lib \
            -I%{_includedir} -L%{_libdir} \
            -no-ssse3 -no-sse4.1 -no-sse4.2 \
            -no-dbus -no-phonon -no-pch
make

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL_ROOT=$RPM_BUILD_ROOT

# make symbolic link to %{_qt4_bindir}
mkdir -p $RPM_BUILD_ROOT%{_appdirmac}/Qt4/
mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_qt4_bindir}
for i in * ; do
    case "${i}" in
      Assistant.app|Designer.app|Linguist.app|QMLViewer.app|qtdemo.app|pixeltool.app|qhelpconverter.app|qttracereplay.app)
        ln -sf %{_qt4_bindir}/${i} $RPM_BUILD_ROOT%{_appdirmac}/Qt4
        ;;
    *)
        ln -sf %{_qt4_bindir}/${i} $RPM_BUILD_ROOT%{_bindir}/${i}
        ;;
  esac
done
popd

# remove extraneous build information
rm -f $RPM_BUILD_ROOT%{_qt4_libdir}/*.la
for f in `find $RPM_BUILD_ROOT%{_qt4libdir} -name '*.prl'`; do
    sed -i.tmp "s|-L$RPM_BUILD_DIR/qt-everywhere-opensource-src-%{version}/lib||g" $f
    rm -f $f.tmp
done

# move docs
mv $RPM_BUILD_ROOT%{_docdir} $RPM_BUILD_DIR/qt-everywhere-opensource-src-%{version}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_qt4_headerdir}/QtUiTools
%{_bindir}/*
%{_qt4_bindir}/*
%exclude %{_qt4_bindir}/qtdemo.app
%{_appdirmac}/Qt4/*
%exclude %{_appdirmac}/Qt4/qtdemo.app
%{_qt4_libdir}/libQt*
%{_qt4_libdir}/*.framework
%{_qt4_libdir}/pkgconfig/*
%{_qt4_importdir}/*
%{_qt4_plugindir}/*
%exclude %{_qt4_plugindir}/sqldrivers/libqsqlite.dylib
%exclude %{_qt4_demosdir}
%exclude %{_qt4_examplesdir}
%{_qt4_prefix}/mkspecs
%{_qt4_prefix}/phrasebooks
%{_qt4_prefix}/q3porting.xml
%{_qt4_translationdir}
%doc changes-4.7.2 INSTALL README
%doc LGPL_EXCEPTION.txt LICENSE.FDL LICENSE.GPL3 LICENSE.LGPL

%files demos
%defattr(-,root,wheel)
%{_qt4_bindir}/qtdemo.app
%{_qt4_demosdir}

%files doc
%defattr(-,root,wheel)
%doc docs/*

%files examples
%defattr(-,root,wheel)
%{_qt4_examplesdir}

%files sqlite
%defattr(-,root,wheel)
%{_qt4_plugindir}/sqldrivers/libqsqlite*

%changelog
* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.7.2-3
- build with specific compiler

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.7.2-2
- change the package name from qt to qt4
- provides including packages

* Fri May 20 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.7.2-1
- fix dependency problem with QtWebKit framework

* Wed May  4 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 4.7.2-0
- initial build for Mac OS X WorkShop

