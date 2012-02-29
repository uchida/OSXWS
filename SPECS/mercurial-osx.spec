%define shared_dir /Users/Shared

Summary: A fast, lightweight distributed source control management system 
Summary(ja): 軽量で高速な分散構成管理システム
Name: mercurial
Version: 2.1
Release: 0%{?_dist_release}
License: GPLv2
Group: Development/Tools
URL: http://mercurial.selenic.com/
Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
Source1: mercurial-init.el
Source10: mercurial-el-install.sh
Source11: mercurial-el-remove.sh
Source20: hgweb.conf
Patch1: mercurial-hgk-fontsize.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-docutils
BuildRequires: emacsen-common pkgconfig
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
Provides: hg = %{version}-%{release}

%description
Mercurial is a fast, lightweight source control management system designed
for efficient handling of very large distributed projects.

Quick start: http://www.selenic.com/mercurial/wiki/index.cgi/QuickStart
Tutorial: http://www.selenic.com/mercurial/wiki/index.cgi/Tutorial
Extensions: http://www.selenic.com/mercurial/wiki/index.cgi/CategoryExtension


%package el
Summary:	Mercurial version control system support for Emacs
Summary(ja):	Mercurial バージョン管理システム用 Emacs サポート
Group:		Applications/Editors
Requires:	hg = %{version}-%{release}, emacsen-common
Requires:       emacsen


%description el
Contains byte compiled elisp packages for mercurial.
To get started: start emacs, load hg-mode with M-x hg-mode, and show 
help with C-c h h


%package hgk
Summary:	Hgk interface for mercurial
Summary(ja):	Mercurial 用 Hgk インタフェース
Group:		Development/Tools
Requires:	hg = %{version}-%{release}, tk


%description hgk
A Mercurial extension for displaying the change history graphically
using Tcl/Tk.  Displays branches and merges in an easily
understandable way and shows diffs for each revision.  Based on
gitk for the git SCM.

Adds the "hg view" command.  See 
http://www.selenic.com/mercurial/wiki/index.cgi/UsingHgk for more
documentation.

%package hgweb
Summary: Simple web interface to mercurial repositories
Summary(ja): mercurial リポジトリへのシンプルな Web インタフェース
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

%description hgweb
Simple web interface to track changes in mercurial repositories.

In Mac OS X WorkShop default, the repositories in %{shared_dir}/mercurial are opened to the public
when you enable "Web Sharing" in "System Preferences".
To see the repositories, access "http://<IP-Address>/cgi-bin/hgweb.cgi".

%description -l ja hgweb
mercurial レポジトリの変更を追うためのシンプルな Web インタフェース。

Mac OS X WorkShop のデフォルトでは、「システム環境設定」で 「Web 共有」を入にすると、
%{shared_dir}/mercurial に置かれたレポジトリが公開されます。
公開されたレポジトリは http://<IP-Address>/cgi-bin/hgweb.cgi から見ることができます。

%prep
%setup -q
%patch1 -p1
sed -i.osxws 's|/usr/local/bin/hg|%{_bindir}/hg|g' contrib/mercurial.el
sed -i.osxws 's|/home/user/hg/hg/contrib/hgk|%{_libexecdir}/mercurial/hgk|g' contrib/sample.hgrc
sed -i.osxws 's|/path/to/repo/or/config|%{_sysconfdir}/hgweb.conf|g' hgweb.cgi

%build
export CFLAGS="-I%{_includedir}"
export LDFLAGS="-L%{_libdir}"
make all

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-script=%{_bindir}  --record=%{name}.files
make install-doc DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

# install contrib
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/mercurial
grep -v 'hgk.py*' < %{name}.files > %{name}-base.files
grep 'hgk.py*' < %{name}.files > %{name}-hgk.files

install -m 755 contrib/hgk $RPM_BUILD_ROOT%{_libexecdir}/mercurial/hgk
install -m 755 contrib/hg-ssh $RPM_BUILD_ROOT%{_bindir}
install -m 755 contrib/convert-repo $RPM_BUILD_ROOT%{_bindir}/mercurial-convert-repo

bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 contrib/bash_completion $bash_completion_dir/mercurial.sh

zsh_completion_dir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
mkdir -p $zsh_completion_dir
install -m 644 contrib/zsh_completion $zsh_completion_dir/_mercurial

mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/mercurial

pushd contrib
for file in mercurial.el mq.el %{SOURCE1}; do
  install -p -m 644 $file $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}/
done
popd

%__mkdir_p %{buildroot}%{_prefix}/lib/emacsen-common/packages/install
%__mkdir_p %{buildroot}%{_prefix}/lib/emacsen-common/packages/remove

%_installemacsenscript %{name} %{SOURCE10}

%_removeemacsenscript  %{name} %{SOURCE11}


mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

cat >hgk.rc <<EOF
[extensions]
# enable hgk extension ('hg help' shows 'view' as a command)
hgk=

[hgk]
path=%{_libexecdir}/mercurial/hgk
EOF
install hgk.rc $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

install contrib/mergetools.hgrc $RPM_BUILD_ROOT%{_sysconfdir}/mercurial/hgrc.d/mergetools.rc.sample

mkdir -p $RPM_BUILD_ROOT%{shared_dir}/mercurial
install -m 644 %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/Library/WebServer/CGI-Executables
install -m 755 hgweb.cgi $RPM_BUILD_ROOT/Library/WebServer/CGI-Executables


%clean
rm -rf $RPM_BUILD_ROOT


%post el
if [ $1 = 2 ] ; then
        %_emacsenPackageRemove %{name}

fi
%_addemacsenlist %{name}

%_emacsenPackageInstall %{name}


%preun el
if [ $1 = 0 ] ; then
        %_emacsenPackageRemove %{name}

        %_removeemacsenlist %{name}

fi


%files -f %{name}-base.files
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING doc/README doc/hg*.txt doc/hg*.html *.cgi contrib/*.fcgi
%doc %attr(644,root,root) %{_mandir}/man?/hg*.gz
%doc %attr(644,root,root) contrib/*.svg contrib/sample.hgrc
%{_sysconfdir}/bash_completion.d/mercurial.sh
%{_datadir}/zsh/site-functions/_mercurial
%{_bindir}/hg-ssh
%{_bindir}/mercurial-convert-repo
%dir %{_sysconfdir}/mercurial
%dir %{_sysconfdir}/mercurial/hgrc.d
%{_sysconfdir}/mercurial/hgrc.d/mergetools.rc.sample
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%dir %{python_sitearch}/mercurial
%dir %{python_sitearch}/hgext


%files el
%{_datadir}/emacs/site-lisp/mercurial
%{_prefix}/lib/emacsen-common/packages/*/mercurial


%files hgk -f %{name}-hgk.files
%{_libexecdir}/mercurial/
%{_sysconfdir}/mercurial/hgrc.d/hgk.rc

%files hgweb
%defattr(-,root,wheel)
/Library/WebServer/CGI-Executables/hgweb.cgi
%config(noreplace) %{_sysconfdir}/hgweb.conf
%defattr(777,root,wheel)
%dir %{shared_dir}/mercurial

%changelog
* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.1-0
- update to 2.1

* Sat Feb 18 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.8.3-3
- build x86_64 mono arch

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.8.3-2
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.8.3-1
- make more compatible with Vine Linux

* Thu May 19 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.8.3-0
- update to 1.8.3

* Wed Feb 16 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.5-0
- update to 1.7.5

* Sat Feb 12 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.3-3
- make default font size bigger in hgk

* Tue Feb  8 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.3-2
- add hgweb sub-package and merge hgk package to mercurial

* Tue Jan 25 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.3-1
- import sub-package from Vine Linux mercurial rpm

* Sat Jan  8 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.3-0
- update to 1.7.3

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.6.4-0
- initial build for Mac OS X WorkShop

