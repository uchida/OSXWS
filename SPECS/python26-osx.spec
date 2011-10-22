%define frameworkdir /Library/Frameworks
%define python_version 2.6
%define python_lib %{frameworkdir}/Python.framework/Versions/%{python_version}/lib/python%{python_version}

Summary: An interpreted, interactive, object-oriented programming language.
Summary(ja): オブジェクト指向言語 Python インタプリタ
Name: python
Version: %{python_version}.7
Release: 3%{?_dist_release}
Source0: http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
Source1: http://docs.python.org/ftp/python/doc/%{version}/python-%{version}-docs-pdf-a4.tar.bz2
Source2: http://docs.python.org/ftp/python/doc/%{version}/python-%{version}-docs-html.tar.bz2
Patch0: python-Lib-ctypes-macholib-dyld-fallback-osxws.patch
Patch1: python-Lib-cgi-osxws.patch
Patch2: python-configure-linkforshared.patch
License: PSF
Group: Development/Languages
URL: http://www.python.org/

Requires(post): alternatives
Requires(postun): alternatives
Requires: alternatives
BuildRequires: ncurses-devel readline-devel
Provides: tkinter
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
Python is an interpreted, interactive, object-oriented programming
language.  It incorporates modules, exceptions, dynamic typing, very high
level dynamic data types, and classes. Python combines remarkable power
with very clear syntax. It has interfaces to many system calls and
libraries, as well as to various window systems, and is extensible in C or
C++. It is also usable as an extension language for applications that need
a programmable interface.  Finally, Python is portable: it runs on many
brands of UNIX, on PCs under Windows, MS-DOS, and OS/2, and on the
Mac.

%package devel
Summary: The libraries and header files needed for Python development.
Summary(ja): Python での開発に必要なライブラリやヘッダファイル
Group: Development/Libraries
Obsoletes: python2-devel

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python.
Summary(ja): Python に含まれる開発ツール一式
Group: Development/Tools
Requires: %{name} = %{version}
Requires: tkinter = %{version}
Obsoletes: python2-tools

%description tools
The Python package includes several development tools that are used
to build python programs.  This package contains a selection of those
tools, including the IDLE Python IDE.

Install python-tools if you want to use these tools to develop
Python programs.  You will also need to install the python and
tkinter packages.

%package docs
Summary: Documentation for the Python programming language.
Summary(ja): Python プログラミング言語のドキュメント
Group: Applications/Documentation
Obsoletes: python2-docs
BuildArch: noarch

%description docs
Documentation relating to the Python programming language in HTML and info
formats.

%prep
%setup -q -a 1 -a 2 -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
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
export CC="/usr/bin/gcc-4.2"
export CXX="/usr/bin/g++-4.2"
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
cur_path=%{frameworkdir}/Python.framework/Versions/%{python_version}
ln -s $cur_path/bin/python%{python_version}-all $RPM_BUILD_ROOT%{_bindir}/python%{python_version}-all
ln -s $cur_path/bin/pythonw%{python_version}-all $RPM_BUILD_ROOT%{_bindir}/pythonw%{python_version}-all
ln -s $cur_path/bin/2to3 $RPM_BUILD_ROOT%{_bindir}/2to3%{python_version}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
ln -s $cur_path/Python $RPM_BUILD_ROOT%{_libdir}/libpython%{python_version}.dylib
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
ln -s $cur_path/man/man1/python%{python_version}.1 $RPM_BUILD_ROOT%{_mandir}/man1/

## tools
mkdir -p $RPM_BUILD_ROOT%{python_lib}/site-packages
echo "#!/bin/bash
exec $cur_path/lib/site-packages/pynche/pynche" \
	> $RPM_BUILD_ROOT%{_bindir}/pynche
chmod 755 $RPM_BUILD_ROOT%{_bindir}/pynche
echo "#!/bin/bash
exec $cur_path/lib/site-packages/modulator/modulator.py" \
	> $RPM_BUILD_ROOT%{_bindir}/modulator
