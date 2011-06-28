%define libname gd

Summary: A graphics library for fast image creation
Summary(ja): 高速な画像生成ライブラリ
Name: lib%{libname}
Version: 2.0.35
Release: 1%{?_dist_release}
Source0: http://www.libgd.org/releases/%{libname}-%{version}.tar.gz
License: BSD
Group: System Environment/Libraries
URL: http://www.libgd.org/

Requires: libpng libjpeg freetype zlib
BuildRequires: libpng-devel libjpeg-devel freetype-devel zlib-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
gd is a graphics library. It allows your code to quickly draw images complete with lines, arcs, text, multiple colors, cut and paste from other images, and flood fills, and write out the result as a PNG or JPEG file. This is particularly useful in World Wide Web applications, where PNG and JPEG are two of the formats accepted for inline images by most browsers.

gd is not a paint program. If you are looking for a paint program, you are looking in the wrong place. If you are not a programmer, you are looking in the wrong place, unless you are installing a required library in order to run an application.

gd does not provide for every possible desirable graphics operation. It is not necessary or desirable for gd to become a kitchen-sink graphics package, but version 2.0 does include most frequently requested features, including both truecolor and palette images, resampling (smooth resizing of truecolor images) and so forth.

%description
gd はグラフィックライブラリです。
gd は高速な画像描画を可能にし、線や円弧、テキスト、多色、
他の画像からのカットアンドペースト、flood fill 等を完備しており、
結果を PNG や JPEG として書き出します。
特に Web アプリケーションの一部として、ほとんどのブラウサーで許容されるようなPNG や JPEG をインライン画像を提供するのは有用です。

gd はペイントプログラムではありません。
画像を生成するライブラリとして、またはアプリケーションの実行に必要なライブラリとして利用できます。

gd は何もかが含まれるようなグラフィックパッケージである必要は無いため、
一部の画像操作の機能のみを提供します。
しかし、gd 2.0 では要望が多かった機能として、truecolor と palette image と
resampling (truecolor 画像の滑かなサイズ変更), forth が含まれています。

%package devel
Summary: The development libraries and header files for gd
Summary(ja): gd 開発ライブラリ、ヘッダファイル
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.

%description -l ja devel
gd-devel パッケージは高速な画像生成ライブラリ gd の開発ライブラリとヘッダファイルを提供します。

%prep
%setup -q -c %{libname}-%{version}
mv %{libname}-%{version} INTEL
cp -Rp  INTEL X86_64

%build
pushd INTEL
export CFLAGS="-O3 -arch i386 -mtune=pentium-m -I/usr/X11/include -I%{_includedir}"
export CXXFLAGS="$CFLAGS" \
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
%configure --with-jpeg=%{_prefix} \
           --host=%{_rpm_platform32} \
           --build=%{_rpm_platform32} \
           --target=%{_rpm_platform32}
make
popd

pushd X86_64
export CFLAGS="-O3 -arch x86_64 -mtune=core2 -I/usr/X11/include -I%{_includedir}"
export CXXFLAGS="$CFLAGS" \
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
%configure --with-jpeg=%{_prefix} \
           --host=%{_rpm_platform64} \
           --build=%{_rpm_platform64} \
           --target=%{_rpm_platform64}
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
%{_libdir}/%{name}.*.dylib
%{_bindir}/*
%exclude %{_bindir}/gdlib-config
%defattr(644,root,wheel,755)
%doc COPYING INSTALL NEWS
%doc README-JPEG.txt readme.jpn README.TESTING README.TXT

%files devel
%defattr(-,root,wheel)
%{_includedir}/*
%{_libdir}/%{name}.a
%{_libdir}/%{name}.dylib
%{_bindir}/gdlib-config
%defattr(644,root,wheel,755)
%doc index.html

%changelog
* Sat Feb  5 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.35-1
- modified permission of documentations.

* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.0.35-0
- initial build for Mac OS X WorkShop

