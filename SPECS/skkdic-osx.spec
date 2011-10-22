Summary: SKK Dictionaries
Name: skkdic
Version: 20100126
Release: 2%{?_dist_release}
Url: http://openlab.ring.gr.jp/skk/
Group: Applications/Text
License: Distrubutable
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gzip

Source0: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.L.gz
Source1: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.JIS2.gz
Source2: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.JIS3_4.gz
Source3: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.pubdic+.gz
Source4: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.edict.tar.gz
Source5: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.assoc.gz
Source6: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.china_taiwan.gz
#Source7: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.fukugo.gz
Source8: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.geo.gz
Source9: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.itaiji.gz
Source10: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.law.gz
Source11: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.mazegaki.gz
Source12: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.okinawa.gz
Source13: http://openlab.ring.gr.jp/skk/dic/SKK-JISYO.jinmei.gz
Source14: http://openlab.ring.gr.jp/skk/dic/zipcode.tar.gz

Source100: dot-dic.skk

%description
SKK dictionaries

%description -l ja
SKK 辞書パッケージです。
%{_defaultdocdir}/%{name}-%{version}/dot-dic.skk
を ~/.skk としてコピーして使用してください。

%prep
%setup -n %{name} -c -T -a 4 -a 14
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE5} %{SOURCE6} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} .
gzip -d *.gz

cp %{SOURCE100} .

mkdir -p DOCS/zipcode
cp zipcode/Makefile.in zipcode/README.ja zipcode/ZIPCODE-MK zipcode/words.zipcode DOCS/zipcode/

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/skk
install -m 644 SKK-JISYO.* $RPM_BUILD_ROOT%{_datadir}/skk
install -m 644 zipcode/SKK-JISYO.* $RPM_BUILD_ROOT%{_datadir}/skk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc DOCS/* dot-dic.skk edict_doc.txt
%{_datadir}/skk/SKK-JISYO.*

%changelog
* Sat Oct 22 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 20100126-2
- initial build for Mac OS X WorkShop 

* Sun Aug 29 2010 IWAI, Masaharu <iwai@alib.jp> 20100126-1
- update to 20100126
- drop SKK-JISYO.fukugo.gz (Source7): upstream removed 2003-04-05
- update dot-dic.skk (Source100): drop SKK-JISYO.fukugo
- s/BuildArchitectures/BuildArch/

* Sat Oct 11 2008 Shu KONNO <owa@bg.wakwak.com> 20030520-1vl5
- applied new versioning policy, spec in utf-8

* Sat May 24 2003 KOBAYASHI R. Taizo <tkoba@vinelinux.org>
- 20030520-0vl2
- added dot-dic.skk

* Tue May 20 2003 KOBAYASHI R. Taizo <tkoba@vinelinux.org>
- 20030520-0vl1

* Tue Mar  7 2001 Uechi Yasumasa <uh@u.dhis.portside.net>
- 20010306-0vl1
- 1st release
