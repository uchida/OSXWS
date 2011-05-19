%define shared_dir /Users/Shared
Summary: the fast version control system
Summary(ja): 高速なバージョン管理システム
Name: git
Version: 1.7.5.1
Release: 0%{?_dist_release}
Source0: http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.bz2
Source1: http://kernel.org/pub/software/scm/git/%{name}-htmldocs-%{version}.tar.bz2
Source2: http://kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.bz2
Source3: http://www8.atwiki.jp/git_jp/pub/git-manual-jp/Documentation/user-manual.zip
Source10: %{name}-install.sh
Source11: %{name}-remove.sh
Source12: git-init.el
Source20: osxws.git.daemon.plist
Source30: gitweb.conf.in
Patch0: git-perl-macosx.patch
Patch1: git_remote_helpers.patch
Patch10: git-1.5-gitweb-home-link.patch
License: GPLv2
Group: Development/Tools
URL: http://git-scm.com

Requires: perl >= 5.8
Requires: python >= 2.6.6
Requires: bash-completion
BuildRequires: python >= 2.6.6
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
Git is a free & open source, distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

Every Git clone is a full-fledged repository with complete history and full revision tracking capabilities, not dependent on network access or a central server.
Branching and merging are fast and easy to do.

For git beginners, see http://www.kernel.org/pub/software/scm/git/docs/gittutorial.html or
  $ man gittutorial

%description -l ja
Git はオープンソースでフリーな小規模から大規模までのプロジェクトを高速に扱うバージョン管理システムです。

全ての Git clone 完全に自立したはリポジトリで、ネットワークアクセスや中央サーバーに依存せず完全な履歴を持ち、全ての修正を追跡できます。
ブランチやマージも高速で簡単に行なえます。

git 初心者の方は http://www8.atwiki.jp/git_jp/pub/git-manual-jp/Documentation/gittutorial.html をみてみるとよいでしょう。

%package all
Summary:        Meta-package to pull in all git tools
Summary(ja):    すべての git ツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}
Requires:       git-daemon = %{version}-%{release}
Requires:       gitweb = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-arch = %{version}-%{release}
Requires:       git-cvs = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}
Requires:       emacs-git = %{version}-%{release}
%description all
Git is a free & open source, distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

Every Git clone is a full-fledged repository with complete history and full revision tracking capabilities, not dependent on network access or a central server. Branching and merging are fast and easy to do.

This is a dummy package which brings in all subpackages.

%description -l ja all
Git はオープンソースでフリーな小規模から大規模までのプロジェクトを高速に扱うバージョン管理システムです。

全ての Git clone 完全に自立したはリポジトリで、ネットワークアクセスや中央サーバーに依存せず完全な履歴を持ち、全ての修正を追跡できます。
ブランチやマージも高速で簡単に行なえます。

このパッケージはサブパッケージすべてをインストールする仮想パッケージです。

%package daemon
Summary:        Git protocol daemon
Summary(ja):    Git プロトコルデーモン
Group:          Development/Tools
Requires:       git = %{version}-%{release}
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
Requires:       perl-Git = %{version}-%{release}
%description svn
%{summary}.

%package cvs
Summary:        Git tools for importing CVS repositories
Summary(ja):    CVS リポジトリを git へインポートするためのツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, cvs
%description cvs
%{summary}.

%package arch
Summary:        Git tools for importing Arch repositories
Summary(ja):    Arch リポジトリを git へインポートするためのツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}
%description arch
Git tools for importing Arch repositories.

%package email
Summary:        Git tools for sending email
Summary(ja):    Eメールを送るための git ツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, perl-Git = %{version}-%{release}
%description email
%{summary}.

%package gui
Summary:        Git GUI tool
Summary(ja):    Git の GUI ツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tk
%description gui
%{summary}.

%package -n gitk
Summary:        Git revision tree visualiser
Summary(ja):    Git リビジョンツリー可視化ツール
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tk
%description -n gitk
%{summary}.

%package -n perl-Git
Summary:        Perl interface to Git
Summary(ja):    Git の perl インタフェース
Group:          Development/Libraries
Requires:       git = %{version}-%{release}
%description -n perl-Git
%{summary}.

%package -n python-Git
Summary:        Python interface to Git
Summary(ja):    Git の python インタフェース
Group:          Development/Libraries
Requires:       git = %{version}-%{release}, python >= 2.6.6
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
Summary:        Header files for git-core
Summary(ja):    git-core 用ヘッダファイル
Group:          Development/Libraries
%description devel
%{summary}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch10 -p1
sed -i.ar 's|\$(AR) rcs \$@|\$(AR) -o \$@|g' Makefile
cat >config.mak <<EOF
prefix=%{_prefix}
DESTDIR=%{buildroot}
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
make CC="gcc-4.2 -arch i386 -arch x86_64" \
     AR="libtool -static" \
     all

%install
rm -rf $RPM_BUILD_ROOT
make CC="gcc-4.2 -arch i386 -arch x86_64" \
     AR="libtool -static" \
     gitwebdir_SQ=/Library/WebServer/CGI-Executables \
     gitwebstaticdir_SQ=/Library/WebServer/Documents/gitweb/static \
     install

mkdir -p html
tar jxf %{SOURCE1} -C html
find html -type f -name '*.txt' -exec rm {} ';'
rm -r html/RelNotes

