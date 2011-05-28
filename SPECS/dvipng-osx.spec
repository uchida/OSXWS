Summary: A DVI-to-PNG converter
Summary(ja): DVI ファイルから PNG ファイルへの変換ユーティリティ
Name: dvipng
Version: 1.13
Release: 0%{?_dist_release}
Source0: http://download.savannah.gnu.org/releases/dvipng/%{name}-%{version}.tar.gz
License: LGPLv3
Group: Applications/Publishing 
URL: http://savannah.nongnu.org/projects/dvipng/

Requires: libgd, tetex, freetype, libpng, zlib
BuildRequires: libgd-devel, tetex, freetype-devel, libpng-devel, zlib-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
This program makes PNG and/or GIF graphics from DVI files as obtained 
from TeX and its relatives. 
If GIF support is enabled, GIF output is chosen by using the 
`dvigif' binary or with the `--gif' option. 

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
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc ChangeLog COPYING COPYING.LESSER INSTALL README RELEASE
%{_bindir}/dvi*
%{_mandir}/man1/dvi*.1*
%{_infodir}/dvipng.info*

%post
install-info %{_infodir}/dvipng.info %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
    install-info --delete %{_infodir}/dvipng.info %{_infodir}/dir
fi

%changelog
* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.13-0
- initial build for Mac OS X WorkShop

