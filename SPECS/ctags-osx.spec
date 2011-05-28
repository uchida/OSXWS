Summary: Exuberant Ctags - a multi-language source code indexing tool
Name: ctags
Version: 5.8
Release: 0%{?_dist_release}
License: GPLv2
Group: Development/Tools
Source: http://prdownloads.sourceforge.net/ctags/ctags-%{version}.tar.gz
# http://hp.vector.co.jp/authors/VA025040/ctags/
Patch0: ctags-japanese.patch
URL: http://ctags.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
Exuberant Ctags generates an index (or tag) file of language objects
found in source files for many popular programming languages. This index
makes it easy for text editors and other tools to locate the indexed
items. Exuberant Ctags improves on traditional ctags because of its
multilanguage support, its ability for the user to define new languages
searched by regular expressions, and its ability to generate emacs-style
TAGS files.

Ues update-alternatives so as not to conflict with the Mac OS X system default ctags.
You may have to run 
    sudo update-alternatives --config ctags
to make sure you are using this package.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
export CFLAGS='-arch i386 -arch x86_64'
export LDFLAGS='-arch i386 -arch x86_64'
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
* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 5.8-0
- initial build for Mac OS X WorkShop