chmod 755 $RPM_BUILD_ROOT%{_bindir}/modulator
#modulator
cp -r Tools/modulator ${RPM_BUILD_ROOT}%{python_lib}/site-packages/
#pynche
rm -f Tools/pynche/*.pyw
cp -r Tools/pynche $RPM_BUILD_ROOT%{python_lib}/site-packages/
(mv Tools/modulator/README Tools/modulator/README.modulator)
(mv Tools/pynche/README Tools/pynche/README.pynche)
#gettext
install -m755  Tools/i18n/pygettext.py $RPM_BUILD_ROOT%{_bindir}
install -m755  Tools/i18n/msgfmt.py $RPM_BUILD_ROOT%{_bindir}

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
  --slave   %{_bindir}/2to3 2to3 %{_bindir}/2to326 \
  --slave   %{_bindir}/smtpd.py smtpd.py %{_bindir}/smtpd%{python_version}.py
# Apple python 2.6
%{_sbindir}/update-alternatives \
  --install %{_bindir}/python python /usr/bin/python2.6 20 \
  --slave   %{_bindir}/pythonw pythonw /usr/bin/pythonw2.6 \
  --slave   %{_bindir}/python-config python-config /usr/bin/python2.6-config \
  --slave   %{_bindir}/pydoc pydoc /usr/bin/pydoc2.6 \
  --slave   %{_bindir}/idle idle /usr/bin/idle2.6 \
  --slave   %{_bindir}/2to3 2to3 /usr/bin/2to3 \
  --slave   %{_bindir}/smtpd.py smtpd.py /usr/bin/smtpd2.6.py
# Apple python 2.5
%{_sbindir}/update-alternatives \
  --install %{_bindir}/python python /usr/bin/python2.5 10 \
  --slave   %{_bindir}/pythonw pythonw /usr/bin/pythonw2.5 \
  --slave   %{_bindir}/python-config python-config /usr/bin/python2.5-config \
  --slave   %{_bindir}/pydoc pydoc /usr/bin/pydoc2.5 \
  --slave   %{_bindir}/idle idle /usr/bin/idle2.5 \
  --slave   %{_bindir}/smtpd.py smtpd.py /usr/bin/smtpd2.5.py
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
%{_bindir}
%exclude %{_bindir}/modulator
%exclude %{_bindir}/msgfmt.py
%exclude %{_bindir}/pygettext.py
%exclude %{_bindir}/pynche
%{_mandir}/man1/*.1*
%{frameworkdir}/Python.framework/Python
%{frameworkdir}/Python.framework/Resources
%{frameworkdir}/Python.framework/Versions/Current
%{frameworkdir}/Python.framework/Versions/%{python_version}/bin
%{frameworkdir}/Python.framework/Versions/%{python_version}/lib
%exclude %{python_lib}/config
%exclude %{python_lib}/test
%exclude %{python_lib}/site-packages/modulator
%exclude %{python_lib}/site-packages/pynche
%{frameworkdir}/Python.framework/Versions/%{python_version}/Mac
%{frameworkdir}/Python.framework/Versions/%{python_version}/Python
%{frameworkdir}/Python.framework/Versions/%{python_version}/Resources
%{frameworkdir}/Python.framework/Versions/%{python_version}/share
%doc README LICENSE
%doc Demo

%files devel
%defattr(-,root,wheel)
%{_libdir}/libpython%{python_version}.dylib
%{frameworkdir}/Python.framework/Headers
%{frameworkdir}/Python.framework/Versions/%{python_version}/Headers
%{frameworkdir}/Python.framework/Versions/%{python_version}/include
%{python_lib}/config
%{python_lib}/test

%files tools
%defattr(-,root,wheel,755)
%doc Tools/modulator/README.modulator
%doc Tools/pynche/README.pynche
%{python_lib}/site-packages/modulator
%{python_lib}/site-packages/pynche
%{_bindir}/modulator
%{_bindir}/msgfmt.py
%{_bindir}/pygettext.py
%{_bindir}/pynche
%{_appdirmac}/*

%files docs
%defattr(-,root,root,755)
%doc Misc/HISTORY Misc/NEWS  Misc/README Misc/cheatsheet Misc/developers.txt
%doc Doc html pdf

%changelog
* Fri Oct 21 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.7-3
- fix LINKSHARED environment variable

* Thu Aug 25 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.7-2
- make python-docs noarch

* Thu Aug 25 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.7-1
- fix postinstall script
- give paths to CC and CXX

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.7-0
- update to 2.6.7

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.6-2
- add subpackages (tools, docs)

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.6-1
- fix typo in Group

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.6.6-0
- initial build for Mac OS X WorkShop

