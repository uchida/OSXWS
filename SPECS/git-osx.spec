%define prereq_ge()  %(LC_ALL="C" rpm -q --queryformat 'PreReq:%%{NAME} >= %%{VERSION}' %1| grep -v "is not")
%define emacsen_pkgdir %{_libdir}/emacsen-common/packages
%define shared_dir /Users/Shared

# Pass --without docs to rpmbuild if you don't want the documentation
Name: 		git
Version: 	1.7.7.1
Release:        0%{?_dist_release}
Summary:  	Core git tools
Summary(ja):	Core git ツール
License: 	GPLv2
Group: 		Development/Tools
URL: 		http://git-scm.com/
Source: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.gz
Source1:	osxws-default-git.el
Source2:    osxws.git.daemon.plist
Source3:    gitweb.conf.in
Source10:       %{name}-install.sh
Source11:       %{name}-remove.sh
Source12:	git-init.el
Source100:  http://kernel.org/pub/software/scm/git/%{name}-htmldocs-%{version}.tar.gz
Source200:  http://kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.gz
Patch0:     git-perl-macosx.patch
Patch1:     git_remote_helpers.patch
Patch10:    git-1.5-gitweb-home-link.patch

####

# Security
# none

BuildRequires:	zlib-devel >= 1.2, openssl-devel

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      fat

Requires:	perl-Git = %{version}-%{release}
Requires:	zlib
Provides:	git-core = %{version}-%{release}
Obsoletes:	git-core <= 1.5.4.3

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

%package all
Summary:	Meta-package to pull in all git tools
Summary(ja):	すべての git ツール
Group:		Development/Tools
Requires:	git = %{version}-%{release}
Requires:	git-svn = %{version}-%{release}
Requires:	git-cvs = %{version}-%{release}
%if "%{?_dist_release}" != "vl4"
Requires:	git-arch = %{version}-%{release}
%endif
Requires:	git-email = %{version}-%{release}
Requires:	gitk = %{version}-%{release}
Requires:	git-gui = %{version}-%{release}
Requires:	perl-Git = %{version}-%{release}
Requires:	emacs-git = %{version}-%{release}
Obsoletes:	git <= 1.5.4.3

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package daemon
Summary:	Git protocol daemon
Summary(ja):	Git プロトコルデーモン
Group:		Development/Tools
Requires:	git = %{version}-%{release}
%description daemon
The git daemon for supporting git:// access to git repositories

In Mac OS X WorkShop default, daemon provide access to the repositories in %{shared_dir}/git
via git://<IP-Address>/<your-repository>.

To publish git repositories, execute the following command in Terminal:
    $ launchctl load -w /Library/LaunchDaemons/osxws.git.daemon.plist
If the Mac OS X firewall is turned on, allow git incomming connections in Advances Setting.

To close repositories, execute the following command in Terminal:
    $ launchctl unload -w /Library/LaunchDaemons/osxws.git.daemon.plist

%description -l ja daemon
git:// 経由での git アクセスを可能にするためのデーモン

Mac OS X WorkShop のデフォルトでは、%{shared_dir}/git におかれた
git レポジトリに git://<IP-Address>/<your-repository> 経由でアクセスできるようになります。

git レポジトリを公開する場合は、ターミナルで以下のコマンドを実行して下さい。
    $ launchctl load -w /Library/LaunchDaemons/osxws.git.daemon.plist
Mac OS X のファイアウォールが有効になっている場合は、詳細設定から git の受信接続を許可してください。

非公開にする場合には以下のコマンドを実行して下さい。
    $ launchctl unload -w /Library/LaunchDaemons/osxws.git.daemon.plist

%package -n gitweb
Summary:        Simple web interface to git repositories
Summary(ja):    git リポジトリへのシンプルな Web インタフェース
Group:          Development/Tools
Requires:       git = %{version}-%{release}

%description -n gitweb
Simple web interface to track changes in git repositories

This package enable to publish git repositories via web.
In Mac OS X WorkShop default, the repositories in %{shared_dir}/git are published
when you enable "Web Sharing" in "System Preferences".
To see the repositories, access http://<IP-Address>/cgi-bin/gitweb.cgi.

%description -l ja -n gitweb
git レポジトリの変更を追うためのシンプルな Web インタフェース。

このパッケージは git レポジトリを Web 経由で公開します。
Mac OS X WorkShop のデフォルトでは、「システム環境設定」で 「Web 共有」を入にすると、
%{shared_dir}/git に置かれたレポジトリが公開されます。
公開されたレポジトリは http://<IP-Address>/cgi-bin/gitweb.cgi から見ることができます。

%package svn
Summary:        Git tools for importing Subversion repositories
Summary(ja):    Subversion リポジトリを git へインポートするためのツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, subversion
%description svn
Git tools for importing Subversion repositories.

%package cvs
Summary:        Git tools for importing CVS repositories
Summary(ja):    CVS リポジトリを git へインポートするためのツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, cvs, cvsps
%description cvs
Git tools for importing CVS repositories.