mkdir -p $RPM_BUILD_ROOT%{_mandir}
tar jxf %{SOURCE2} -C $RPM_BUILD_ROOT%{_mandir}
for man in `find $RPM_BUILD_ROOT%{_mandir} -type f`; do
    sed -i."tmp" "s,/usr/bin/git,%{_bindir}/git,g" $man
    sed -i."tmp" "s,/usr/libexec/git-core,%{_libexecdir}/git-core,g" $man
    sed -i."tmp" "s,/usr/share/git-core,%{_datarootdir}/git-core,g" $man
    sed -i."tmp" "s,\$(prefix),%{_prefix},g" $man
    rm -f $man.tmp
done

unzip %{SOURCE3}
mv user-manual user-manual-ja

# emacs-git
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/git
mkdir -p $RPM_BUILD_ROOT%{_libdir}/emacsen-common/packages/install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/emacsen-common/packages/remove
# install el files
install -m644 contrib/emacs/*.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/git/

%_installemacsenscript %{name} %{SOURCE10}

%_removeemacsenscript %{name} %{SOURCE11}

# install init-el
install -m644 %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/git/

# make symbolic link to /Applications/OSXWS
mkdir -p $RPM_BUILD_ROOT%{_appdirmac}
ln -sf %{_datarootdir}/git-gui/lib/Git\ Gui.app $RPM_BUILD_ROOT%{_appdirmac}

# bash completion
bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 contrib/completion/git-completion.bash $bash_completion_dir/git

# install plist file to LaunchDaemons
mkdir -p $RPM_BUILD_ROOT/Library/LaunchDaemons
install %{SOURCE20} $RPM_BUILD_ROOT/Library/LaunchDaemons

# install gitweb.conf
sed "s|@PROJECTROOT@|%{shared_dir}/git|g" %{SOURCE30} > %{buildroot}%{_sysconfdir}/gitweb.conf

# make directory for public git repositories
mkdir -p $RPM_BUILD_ROOT%{shared_dir}/git

# remove extraneous
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT/Library/Perl/Updates

# remember files
(find $RPM_BUILD_ROOT%{_libexecdir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citooli|git-daemon" | sed -e s@^$RPM_BUILD_ROOT@@) > bin-man-doc-files
(find $RPM_BUILD_ROOT%{perl_vendorlib} -type f | sed -e s@^$RPM_BUILD_ROOT@@) >> perl-files
(find $RPM_BUILD_ROOT%{_mandir} -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@ -e 's/$/*/' ) >> bin-man-doc-files

# header files and lib
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/xdiff
install *.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install xdiff/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/xdiff
install libgit.a $RPM_BUILD_ROOT%{_libdir}
install xdiff/lib.a $RPM_BUILD_ROOT%{_libdir}/libgit_xdiff.a

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

%preun daemon
if [ "$1" = 0 ]; then
    launchctl load /Library/LaunchDaemons/osxws.git.daemon.plist
    launchctl unload -w /Library/LaunchDaemons/osxws.git.daemon.plist
fi

%files -f bin-man-doc-files
%defattr(-,root,wheel)
%{_bindir}/git
%{_bindir}/git-receive-pack
%{_bindir}/git-upload-archive
%{_bindir}/git-upload-pack
%{_bindir}/git-shell
%{_datarootdir}/git-core/
%{_sysconfdir}/bash_completion.d/git
%doc COPYING INSTALL README Documentation/RelNotes
%doc html/
%doc user-manual-ja/

%files svn
%defattr(-,root,wheel)
%{_libexecdir}/git-core/*svn*
%{_mandir}/man1/*svn*.1*
%doc html/*svn*.html

%files cvs
%defattr(-,root,wheel)
%{_bindir}/git-cvsserver
%{_libexecdir}/git-core/*cvs*
%{_mandir}/man1/*cvs*.1*
%doc html/*git-cvs*.html

%files arch
%defattr(-,root,wheel)
%{_libexecdir}/git-core/git-archimport
%{_mandir}/man1/git-archimport.1*
%doc html/git-archimport.html

%files email
%defattr(-,root,wheel)
%{_libexecdir}/git-core/*email*
%{_mandir}/man1/*email*.1*
%doc html/*email*.html

%files gui
%defattr(-,root,wheel)
%{_libexecdir}/git-core/git-gui*
%{_libexecdir}/git-core/git-citool
%{_datarootdir}/git-gui/lib/
%{_appdirmac}/
%{_mandir}/man1/git-gui.1*
%doc html/git-gui.html
%{_mandir}/man1/git-citool.1*
%doc html/git-citool.html

%files -n gitk
%defattr(-,root,wheel)
%{_bindir}/gitk
%{_datadir}/gitk
%{_mandir}/man1/*gitk*.1*
%doc html/*gitk*.html

%files -n perl-Git
%defattr(-,root,wheel)
%{perl_sitelib}/*

%files -n python-Git
%defattr(-,root,wheel)
%{python_sitelib}/*

%files -n emacs-git
%defattr(-,root,wheel)
%{_datadir}/emacs/site-lisp/git
%{_libdir}/emacsen-common/packages/*/git

%files daemon
%defattr(-,root,wheel)
%{_libexecdir}/git-core/git-daemon
/Library/LaunchDaemons/osxws.git.daemon.plist
%defattr(777,root,wheel)
%dir %{shared_dir}/git

%files -n gitweb
%defattr(-,root,wheel)
/Library/WebServer/CGI-Executables/gitweb.cgi
/Library/WebServer/Documents/gitweb/static/
%config(noreplace) %{_sysconfdir}/gitweb.conf
%doc gitweb/README
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

