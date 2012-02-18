%define tcl 0
%define guile 0

Summary: Connects C/C++/Objective C to some high-level programming languages
Summary(ja): Connects C/C++/Objective C to some high-level programming languages
Name: swig
Version: 2.0.4
Release: 1%{?_dist_release}
License: GPLv3+ and BSD
Group: Development/Tools
URL: http://swig.sourceforge.net/
Source: http://downloads.sourceforge.net/project/swig/swig/swig-%{version}/swig-%{version}.tar.gz
Patch1: swig-1.3.23-pylib.patch
Patch4: swig203-rh706140.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl, python-devel, pcre-devel
%if %{tcl}
BuildRequires: tcl-devel
%endif
%if %{guile}
BuildRequires: guile-devel
%endif
BuildRequires: autoconf, automake, gawk, nkf
Obsoletes: swig-runtime

%description
Simplified Wrapper and Interface Generator (SWIG) is a software
development tool for connecting C, C++ and Objective C programs with a
variety of high-level programming languages.  SWIG is primarily used
with Perl, Python and Tcl/TK, but it has also been extended to Java,
Eiffel and Guile.  SWIG is normally used to create high-level
interpreted programming environments, systems integration, and as a
tool for building user interfaces

%package doc
Summary: Documentation files for SWIG
Summary(ja): Documentation files for SWIG
License: BSD
Group: Development/Tools
BuildArch: noarch

%description doc
This package contains documentation for SWIG and useful examples

%prep
%setup -q -n swig-%{version}
%patch1 -p1 -b .pylib
%patch4 -p1 -b .rh706140

# as written on https://fedoraproject.org/wiki/Packaging_talk:Perl, section 2
# (specific req/prov filtering). Before you remove this hack make sure you don't
# reintroduce https://bugzilla.redhat.com/show_bug.cgi?id=489421
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} `perl -p -e 's|\S+%{_docdir}/%{name}-doc-%{version}\S+||'`
EOF

%define __perl_provides %{_builddir}/%{name}-%{version}/%{name}-prov
chmod +x %{__perl_provides}

cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} `perl -p -e 's|\S+%{_docdir}/%{name}-doc-%{version}\S+||'`
EOF

%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

for all in CHANGES README; do
	iconv -f ISO88591 -t UTF8 < $all > $all.new
	touch -r $all $all.new
	mv -f $all.new $all
done

%build
./autogen.sh
%configure
make %{?_smp_mflags}

# Test suite is currently broken
#make check

%install
rm -rf %{buildroot}

pushd Examples/
# Remove all arch dependent files in Examples/
find -type f -name 'Makefile.in' | xargs rm -f --

# We don't want to ship files below.
rm -rf test-suite
find -type f -name '*.dsp' | xargs rm -f --
find -type f -name '*.dsw' | xargs rm -f --

# Convert files to UNIX format
for all in `find -type f`; do
	nkf --unix $all
	chmod -x $all
done
popd

make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/swig
%{_mandir}/man1/ccache-swig.1*
%doc ANNOUNCE CHANGES CHANGES.current INSTALL LICENSE LICENSE-GPL
%doc LICENSE-UNIVERSITIES COPYRIGHT README TODO

%files doc
%defattr(-,root,root,-)
%doc Doc Examples LICENSE LICENSE-GPL LICENSE-UNIVERSITIES COPYRIGHT

%changelog
* Sat Oct 29 2011 Daisuke SUZUKI <daisuke@linux.or.jp> 2.0.4-1
- update to 2.0.4

* Tue Mar 02 2010 MATSUBAYASHI Kohji <shaolin@vinelinux.org> - 1.3.40-2
- add missing man file(s) to the filelist

* Mon Mar 01 2010 Shu KONNO <owa@bg.wakwak.com> 1.3.40-1
- new upstream release
- rebuild with new toolchain

* Fri Sep 05 2008 Daisuke SUZUKI <daisuke@linux.or.jp> 1.3.35-1
- new upstream release

* Wed Mar 28 2007 NAKAMURA Kenta <kenta@vinelinux.org> 1.3.31-0vl1
- new upstream release
- removed php-devel and ruby-devel from BuildPreReq:.

* Sun May 28 2006 Daisuke SUZUKI <daisuke@linux.or.jp> 1.3.29-0vl1
- new upstream release
- use %%configure
- remove runtime subpackage

* Sun Jan 23 2005 Tomohiro 'Tomo-p' KATO <tomop@teamgedoh.net>
- 1.3.21-0vl2
- un-libtoolize (tarball have already been libtoolized).
- fix %%clean.
- add guile-devel, php-devel, python-devel and ruby-devel to BuildPreReq:.

* Wed Mar 03 2004 Seiya Nishizawa <seiya@kugi.kyoto-u.ac.jp>
- 1.3.21-0vl1
- update version

* Sat Dec 27 2003 Seiya Nishizawa <seiya@kugi.kyoto-u.ac.jp>
- 1.3.20-0vl1
- update version

* Mon Jun 03 2003 Seiya Nishizawa <seiya@kugi.kyoto-u.ac.jp>
- update version

* Mon Mar 03 2002 Seiya Nishizawa <seiya@kugi.kyoto-u.ac.jp>
- update version

* Mon Mar 26 2001 Kazuhisa TAKEI <takei@vinelinux.org>
- import to Vine Linux

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3a3-1mdk
- BM.
- Clean up specs.
- 1.3a3.

* Tue Jun 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1p5-5mdk
- Use makeinstall macros.

* Mon Apr 10 2000 Francis Galiegue <fg@mandrakesoft.com> 1.1p5-4mdk

- Provides: swig

* Mon Apr  3 2000 Pixel <pixel@mandrakesoft.com> 1.1p5-3mdk
- rebuild with new perl
- cleanup

* Wed Mar 22 2000 Francis Galiegue <fg@mandrakesoft.com> 1.1p5-2mdk

- Rebuilt on kenobi
- Don't use prefix

* Fri Mar 10 2000 Francis Galiegue <francis@mandrakesoft.com> 1.1p5-1mdk

- First RPM for Mandrake