%package arch
Summary:        Git tools for importing Arch repositories
Summary(ja):    Arch リポジトリを git へインポートするためのツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tla
%description arch
Git tools for importing Arch repositories.

%package email
Summary:        Git tools for sending email
Summary(ja):    Eメールを送るための git ツール
Group:          Development/Tools
Requires:	git = %{version}-%{release}, perl-Git = %{version}-%{release}
%description email
Git tools for sending email.

%package gui
Summary:        Git GUI tool
Summary(ja):    Git の GUI ツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tk
%description gui
Git GUI tool.

%package -n gitk
Summary:        Git revision tree visualiser
Summary(ja):    Git リビジョンツリー可視化ツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tk
%description -n gitk
Git revision tree visualiser.

%package -n perl-Git
Summary:        Perl interface to Git
Summary(ja):    Git の perl インタフェース
Group:          Development/Libraries
Requires:       git = %{version}-%{release}

%description -n perl-Git
Perl interface to Git.

%package -n python-Git
Summary:        Python interface to Git
Summary(ja):    Git の python インタフェース
Group:          Development/Libraries
Requires:       git = %{version}-%{release}
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python > 2.6.1
%else
Requires: python
BuildRequires: python
%endif
%description -n python-Git
%{summary}.

%package -n emacs-git
Summary:       Git version control system support for Emacs
Summary(ja):   Emacs の Git サポート
Group:         Applications/Editors
Requires:      git = %{version}-%{release}, emacsen-common

%description -n emacs-git
%{summary}.

%package devel
Summary:	Header files for git-core
Summary(ja):	git-core 用ヘッダファイル
Group:		Development/Libraries

%description devel
Header files for git-core.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch10 -p1

sed -i.mac_ar 's|\$(AR) rcs \$@|\$(AR) -o \$@|g' Makefile
cat >config.mak <<EOF
prefix=%{_prefix}
NO_FINK=1
NO_DARWIN_PORTS=1
NO_R_TO_GCC_LINKER=1
CC_LD_DYNPATH=-L
GITWEB_PROJECTROOT=%{shared_dir}/git
GITWEB_JS=/gitweb/static/gitweb.js
GITWEB_CSS=/gitweb/static/gitweb.css
GITWEB_LOGO=/gitweb/static/git-logo.png
GITWEB_FAVICON=/gitweb/static/git-favicon.png
GITWEB_CONFIG_SYSTEM=%{_sysconfdir}/gitweb.conf
PYTHON_PATH=%{_bindir}/python
ETC_GITCONFIG=%{_sysconfdir}/gitconfig
EOF

%build
export VERSIONER_PERL_VERSION=5.8.9
make CC="/usr/bin/gcc-4.2 -arch i386 -arch x86_64" \
     AR="/usr/bin/libtool -static" \
     prefix=%{_prefix} all

%install
rm -rf $RPM_BUILD_ROOT
export VERSIONER_PERL_VERSION=5.8.9
make DESTDIR=$RPM_BUILD_ROOT \
     AR="/usr/bin/libtool -static" \
     gitwebdir_SQ=/Library/WebServer/CGI-Executables \
     gitwebstaticdir_SQ=/Library/WebServer/Documents/gitweb/static \
     install install-gitweb

mkdir -p html
tar jxf %{SOURCE100} -C html
find html -type f -name '*.txt' -exec rm {} ';'
mv html/*.{html,css} Documentation/

mkdir -p $RPM_BUILD_ROOT%{_mandir}
tar jxf %{SOURCE200} -C $RPM_BUILD_ROOT%{_mandir}

# perl-Git
# Error.pm provide by perl-Error package
rm -rf $RPM_BUILD_ROOT%{perl_vendorlib}/Error.pm

# emacs-git
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/git
mkdir -p $RPM_BUILD_ROOT%{emacsen_pkgdir}/install
mkdir -p $RPM_BUILD_ROOT%{emacsen_pkgdir}/remove

# install el files
install -m644 contrib/emacs/*.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/git/

# install vine-default file
install -m644 %{SOURCE1} %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/git/

# install  script( bytecompile el and install elc , remove )

%_installemacsenscript git %{SOURCE10}

%_removeemacsenscript  git %{SOURCE11}

# install plist file to LaunchDaemons
mkdir -p $RPM_BUILD_ROOT/Library/LaunchDaemons
install %{SOURCE2} $RPM_BUILD_ROOT/Library/LaunchDaemons

# install gitweb.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
sed "s|@PROJECTROOT@|%{shared_dir}/git|g" %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/gitweb.conf

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'

(find $RPM_BUILD_ROOT%{_libexecdir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citooli|git-daemon" | sed -e s@^$RPM_BUILD_ROOT@@)               > bin-man-doc-files
(find $RPM_BUILD_ROOT%{perl_sitelib} -type f | sed -e s@^$RPM_BUILD_ROOT@@) >> perl-files
(find $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT/Documentation -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@ -e 's/$/*/' ) >> bin-man-doc-files
mkdir -p $RPM_BUILD_ROOT/srv/git

# bash completion
bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 contrib/completion/git-completion.bash $bash_completion_dir/git

