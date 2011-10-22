%define _noVersionedDependencies        1
%define prereq_ge()  %(LC_ALL="C" rpm -q --queryformat 'PreReq:%%{NAME} >= %%{VERSION}' %1| grep -v "is not")
%define _libdir %{_prefix}/lib

Summary:      SKK for emacs
Summary(ja):  Emacs 用 SKK (かな漢字変換プログラム)
Name:         skk
Version:      13.1
Release:      1%{?_dist_release}

Source0:      http://openlab.ring.gr.jp/skk/maintrunk/ddskk-%{version}.tar.gz
Source1:      %{name}-install.sh
Source2:      %{name}-remove.sh
Source3:      %{name}-init.el
Source4:      vine-default-%{name}.el
Patch0:       ddskk-11.4-tut.patch
Patch1:       ddskk-11.6.0-make.patch
Patch2:       ddskk-info.patch

License:      GPL
Group:        Applications/Editors/Emacs
BuildRoot:    %{_tmppath}/%{name}-%{version}-root
BuildArch:    noarch

PreReq:       emacsen, make, install-info, skkdic
%prereq_ge    emacsen-common
%prereq_ge    apel
BuildPreReq:  emacsen-common, apel

Obsoletes:    ddskk
Vendor:       Project Vine
Distribution: Vine Linux

%description
Daredevil SKK is a branch of SKK (Simple Kana to Kanji conversion
program, an input method of Japanese).  It forked from the maintrunk,
SKK version 10.56.

%description -l ja
Daredevil SKK は、かな漢字変換プログラムです。
又、Daredevil SKK は SKK 10.56 から派生したバージョンです。

rskkserv をインストールしている場合は、
~/.emacs に、以下の設定をして下さい。

(setq skk-server-portnum 1178)
(setq skk-server-host "localhost")


NICOLA-DDSKK も同梱しています。
NICOLA-DDSKK とは、Daredevil SKK で NICOLA かな入力（親指シフト入力）
によって日本語入力を可能にするものです。

設定等は、%{_docdir}/%{name}-%{version}/nicola-ddskk/README.NICOLA.ja を
参照して下さい。


%prep

%setup -q -n ddskk-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -f *.orig

%__cp -af %{SOURCE3} %{SOURCE4} .

%build
make info

mkdir nicola-ddskk
cp -pf nicola/{ChangeLog*,README.*} nicola-ddskk

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
[ "${RPM_BUILD_ROOT}" != "/" ] && mkdir -p ${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}
mkdir -p $RPM_BUILD_ROOT%{emacsen_pkgdir}/{install,remove}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}/nicola

#
# install el files
# 

cp -af Makefile SKK-MK *.el *.in etc ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/%{name}

cp -f nicola/{Makefile,NICOLA-DDSKK-*,*.el} \
  $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}/nicola

#
# install  script( bytecompile el and install elc , remove )   
#

%_installemacsenscript %{name} %{SOURCE1} 

%_removeemacsenscript  %{name} %{SOURCE2}

#
# install info file
# 
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
install -m 644 doc/skk.info* ${RPM_BUILD_ROOT}%{_infodir}

( cd ${RPM_BUILD_ROOT}%{_infodir}
  for i in skk.info skk.info-1 skk.info-2 skk.info-3 skk.info-4 ; do
    nkf -Je $i > $i.euc
    mv -f $i.euc $i
    gzip -9 $i
  done
)

%post 
#
# bytecompile and install 
#

if [ "$1" = 2 ]; then

%_emacsenPackageRemove %{name}

fi

%_addemacsenlist %{name}

%_emacsenPackageInstall %{name}

/sbin/install-info %{_infodir}/skk.info.gz %{_infodir}/dir

%preun

if [ "$1" = 0 ]; then

%_emacsenPackageRemove %{name}

%_removeemacsenlist %{name}

/sbin/install-info --delete %{_infodir}/skk.info.gz %{_infodir}/dir

fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc READMEs ChangeLog* etc/Emacs.ad
%doc nicola-ddskk
%{_infodir}/*.info*
%{_datadir}/emacs/site-lisp/%{name}/
%{emacsen_pkgdir}/install/%{name}
%{emacsen_pkgdir}/remove/%{name}


%changelog
* Sun Aug 29 2010 IWAI, Masaharu <iwai@alib.jp> 13.1-1
- new upstream release
 - update skk-install.sh: update VERSION
- using emacsen_pkgdir rpm macro
- check emacs-ime value in vine-default-skk.el

* Sat Apr 11 2009 Munehiro Yamamoto <munepi@cg8.so-net.ne.jp> 11.6.0-2
- added vine-default-skk.el, skk-init.el
- updated skk-install.sh for vine-default-skk.el

* Sat Aug 16 2008 Shu KONNO <owa@bg.wakwak.com> 11.6.0-1vl5
- applied new versioning policy, spec in utf-8
- added %%define _libdir %%{_prefix}/lib

* Tue Sep 12 2006 Ryoichi INAGAKI <ryo1@bc.wakwak.com> 11.6.0-0vl6
- changed Group to Appliations/Editors/Emacs <BTS:VineLinux:163>

* Thu Jul 20 2006 Ryoichi INAGAKI <ryo1@bc.wakwak.com> 11.6.0-0vl5
- s/Copyright/License/
- changed Group to Applications/Editors/EmacsLisp

* Tue May 20 2003 KOBAYASHI R. Taizo <tkoba@vinelinux.org> 11.6.0-0vl4
- added PreReq skkdic

* Sun May 26 2002 MATUBARA Kazuyuki <matubara@kamome.or.jp> 11.6.0-0vl3
- package name changed from ddskk to skk

* Sat Apr 20 2002 MATUBARA Kazuyuki <matubara@kamome.or.jp> 11.6.0-0vl2
- delete xemacs message to ddskk-install.sh

* Sun Mar 03 2002 MATUBARA Kazuyuki <matubara@mb.asmnet.ne.jp> 11.6.0-0vl1
- 1st packageing
