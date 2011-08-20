Name:           cvsps
Version:        2.1
Release:        0%{?_dist_release}
Summary:        Patchset tool for CVS

Group:          Development/Tools
License:        GPL+
URL:            http://www.cobite.com/cvsps/
Source0:        http://www.cobite.com/cvsps/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: fat

BuildRequires:  zlib-devel
# Requires cvs only with --no-cvs-direct, but I cannot imagine this dep
# being a problem on systems where cvsps will be installed...
Requires: cvs

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
export CC="/usr/bin/gcc-4.2 -arch i386 -arch x86_64"
export CPP="/usr/bin/gcc -E"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc CHANGELOG COPYING README merge_utils.sh
%{_bindir}/cvsps
%{_mandir}/man1/cvsps.1*


%changelog
* Sun Jul  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.1-0
- initial build for Mac OS X WorkShop

