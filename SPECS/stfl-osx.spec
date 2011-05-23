Summary: Structured Terminal Forms Language/Library
Name: stfl
Version: 0.21
Release: 1%{?_dist_release}
Source0: http://www.clifford.at/stfl/stfl-0.21.tar.gz
Patch0: stfl-macosx.patch
Patch1: stfl-iconv.patch
License: LGPL or GPLv3+
Group: System Environment/Libraries
URL: http://www.clifford.at/stfl/

BuildRequires: ncurses-devel
BuildRequires: pkgconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
STFL is a library which implements a curses-based widget set for text terminals.
The STFL API can be used from C, SPL, Python, Perl and Ruby.
Since the API is only 14 simple function calls big and there are already generic SWIG bindings
it is very easy to port STFL to additional scripting languages.

A special language (the Structured Terminal Forms Language) is used to describe STFL GUIs.
The language is designed to be easy and fast to write so an application programmer does not need
to spend ages fiddling around with the GUI and can concentrate on the more interesting programming tasks.

%package devel
Summary: The development libraries and header files for stfl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The stfl-devel package contains the development libraries and header
files for stfl

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
sed -i.arch 's|@LDFLAGS@|"-arch i386 -arch x86_64"|g' perl5/Makefile.snippet
sed -i.arch 's|@LDDLFLAGS@|"-arch i386 -arch x86_64 -bundle -undefined dynamic_lookup"|g' perl5/Makefile.snippet
rm -f perl5/Makefile.snippet.arch
%patch1 -p1
for f in Makefile stfl.pc.in perl5/Makefile.PL python/Makefile.snippet ruby/Makefile.snippet; do
    sed -i.tmp 's|-lncursesw|-lncurses|g' $f
    rm -f $f.tmp
done
for f in stfl_internals.h; do
    sed -i.tmp 's|<ncursesw/ncurses.h>|<ncurses.h>|g' $f
    rm -f $f.tmp
done

%build
export CFLAGS='-arch i386 -arch x86_64'
export LDLIBS='-arch i386 -arch x86_64'
make prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT

make install prefix=%{_prefix} DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT/Library/Perl/Updates

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc COPYING README
%{python_sitelib}/*
%{perl_sitelib}/*
%{rslibdir}/*
%{_libdir}/libstfl.*.dylib

%files devel
%defattr(-,root,wheel)
%{_includedir}/*
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.dylib
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Jan  9 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.21-1
- remove extraneous objects

* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.21-0
- initial build for Mac OS X WorkShop

