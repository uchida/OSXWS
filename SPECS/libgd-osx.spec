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
%setup -q -n %{libname}-%{version}

%build
export CFLAGS="-I/usr/X11/include -I%{_includedir}"
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} \
            --bindir=%{_bindir} --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --sharedstatedir=%{_sharedstatedir} \
            --mandir=%{_mandir} --infodir=%{_infodir} \
            --with-jpeg=%{_prefix} \
            CC='gcc-4.2 -arch i386 -arch x86_64' \
            CPP='gcc-4.2 -E'
make

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
make install-man DESTDIR=$RPM_BUILD_ROOT

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