# header files and lib
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/xdiff
install *.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install xdiff/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/xdiff
install libgit.a $RPM_BUILD_ROOT%{_libdir}
install xdiff/lib.a $RPM_BUILD_ROOT%{_libdir}/libgit_xdiff.a

# make symbolic link to /Applications/OSXWS
mkdir -p $RPM_BUILD_ROOT%{_appdirmac}
ln -sf %{_datarootdir}/git-gui/lib/Git\ Gui.app $RPM_BUILD_ROOT%{_appdirmac}

# make directory for public git repositories
mkdir -p $RPM_BUILD_ROOT%{shared_dir}/git


%clean
rm -rf $RPM_BUILD_ROOT

%post -n emacs-git

# bytecompile and install

if [ "$1" = 2 ]; then

%_emacsenPackageRemove git

fi

%_addemacsenlist git

%_emacsenPackageInstall git

%preun -n emacs-git

if [ "$1" = 0 ]; then

%_emacsenPackageRemove git

%_removeemacsenlist git

fi


%files -f bin-man-doc-files
%defattr(-,root,wheel)
%{_bindir}/git
%{_bindir}/git-receive-pack
%{_bindir}/git-upload-archive
%{_bindir}/git-upload-pack
%{_bindir}/git-shell
%{_datadir}/git-core/
%doc README COPYING Documentation/*.txt contrib/hooks
%doc Documentation/*.html Documentation/docbook-xsl.css
%doc Documentation/howto Documentation/technical
%{_sysconfdir}/bash_completion.d

%files svn
%defattr(-,root,wheel)
%{_libexecdir}/git-core/*svn*
%doc Documentation/*svn*.txt
%{_mandir}/man1/*svn*.1*
%doc Documentation/*svn*.html

%files cvs
%defattr(-,root,wheel)
%doc Documentation/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{_libexecdir}/git-core/*cvs*
%{_mandir}/man1/*cvs*.1*
%doc Documentation/*git-cvs*.html

%files arch
%defattr(-,root,whell)
%doc Documentation/git-archimport.txt
%{_libexecdir}/git-core/git-archimport
%{_mandir}/man1/git-archimport.1*
%doc Documentation/git-archimport.html

%files email
%defattr(-,root,wheel)
%doc Documentation/*email*.txt
%{_libexecdir}/git-core/*email*
%{_mandir}/man1/*email*.1*
%doc Documentation/*email*.html

%files gui
%defattr(-,root,wheel)
%{_libexecdir}/git-core/git-gui*
%{_libexecdir}/git-core/git-citool
%{_datadir}/git-gui/
%{_mandir}/man1/git-gui.1*
%doc Documentation/git-gui.html
%{_mandir}/man1/git-citool.1*
%doc Documentation/git-citool.html
%{_appdirmac}/

%files -n gitk
%defattr(-,root,wheel)
%doc Documentation/*gitk*.txt
%{_bindir}/gitk
%{_datadir}/gitk
%{_mandir}/man1/*gitk*.1*
%doc Documentation/*gitk*.html

%files -n perl-Git -f perl-files
%defattr(-,root,wheel)


%files -n python-Git
%defattr(-,root,wheel)
%{python_sitelib}/*

%files -n emacs-git
%defattr(-,root,wheel)
%{_datadir}/emacs/site-lisp/git
%{emacsen_pkgdir}/install/git
%{emacsen_pkgdir}/remove/git

%files daemon
%defattr(-,root,wheel)
%{_libexecdir}/git-core/git-daemon
/Library/LaunchDaemons/osxws.git.daemon.plist
%defattr(777,root,wheel)
%dir %{shared_dir}/git

%files -n gitweb
%defattr(-,root,wheel)
%doc gitweb/README
/Library/WebServer/CGI-Executables/gitweb.cgi
/Library/WebServer/Documents/gitweb/static/
%config(noreplace) %{_sysconfdir}/gitweb.conf
%defattr(777,root,wheel)
%dir %{shared_dir}/git

%files devel
%defattr(644,root,wheel,755)
%{_includedir}/git
%{_libdir}/libgit.a
%{_libdir}/libgit_xdiff.a


%files all
# No files for you!

%changelog
* Wed Oct 26 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.7.1-0
- update to 1.7.7.1

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.5.1-4
- mofify python requirements for OSXWS

* Sun Jul  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.5.1-3
- remove unnecessary requires in perl-Git, git-svn

* Fri Jul  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.5.1-2
- remove unnecessary requires

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.5.1-1
- make more compatible with Vine Linux

* Thu May 19 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.5.1-0
- update to 1.7.5.1

* Sun Apr  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.4.2-0
- update to 1.7.4.2

* Wed Feb 16 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.4.1-0
- update to 1.7.4.1
- added Japanese user manual

* Tue Feb  8 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.3.5-2
- modified git-daemon and gitweb subpackages for Mac OS X

* Tue Jan 25 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.3.5-1
- virtual packaging based on Vine Linux
- remove git-daemon and gitweb

* Sat Jan  8 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.7.3.5-0
- initial build for Mac OS X WorkShop

