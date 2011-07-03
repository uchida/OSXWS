Name:           cvsps
Version:        2.1
Release:        1%{?_dist_release}
Summary:        Patchset tool for CVS

Group:          Development/Tools
License:        GPL+
URL:            http://www.cobite.com/cvsps/
Source0:        http://www.cobite.com/cvsps/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  zlib-devel
# Requires cvs only with --no-cvs-direct, but I cannot imagine this dep
# being a problem on systems where cvsps will be installed...
Requires(hint): cvs

%description
CVSps is a program for generating 'patchset' information from a CVS
repository.  A patchset in this case is defined as a set of changes
made to a collection of files, and all committed at the same time
(using a single 'cvs commit' command).  This information is valuable
to seeing the big picture of the evolution of a cvs project.  While
cvs tracks revision information, it is often difficult to see what
changes were committed 'atomically' to the repository.


%prep
%setup -q
sed -i -e 's/diffs\\-opts/diff\\-opts/' cvsps.1


%build
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGELOG COPYING README merge_utils.sh
%{_bindir}/cvsps
%{_mandir}/man1/cvsps.1*


%changelog
* Sun Aug 24 2008 Daisuke SUZUKI <daisuke@linux.or.jp> 2.1-1
- initial build for Vine Linux

* Sat Jun 14 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.2-0.1.b1
- 2.2b1.

* Sat Feb  9 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.1-6
- Change cvs dependency to a Requires(hint).
- Fix typo in man page.

* Thu Aug 16 2007 Ville Skyttä <ville.skytta at iki.fi> - 2.1-5
- License: GPL+

* Tue Aug 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.1-4
- Rebuild.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.1-3
- Rebuild.

* Fri May 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.1-2
- 2.1.

* Sun Mar 20 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.0-0.2.rc1
- Drop 0.fdr and Epoch: 0.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-0.fdr.0.2.rc1
- Remove #---- section markers.

* Fri Jul  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-0.fdr.0.1.rc1
- First build.
