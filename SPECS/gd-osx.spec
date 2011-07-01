Summary: A graphics library for drawing .png files.
Summary(ja): PNGイメージファイルを描写するためのグラフィックライブラリ
Name: gd
Version: 2.0.35
Release: 2%{_dist_release}
Source0: http://www.libgd.org/releases/gd-%{version}.tar.bz2
Patch1:  gd-2.0.35-overflow.patch
Patch2:  gd-2.0.35-CVE-2009-3546.diff
License: BSD
URL: http://www.libgd.org/
Group: System Environment/Libraries

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libjpeg-devel zlib-devel freetype-devel
BuildRequires: libpng-devel >= 2:1.2.5
Provides: libgd = %{version}-%{release}
Obsoletes: libgd
BuildArch: fat

%description
Gd is a graphics library for drawing .png files.  Gd allows your code to
quickly draw images (lines, arcs, text, multiple colors, cutting and
pasting from other images, flood fills) and write out the result as a
.png file. Gd is particularly useful in web applications, where .pngs
are commonly used as inline images.  Note, however, that gd is not a
paint program.

Install gd if you are developing applications which need to draw .png
files.  If you install gd, you'll also need to install the gd-devel
package.

%description -l ja
GdはPNGファイルを描写するためのグラフックライブラリです。 Gdを使って、
画像(線や弧, テキスト, カラー, 他の画像からのカット＆ペースト等々)を
簡単に描写して、PNGファイルへ結果を出力することができます。
Gdは特に、一般にPNG画像を埋め込む必要のあるウェブアプリケーションで
便利です。ただし、注意して欲しいのは, Gdはペイントツールではありませ
ん。

PNGファイルを描写する必要のあるアプリケーションを開発する場合、
Gdをインストールしてください。gdをインストールした場合、gd-devel
パッケージも必要になります。

%package progs
Summary: Utility programs that use libgd.
Summary(ja): libgd を用いたユーティリティプログラム
Group: Applications/Graphics
Requires: gd = %{version}, perl

%description progs
These are utility programs supplied with gd, the .png graphics library.
If you install these, you must install gd.

%description progs -l ja
これは PNG グラフィックライブラリ gd によって提供されるユーティリティ
プログラムです。これをインストールするには, gdをインストールする必要
があります。

%package devel
Requires: gd = %{version}
Summary: The development libraries and header files for gd.
Summary(ja): gd用の開発ライブラリとヘッダファイル
Group: Development/Libraries

%description devel
These are the development libraries and header files for gd, the .png
graphics library.

If you're installing the gd graphics library, you must install gd-devel.

%description devel -l ja
これらは開発ライブラリです。
PNGグラフィックライブラリ gd 用の開発ライブラリおよびヘッダファイル
です。

gdをインストールした場合、gd-develパッケージも必要になります。

%prep
%setup -q -c %{name}-%{version}
mv %{name}-%{version} INTEL
pushd INTEL
%patch1 -p1 -b .overflow
%patch2 -p0 -b .CVE-2009-3546
popd
cp -Rp  INTEL X86_64

%build
pushd INTEL
export CFLAGS="-O3 -arch i386 -mtune=pentium-m -I/usr/X11/include -I%{_includedir}"
export CXXFLAGS="$CFLAGS" \
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
%configure --with-jpeg=%{_prefix} \
           --host=%{_rpm_platform32} \
           --build=%{_rpm_platform32} \
           --target=%{_rpm_platform32} \
           CPPFLAGS="-DJISX0208"

make
popd

pushd X86_64
export CFLAGS="-O3 -arch x86_64 -mtune=core2 -I/usr/X11/include -I%{_includedir}"
export CXXFLAGS="$CFLAGS" \
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
%configure --with-jpeg=%{_prefix} \
           --host=%{_rpm_platform64} \
           --build=%{_rpm_platform64} \
           --target=%{_rpm_platform64} \
           CPPFLAGS="-DJISX0208"
make
cp -fRp COPYING INSTALL NEWS ..
cp -fRP README-JPEG.txt readme.jpn README.TESTING README.TXT ..
cp -fRP index.html ..
popd

%check
for arch in INTEL X86_64; do
    pushd $arch
    make check
    popd
done

%install
rm -rf $RPM_BUILD_ROOT

PWD=`pwd`
for arch in INTEL X86_64; do
    pushd $arch
    rm -rf ${PWD}-root
    make install DESTDIR=${PWD}-root
    make install-man DESTDIR=${PWD}-root
    popd
done

# make Universal Binaries concatnate by lipo
filelist=$(find ./INTEL-root -type f | xargs file | sed -e 's,^\./INTEL-root/,,g' | \
        grep -E \(Mach-O\)\|\(ar\ archive\) |sed -e 's,:.*,,g' -e '/\for\ architecture/d')
for i in $filelist; do
    /usr/bin/lipo -create INTEL-root/$i X86_64-root/$i -output `basename $i`
    cp -f `basename $i` INTEL-root/$i
done

# check header files
for i in `find INTEL-root -name "*.h" -type f`; do
    TARGET=`echo $i | sed -e "s,.*INTEL-root,,"`
    TEMP=`diff -u INTEL-root/$TARGET X86_64-root/$TARGET > /dev/null || echo different`
    if [ -n "$TEMP" ]; then
        mv X86_64-root/$TARGET INTEL-root/${TARGET%.*}-x86_64.h
        mv INTEL-root/$TARGET INTEL-root/${TARGET%.*}-i386.h
        FILE=${TARGET##*/}
        FILE=${FILE%.*}
        cat <<EOF > INTEL-root/$TARGET
#if defined (__i386__)
#include "${FILE}-i386.h"
#elif defined( __x86_64__ )
#include "${FILE}-x86_64.h"
#endif
EOF
    fi
done

# install
mkdir -p $RPM_BUILD_ROOT
tar cf - -C INTEL-root . | tar xpf - -C $RPM_BUILD_ROOT

# clean extraneous
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_libdir}/*.*.dylib
%defattr(644,root,wheel,755)
%doc COPYING INSTALL NEWS
%doc README-JPEG.txt readme.jpn README.TESTING README.TXT

%files progs
%defattr(-,root,wheel)
%{_bindir}/*

%files devel
%defattr(-,root,wheel)
%{_includedir}/*
%{_libdir}/*.dylib
%{_libdir}/*.a
%defattr(644,root,wheel,755)
%doc index.html

%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.35-2
- reorganize sub-packages due to Vine Linux comaptivility

* Sat Feb  5 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.35-1
- modified permission of documentations.

* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.35-0
- initial build for Mac OS X WorkShop

