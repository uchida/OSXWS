Name:             dvipng
Version:          1.13
Release:          1%{?_dist_release}

Summary:          Converts DVI files to PNG/GIF format
Summary(ja):      DVIファイルをPNG/GIF画像に変換
Source:           %{name}-%{version}.tar.gz
URL:              http://sourceforge.net/projects/dvipng/
Group:            Applications/Publishing
License:          LGPLv3

BuildRequires:    libkpathsea-devel
BuildRequires:    gd-devel
BuildRequires:    zlib-devel
BuildRequires:    libpng-devel
BuildRequires:    tetex
BuildRequires:    freetype-devel

BuildRoot:        %{_tmppath}/%{name}-%{version}-root
BuildArch:        fat

%description
This program makes PNG and/or GIF graphics from DVI files as obtained
from TeX and its relatives.

It is intended to produce anti-aliased screen-resolution images as
fast as is possible. The target audience is people who need to generate
and regenerate many images again and again. 


%description -l ja
TeX やその関連ツールにより作成される DVI ファイルを 
PNG または GIF 画像に変換するプログラムです。

可能な限り素早くアンチエリアスが効いた画面解像度の画像を生成します。
このソフトの主な対象者は、多数の画像を何度も繰り返し再生成したい人です。 


%prep
%setup -q

%build
export CFLAGS="-I/usr/X11/include -I%{_includedir} -no-cpp-precomp"
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
%configure \
    CC='/usr/bin/gcc-4.2 -arch i386 -arch x86_64' \
    CXX='/usr/bin/gcc-4.2 -arch i386 -arch x86_64' \
    CPP="/usr/bin/gcc-4.2 -E" CXXCPP="/usr/bin/g++-4.2 -E"
make

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

rm -rf ${RPM_BUILD_ROOT}/%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%post 
/sbin/install-info %{_infodir}/dvipng.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ "$1" = "0" ] ; then 
    /sbin/install-info --delete %{_infodir}/dvipng.info %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog ChangeLog.0 README RELEASE
%{_bindir}/dvigif
%{_bindir}/dvipng
%{_infodir}/dvipng.info*
%{_mandir}/man1/dvigif.1*
%{_mandir}/man1/dvipng.1*


%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.13-1
- make more compatible with Vine Linux

* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.13-0
- initial build for Mac OS X WorkShop

