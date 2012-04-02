Name:               ganglia
Version:            3.3.1
Release:            0%{?_dist_release}
Summary:            Ganglia Distributed Monitoring System

Group:              Applications/Internet
License:            BSD
URL:                http://ganglia.sourceforge.net/
Source0:            http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
#Source0:            http://www.ganglia.info/snapshots/3.1.x/%{name}-%{version}.%{svnrev}.tar.gz
Source10:           osxws.ganglia.gmond.plist
Source20:           osxws.ganglia.gmetad.plist
Patch0:             diskusage-pcre.patch
Patch2:             diskmetrics.patch
Patch10:            patch-libmetrics-darwin-metrics.c.diff
Patch20:            ganglia-3.3.1-osxws-prefix.patch
Buildroot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      rrdtool-devel
#BuildRequires:      apr-devel >= 1
BuildRequires:      libpng-devel, libart_lgpl-devel
BuildRequires:      libconfuse-devel
#BuildRequires:      expat-devel
BuildRequires:      python-devel, freetype-devel
BuildRequires:      pcre-devel

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

%package web
Summary:            Ganglia Web Frontend
Group:              Applications/Internet
Requires:           rrdtool
#Requires:           php, php-gd
Requires:           %{name}-gmetad = %{version}-%{release}

%description web
This package provides a web frontend to display the XML tree published by
ganglia, and to provide historical graphs of collected metrics. This website is
written in the PHP4 language.

%package gmetad
Summary:            Ganglia Metadata collection daemon
Group:              Applications/Internet
Requires:           %{name} = %{version}-%{release}

%description gmetad
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmetad daemon aggregates monitoring data from several clusters
to form a monitoring grid. It also keeps metric history using rrdtool.

To launch gmetad:

 $ launchctl load /Library/LaunchDaemons/osxws.ganglia.gmetad.plist

%package gmond
Summary:            Ganglia Monitoring daemon
Group:              Applications/Internet
Requires:           %{name} = %{version}-%{release}

%description gmond
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond daemon provides the ganglia service within a single cluster or
Multicast domain.

To launch gmond:

 $ launchctl load /Library/LaunchDaemons/osxws.ganglia.gmond.plist


%package gmond-python
Summary:            Ganglia Monitor daemon python DSO and metric modules
Group:              Applications/Internet
Requires:           ganglia-gmond, python

%description gmond-python
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This package provides the gmond python DSO and python gmond modules, which
can be loaded via the DSO at gmond daemon start time.

%package devel
Summary:            Ganglia Library
Group:              Applications/Internet
Requires:           %{name} = %{version}-%{release}

%description devel
The Ganglia Monitoring Core library provides a set of functions that
programmers can use to build scalable cluster or grid applications

