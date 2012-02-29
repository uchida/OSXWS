Summary: A C programming language indexing and/or cross-reference tool.
Name: ctags
Version: 5.8
Release: 2%{?_dist_release}
License: GPLv2
Group: Development/Tools
Source: http://prdownloads.sourceforge.net/ctags/ctags-%{version}.tar.gz
# http://hp.vector.co.jp/authors/VA025040/ctags/
Patch0: ctags-japanese.patch
URL: http://ctags.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires(post): alternatives
Requires(postun): alternatives

%description
Ctags generates an index (or tag) file of C language objects found in
C source and header files.  The index makes it easy for text editors or
other utilities to locate the indexed items.  Ctags can also generate a
cross reference file which lists information about the various objects
found in a set of C language files in human readable form.  Exuberant
Ctags improves on ctags because it can find all types of C language tags,
including macro definitions, enumerated values (values inside enum{...}),
function and method definitions, enum/struct/union tags, external
function prototypes, typedef names and variable declarations.  Exuberant
Ctags is far less likely to be fooled by code containing #if preprocessor
conditional constructs than ctags.  Exuberant ctags supports output of
Emacs style TAGS files and can be used to print out a list of selected
objects found in source files.

Install ctags if you are going to use your system for C programming.

To evade the conflict with one of Mac OS X system, use update-alternatives,
so you may have to run 
    sudo update-alternatives --config ctags
to make sure you are using this package.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall prefix=$RPM_BUILD_ROOT%{_prefix}
mv $RPM_BUILD_ROOT%{_bindir}/ctags $RPM_BUILD_ROOT%{_bindir}/ctags-exuberant
mv $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1 $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1-exuberant

%clean
rm -rf $RPM_BUILD_ROOT

%post
# this package (default)
%{_sbindir}/update-alternatives \
  --install %{_bindir}/ctags ctags %{_bindir}/ctags-exuberant 70 \
  --slave   %{_mandir}/man1/ctags.1 ctags.1 %{_mandir}/man1/ctags.1-exuberant
# Mac OS X default
%{_sbindir}/update-alternatives \
  --install %{_bindir}/ctags ctags /usr/bin/ctags 50 \
  --slave   %{_mandir}/man1/ctags.1 ctags.1 /usr/share/man/man1/ctags.1
# fix broken symlink if it's there
if [ ! -f %{_bindir}/ctags ] ; then
  echo "%{_sbindir}/update-alternatives --auto ctags"
  %{_sbindir}/update-alternatives --auto ctags
fi

%postun
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove ctags %{_bindir}/ctags-exuberant
  %{_sbindir}/update-alternatives --auto ctags
fi

%triggerpostun -- ctags < %{version}-%{release}
%{_sbindir}/update-alternatives --auto ctags

%files
%defattr(-,root,wheel)
%doc COPYING EXTENDING.html FAQ NEWS README ctags.html
%doc README_J.TXT ctags_j.html
%{_bindir}/ctags-exuberant
%{_mandir}/man1/ctags*

%changelog
* Sat Feb 18 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.8-2
- build x86_64 mono arch

* Tue Jun 28 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.8-1
- change summary and description for Vine Linux compatibility

* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.8-0
- initial build for Mac OS X WorkShop

