%define __python /usr/osxws/bin/python
%define shared_dir /Users/Shared

Summary: Mercurial source control management
Summary(ja): Mercurial ソースコード管理
Name: mercurial
Version: 1.8.3
Release: 0%{?_dist_release}
Source0: http://mercurial.selenic.com/release/mercurial-%{version}.tar.gz
Source1: mercurial-init.el
Source10: mercurial-el-install.sh
Source11: mercurial-el-remove.sh
Source20: hgweb.conf
Patch1: mercurial-hgk-fontsize.patch
License: GPLv2
Group: Development/Tools
URL: http://mercurial.selenic.com/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: bash-completion
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
Mercurial is a free, distributed source control management tool.
It offers you the power to efficiently handle projects of any size while using an intuitive interface.
It is easy to use and hard to break, making it ideal for anyone working with versioned files.

For mercurial beginner, see http://mercurial.selenic.com/wiki/BeginnersGuides

%description -l ja
Mercurial はフリーで配布されているソースコード管理ツールです。
直感的なインターフェースであらゆる規模のプロジェクトを効率良く扱う能力を提供します。
使いやすく、壊れにくく、バージョン管理されたファイルを扱うのに最適です。

mercurial 初心者の方は http://mercurial.selenic.com/wiki/JapaneseBeginnersGuides をみてみましょう。

%package el
Summary: Mercurial version control system support for Emacs
Summary(ja): Mercurial バージョン管理システム用 Emacs サポート
Group: Applications/Editors
Requires: %{name} = %{version}-%{release}, emacsen-common
Requires: emacsen

%description el
Contains byte compiled elisp packages for mercurial.
To get started: start emacs, load hg-mode with M-x hg-mode, and show
help with C-c h h

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
%setup -q -n %{name}-%{version}
%patch1 -p1
sed -i.osxws 's|/usr/local/bin/hg|%{_bindir}/hg|g' contrib/mercurial.el
sed -i.osxws 's|/home/user/hg/hg/contrib/hgk|%{_libexecdir}/mercurial/hgk|g' contrib/sample.hgrc
sed -i.osxws 's|/path/to/repo/or/config|%{_sysconfdir}/hgweb.conf|g' hgweb.cgi
sed -i.osxws 's|#!/usr/bin/env python|#!%{_bindir}/python|g' hgweb.cgi

%build
export CC="gcc-4.2"
export ARCHFLAGS="-arch i386 -arch x86_64"
export CFLAGS="-I%{_includedir}"
export LDFLAGS="-L%{_libdir}"
make all

%install
rm -rf $RPM_BUILD_ROOT
# install
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-script=%{_bindir}  --record=%{name}.files
make install-doc DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

# install contrib
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/mercurial
install -m 755 contrib/hgk $RPM_BUILD_ROOT%{_libexecdir}/mercurial/hgk
install -m 755 contrib/hg-ssh $RPM_BUILD_ROOT%{_bindir}
install -m 755 contrib/convert-repo $RPM_BUILD_ROOT%{_bindir}/mercurial-convert-repo

bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 contrib/bash_completion $bash_completion_dir/mercurial.sh

zsh_completion_dir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
mkdir -p $zsh_completion_dir
install -m 644 contrib/zsh_completion $zsh_completion_dir/_mercurial

hgrc_dir=$RPM_BUILD_ROOT%{_sysconfdir}/mercurial/hgrc.d
mkdir -p $hgrc_dir
install -m 644 contrib/mergetools.hgrc $hgrc_dir/mergetools.hgrc.sample

emacs_lisp_dir=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
mkdir -p $emacs_lisp_dir
install -p -m 644 contrib/{mercurial,mq}.el $emacs_lisp_dir
install -p -m 644 %{SOURCE1} $emacs_lisp_dir

mkdir -p $RPM_BUILD_ROOT%{_libdir}/emacsen-common/packages/install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/emacsen-common/packages/remove

%_installemacsenscript %{name} %{SOURCE10}

%_removeemacsenscript %{name} %{SOURCE11}

cat >hgk.rc <<EOF
[extensions]
# enable hgk extension ('hg help' shows 'view' as a command)
hgk=

[hgk]
path=%{_libexecdir}/mercurial/hgk
EOF
install hgk.rc $RPM_BUILD_ROOT%{_sysconfdir}/mercurial/hgrc.d

mkdir -p $RPM_BUILD_ROOT%{shared_dir}/mercurial
install -m 644 %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/Library/WebServer/CGI-Executables
install -m 755 hgweb.cgi $RPM_BUILD_ROOT/Library/WebServer/CGI-Executables

%clean
rm -rf $RPM_BUILD_ROOT

%post el
if [ $1 = $2 ]; then

    %_emacsenPackageRemove %{name}

fi

%_addemacsenlist %{name}

%_emacsenPackageInstall %{name}

%preun el
if [ $1 = 0 ]; then

    %_emacsenPackageRemove %{name}

    %_removeemacsenlist %{name}

fi

%files
%defattr(-,root,wheel)
%{_bindir}
%{python_sitelib}
%{_sysconfdir}/mercurial
%{_libexecdir}/mercurial
%{_sysconfdir}/bash_completion.d/mercurial.sh
%{_datadir}/zsh/site-functions/_mercurial
%{_mandir}/man?/hg*
%doc CONTRIBUTORS COPYING doc/README
%doc *.cgi contrib/*.fcgi contrib/*.wsgi
%doc contrib/sample.hgrc contrib/*.svg

%files el
%defattr(-,root,wheel)
%{_datadir}/emacs/site-lisp/*.el
%{_prefix}/lib/emacsen-common/packages/*/mercurial

%files hgweb
%defattr(-,root,wheel)
/Library/WebServer/CGI-Executables/hgweb.cgi
%config(noreplace) %{_sysconfdir}/hgweb.conf
%defattr(777,root,wheel)
%dir %{shared_dir}/mercurial

%changelog
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