%prep
%setup -q -n %{name}-%{version}%{?svnrev:.%{svnrev}}
%patch0 -p1
%patch2 -p1
%patch10 -p0
%patch20 -p1
## Hey, those shouldn't be executable...
chmod -x lib/*.{h,x}

%build
#export CC=clang
#export CXX=clang++
export CPPFLAGS="-I%{_includedir}"
export LDFLAGS="-L%{_libdir}"
%configure \
    --with-gmetad \
    --with-gexec \
    --disable-debug \
    --disable-static \
    --enable-shared \
    --sysconfdir=%{_sysconfdir}/ganglia \
    --with-libpcre=%{_libdir} \
    --with-librrd=%{_libdir}

make %{?_smp_mflags}
make -C web

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT 

## Put web files in place
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/ganglia/dwoo/compiled
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/ganglia/dwoo/cache
cp -rf web/conf $RPM_BUILD_ROOT%{_localstatedir}/ganglia
mkdir -p $RPM_BUILD_ROOT/Library/WebServer/Documents/%{name}
(cd web && tar --exclude ".git*" --exclude "*.gz" \
               --exclude "*.in" --exclude "Makefile" \
               --exclude "AUTHORS" --exclude "COPYING" \
               --exclude "README" --exclude "TODO" \
               --exclude "debian" --exclude "ganglia-web" \
               --exclude "gweb.spec" --exclude "rpmbuild" -cpf - .) | \
(cd $RPM_BUILD_ROOT/Library/WebServer/Documents/%{name} && tar xpf -)
ln -s /Library/WebServer/Documents/%{name}/conf_default.php $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf_default.php

## Create directory structures
mkdir -p $RPM_BUILD_ROOT/Library/LaunchDaemons
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/%{name}/rrds
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5
## Put files in place
cp -p %{SOURCE10} $RPM_BUILD_ROOT/Library/LaunchDaemons
cp -p %{SOURCE20} $RPM_BUILD_ROOT/Library/LaunchDaemons
cp -p gmond/gmond.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/gmond.conf.5
cp -p gmetad/gmetad.conf $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/gmetad.conf
cp -p mans/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
## Build default gmond.conf from gmond using the '-t' flag
gmond/gmond -t > $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/gmond.conf

## Python bits
# Copy the python metric modules and .conf files
cp -p gmond/python_modules/conf.d/*.pyconf $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/
cp -p gmond/modules/conf.d/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/
cp -p gmond/python_modules/*/*.py $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/
# Don't install the example modules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/example.conf
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/example.pyconf
# Don't install the status modules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/modgstatus.conf
# Clean up the .conf.in files
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/*.conf.in
## Disable the diskusage module until it is configured properly
#mv $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/diskusage.pyconf $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/diskusage.pyconf.off
# Don't install Makefile* in the web dir
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/Makefile*

# Remove multicpu.conf. modmulticpu.so is broken, this work only on Linux
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/multicpu.conf

## Install binaries
make install DESTDIR=$RPM_BUILD_ROOT
## House cleaning
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/{Makefile.am,version.php.in}

%clean
rm -rf $RPM_BUILD_ROOT

%preun gmetad
if [ "$1" = 0 ]
then
  launchctl stop osxws.ganglia.gmetad
  launchctl unload /Library/LaunchDaemons/osxws.ganglia.gmetad.plist
fi

%preun gmond
if [ "$1" = 0 ]
then
  launchctl stop osxws.ganglia.gmond
  launchctl unload /Library/LaunchDaemons/osxws.ganglia.gmond.plist
fi

%files
%defattr(-,root,wheel,-)
%doc AUTHORS BUGS COPYING INSTALL NEWS
%doc README.AIX README.GIT README.WIN
%{_libdir}/libganglia*.*.dylib
%dir %{_libdir}/ganglia
%{_libdir}/ganglia/*.so
%exclude %{_libdir}/ganglia/modpython.so
%{_bindir}/ganglia-config

%files gmetad
%defattr(-,root,wheel,-)
%dir %{_localstatedir}/%{name}
%attr(0755,nobody,nobody) %{_localstatedir}/%{name}/rrds
%{_sbindir}/gmetad
%{_mandir}/man1/gmetad.1*
/Library/LaunchDaemons/osxws.ganglia.gmetad.plist
%dir %{_sysconfdir}/ganglia
%config(noreplace) %{_sysconfdir}/ganglia/gmetad.conf

%files gmond
%defattr(-,root,wheel,-)
%{_bindir}/gmetric
%{_bindir}/gstat
%{_sbindir}/gmond
/Library/LaunchDaemons/osxws.ganglia.gmond.plist
%{_mandir}/man5/gmond.conf.5*
%{_mandir}/man1/gmond.1*
%{_mandir}/man1/gstat.1*
%{_mandir}/man1/gmetric.1*
%dir %{_sysconfdir}/ganglia
%dir %{_sysconfdir}/ganglia/conf.d
%config(noreplace) %{_sysconfdir}/ganglia/gmond.conf
%exclude %{_sysconfdir}/ganglia/conf.d/modpython.conf

%files gmond-python
%defattr(-,root,wheel,-)
%dir %{_libdir}/ganglia/python_modules/
%{_mandir}/man1/gmetad.py.1*
%{_libdir}/ganglia/python_modules/*.py*
%{_libdir}/ganglia/modpython.so*
%config(noreplace) %{_sysconfdir}/ganglia/conf.d/*.pyconf*
%config(noreplace) %{_sysconfdir}/ganglia/conf.d/modpython.conf

%files devel
%defattr(-,root,wheel,-)
%{_includedir}/*.h
%{_libdir}/libganglia*.dylib

%files web
%defattr(-,root,wheel,-)
%doc web/AUTHORS web/COPYING web/README web/TODO
%{_localstatedir}/%{name}/conf/*.json
%{_localstatedir}/%{name}/conf/sql/ganglia.mysql
%attr(755,www,www) %{_localstatedir}/ganglia/dwoo/compiled
%attr(755,www,www) %{_localstatedir}/ganglia/dwoo/cache
/Library/WebServer/Documents/%{name}
%config(noreplace) /Library/WebServer/Documents/%{name}/conf_default.php
%{_sysconfdir}/ganglia/conf_default.php

%changelog
* Wed Apr 04 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.3.1-0
- update to 3.3.1
- change config file for ganglia-web
- disable g{meta,mon}d auto launch

* Fri Mar 16 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.1.7-6
- initial build for Mac OS X WorkShop

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 3.1.7-6
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Kostas Georgiou <georgiou@fedoraproject.org> - 3.1.7-4
- Fix buffer overflow in moddisk.so #689483

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.1.7-2
- Rebuild for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Apr 22 2010 Kostas Georgiou <georgiou@fedoraproject.org> - 3.1.7-1
- New upstream release
- Spec file cleanups
- Use the new name_match feature to enable the diskusage plugin by default

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 29 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.2-3
- Rebuilt for #492703, no obvious reasons why the previous build was bad :(

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.2-1
- Update to 3.1.2
- Remove unneeded patch for CVE-2009-0241

* Tue Jan 20 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.1-4
- [480236] Updated patch for the buffer overflow from upstream with
  additional fixes

* Wed Jan 14 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.1-3
- Fix for gmetad server buffer overflow
- The private_clusters file should not be readable by everyone

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.1.1-2
- Rebuild for Python 2.6

* Fri Oct 24 2008 Jarod Wilson <jarod@redhat.com> 3.1.1-1
- Update to 3.1.1

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> 3.1.0-2
- Include unowned directories.

* Mon Aug 11 2008 Kostas Georgiou <k.georgiou@imperial.ac.uk> 3.1.0-1
- Upstream patches from 3.1.1
- Move private_clusters config to /etc and mark it as a config file
- Only allow connections from localhost by default on the web frontend
- Add some extra module config files (modules are always loaded at the
  moment so removing the configs has no effect beyond metric collection
  (upstream is working on way way to disable module loading from the
  configs)

* Tue Jul 29 2008 Kostas Georgiou <k.georgiou@imperial.ac.uk> 3.1.0-0.5
- Add the config files for the python module

* Thu Jul 17 2008 Kostas Georgiou <k.georgiou@imperial.ac.uk> 3.1.0-0.4
- Update to the 3.1.0 pre-release
- Fixes gmond.conf to use the ganglia user and not nobody
- Removal of the ppc64 work-around
 
* Fri Jun 13 2008 Jarod Wilson <jwilson@redhat.com> 3.1.0-0.3.r1399
- One more try at work-around. Needs powerpc64, not ppc64...

* Fri Jun 13 2008 Jarod Wilson <jwilson@redhat.com> 3.1.0-0.2.r1399
- Work-around for incorrectly hard-coded libdir on ppc64

* Wed Jun 11 2008 Jarod Wilson <jwilson@redhat.com> 3.1.0-0.1.r1399
- Update to 3.1.x pre-release snapshot, svn rev 1399

* Mon Jun 09 2008 Jarod Wilson <jwilson@redhat.com> 3.0.7-2
- Bump and rebuild against latest rrdtool

* Wed Feb 27 2008 Jarod Wilson <jwilson@redhat.com> 3.0.7-1
- New upstream release
- Fixes "Show Hosts" toggle
- Fixes to host view metric graphs
- Fixes two memory leaks

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> 3.0.6-2
- Bump and rebuild with gcc 4.3

* Mon Dec 17 2007 Jarod Wilson <jwilson@redhat.com> 3.0.6-1
- New upstream release (security fix for web frontend
  cross-scripting vulnerability) {CVE-2007-6465}

* Wed Oct 24 2007 Jarod Wilson <jwilson@redhat.com> 3.0.5-2
- Reorg packages to fix multilib conflicts (#341201)

* Wed Oct 03 2007 Jarod Wilson <jwilson@redhat.com> 3.0.5-1
- New upstream release

* Fri May 18 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-3
- Add missing Req: php-gd so people will see nifty pie charts

* Sat Mar 24 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-2
- Own created directories (#233790)

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-1
- New upstream release

* Thu Nov 09 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-11
- gmond also needs ganglia user (#214762)

* Tue Sep 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-10
- Rebuild for new glibc

* Fri Jul 28 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-9
- Add missing Reqs on chkconfig and service
- Make %%preun sections match Fedora Extras standards
- Minor %%configure tweak

* Tue Jul 11 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-8
- Add missing php req for ganglia-web
- Misc tiny spec cleanups

* Tue Jun 13 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-7
- Clean up documentation

* Mon Jun 12 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-6
- Remove misplaced execute perms on source files

* Thu Jun 08 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-5
- Whack Obsoletes/Provides, since its never been in FE before
- Use mandir macro
- Check if service is running before issuing a stop in postun
- Remove shadow-utils Prereq, its on the FE exception list

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-4
- Run things as user ganglia instead of nobody
- Don't turn on daemons by default

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-3
- Kill off static libs
- Add URL for Source0

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-2
- Move web-frontend from /var/www/html/ to /usr/share/
- Make everything arch-specific

* Thu Jun 01 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-1
- Initial build for Fedora Extras, converting existing spec to
  (attempt to) conform with Fedora packaging guidelines
