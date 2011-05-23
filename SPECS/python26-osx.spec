%define frameworkdir /Library/Frameworks
%define python_version 2.6

Summary: An interpreted, interactive, object-oriented programming language
Name: python
Version: 2.6.6
Release: 1%{?_dist_release}
Source0: http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
Source1: http://docs.python.org/ftp/python/doc/%{version}/python-%{version}-docs-pdf-a4.tar.bz2
Source2: http://docs.python.org/ftp/python/doc/%{version}/python-%{version}-docs-html.tar.bz2
Patch0: python-Lib-ctypes-macholib-dyld-fallback-osxws.patch
Patch1: python-Lib-cgi-osxws.patch
License: PSF
Group: Development/Languages
URL: http://www.python.org/

Requires(post): alternatives
Requires(postun): alternatives
Requires: alternatives
BuildRequires: ncurses-devel readline-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
Python is an interpreted, interactive, object-oriented programming language 
often compared to Tcl, Perl, Scheme or Java. 
Python includes modules, classes, exceptions, very high level dynamic data types and dynamic typing. 
Python supports interfaces to many system calls and libraries,
as well as to various windowing systems (X11, Motif, Tk, Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need a programmable interface.

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: /usr/osxws/bin/python2.6

%description devel
The Python programming language's interpreter can be extended with dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.
The python package will also need to be installed.

%prep
%setup -q -a 1 -a 2 -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
# OSXWS
sed -i.tmp "s|/usr/local|%{_prefix}|g" setup.py
rm -f setup.py.tmp
for f in Demo/cgi/cgi?.py ; do
    sed -i.tmp "s|/usr/local/bin/python|%{_bindir}/python|g" Demo/cgi/cgi?.py
    rm -f $f.tmp
done
sed -i.tmp "s|/usr/local/bin/python|%{_bindir}/python|g" Mac/PythonLauncher/factorySettings.plist
rm -f Mac/PythonLauncher/factorySettings.plist.tmp
for f in Mac/Makefile.in Mac/IDLE/Makefile.in Mac/Tools/Doc/setup.py Mac/PythonLauncher/Makefile.in; do
    sed -i.tmp "s|/Applications|%{_appdirmac}|g" $f
    rm -f $f.tmp
done
# to evade locale.getpreferredencoding() problem
sed -i.tmp "s|'darwin', ||g" Lib/locale.py
sed -i.tmp "s|defined(__APPLE__)|0|g" Modules/_localemodule.c
rm -f Lib/locale.py.tmp Modules/_localemodule.c.tmp
# documents
mv python-%{version}-docs-html html
mv docs-pdf pdf

%build
./configure --prefix=/usr/osxws --enable-framework=/Library/Frameworks \
            --enable-universalsdk --with-universal-archs="intel" --enable-ipv6
make

%install
rm -rf $RPM_BUILD_ROOT
# install framework
make frameworkinstall DESTDIR=$RPM_BUILD_ROOT
make maninstall DESTDIR=$RPM_BUILD_ROOT

# remove non-versioned binary and script
rm $RPM_BUILD_ROOT%{_bindir}/{idle,pydoc,python,pythonw,python-config,smtpd.py}

# make symbloc link from framework to /usr/osxws with relative path
cur_path=%{frameworkdir}/Python.framework/Versions/Current
ln -s $cur_path/bin/python%{python_version}-all $RPM_BUILD_ROOT%{_bindir}/python%{python_version}-all
ln -s $cur_path/bin/pythonw%{python_version}-all $RPM_BUILD_ROOT%{_bindir}/pythonw%{python_version}-all
mkdir -p $RPM_BUILD_ROOT%{_libdir}
ln -s $cur_path/Python $RPM_BUILD_ROOT%{_libdir}/libpython%{python_version}.dylib
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
ln -s $cur_path/man/man1/python%{python_version}.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post
# this package (default)
%{_sbindir}/update-alternatives \
  --install %{_bindir}/python python %{_bindir}/python%{python_version} 30 \
  --slave   %{_bindir}/pythonw pythonw %{_bindir}/pythonw%{python_version} \
  --slave   %{_bindir}/python-config python-config \
              %{_bindir}/python%{python_version}-config \
  --slave   %{_bindir}/pydoc pydoc %{_bindir}/pydoc%{python_version} \
  --slave   %{_bindir}/idle idle %{_bindir}/idle%{python_version} \
  --slave   %{_bindir}/smtp.py smtp.py %{_bindir}/smtpd%{python_version}.py
# Apple python 2.6
%{_sbindir}/update-alternatives \
  --install %{_bindir}/python python /usr/bin/python2.6 20 \
  --slave   %{_bindir}/pythonw pythonw /usr/bin/pythonw2.6 \
  --slave   %{_bindir}/python-config python-config /usr/bin/python2.6-config \
  --slave   %{_bindir}/pydoc pydoc /usr/bin/pydoc2.6 \
  --slave   %{_bindir}/idle idle /usr/bin/idle2.6 \
  --slave   %{_bindir}/smtp.py smtp.py /usr/bin/smtpd2.6.py
# Apple python 2.5
%{_sbindir}/update-alternatives \
  --install %{_bindir}/python python /usr/bin/python2.5 10 \
  --slave   %{_bindir}/pythonw pythonw /usr/bin/pythonw2.5 \
  --slave   %{_bindir}/python-config python-config /usr/bin/python2.5-config \
  --slave   %{_bindir}/pydoc pydoc /usr/bin/pydoc2.5 \
  --slave   %{_bindir}/idle idle /usr/bin/idle2.5 \
  --slave   %{_bindir}/smtp.py smtp.py /usr/bin/smtpd2.5.py
# fix broken symlink if it's there
if [ ! -f %{_bindir}/python ] ; then
  echo "%{_sbindir}/update-alternatives --auto python"
  %{_sbindir}/update-alternatives --auto python
fi

%postun
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove python \
              %{_bindir}/python-%{python_version}
  %{_sbindir}/update-alternatives --auto python
fi
%triggerpostun -- python < %{version}-%{release}
%{_sbindir}/update-alternatives --auto python

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{_mandir}/man1/*.1*
%{frameworkdir}/Python.framework/Python
%{frameworkdir}/Python.framework/Resources
%{frameworkdir}/Python.framework/Versions/Current
%{frameworkdir}/Python.framework/Versions/%{python_version}/bin
%{frameworkdir}/Python.framework/Versions/%{python_version}/lib
%{frameworkdir}/Python.framework/Versions/%{python_version}/Mac
%{frameworkdir}/Python.framework/Versions/%{python_version}/Python
%{frameworkdir}/Python.framework/Versions/%{python_version}/Resources
%{frameworkdir}/Python.framework/Versions/%{python_version}/share
%{_appdirmac}/*
%doc README LICENSE
%doc Demo Doc
%doc html pdf

%files devel
%defattr(-,root,wheel)
%{_libdir}/libpython%{python_version}.dylib
%{frameworkdir}/Python.framework/Headers
%{frameworkdir}/Python.framework/Versions/%{python_version}/Headers
%{frameworkdir}/Python.framework/Versions/%{python_version}/include

%changelog
* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.6-1
- fix type in Group

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.6-0
- initial build for Mac OS X WorkShop

