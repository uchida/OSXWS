Name: graphviz
Summary: Graph Visualization Tools
Version: 2.26.3
Release: 0%{?_dist_release}
Group: 	Applications/Multimedia
License: CPL
URL: http://www.graphviz.org/
Source0: http://www.graphviz.org/pub/graphviz/ARCHIVE/%{name}-%{version}.tar.gz
Patch0: graphviz-ptrdiff.patch
Patch1: graphviz-quartz-libtool.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkgconfig libpng-devel libgd-devel
BuildRequires: cairo-devel freetype-devel
BuildRequires: urw-fonts
BuildRequires: zlib-devel
BuildRequires: ghostscript-devel
BuildArch: fat

%description
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts).

%package devel
Group: 	Development/Libraries
Summary: Development package for graphviz
Requires: %{name} = %{version}-%{release}, pkgconfig

%description devel
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts). This package contains development files for 
graphviz.

%package doc
Group: 	Documentation
Summary: PDF and HTML documents for graphviz
BuildArch: noarch

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="-I/usr/X11/include -I%{_includedir}"
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
%configure --disable-static \
           --with-quartz \
           --with-libgd \
           --with-ghostscript \
           --with-pangocairo \
           --without-x \
           --without-gtk \
           --without-gdk-pixbuf \
           --without-lasi \
           --without-gtkgl \
           --without-gtkglext \
           --without-glade \
           --without-glitz \
           --without-rsvg \
           --without-mylibgd \
           --without-gts \
           --disable-python \
           --disable-java \
           --disable-r \
           --disable-lua \
           --disable-tcl \
           --disable-ruby \
           --disable-perl \
           --disable-php \
           CC='/usr/bin/gcc-4.2 -arch i386 -arch x86_64' \
           CPP='/usr/bin/gcc-4.2 -E'
sed -i.tag 's|LTOBJCCOMPILE = $(LIBTOOL)|LTOBJCCOMPILE = $(LIBTOOL) --tag=CC|g' plugin/quartz/Makefile
make

%install rm -rf %{buildroot} __doc
make DESTDIR=%{buildroot} \
 docdir=%{buildroot}%{_docdir}/%{name} \
 pkgconfigdir=%{_libdir}/pkgconfig \
 install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
chmod -x %{buildroot}%{_datadir}/%{name}/lefty/*
cp -a %{buildroot}%{_datadir}/%{name}/doc __doc
rm -rf %{buildroot}%{_datadir}/%{name}/doc

%clean
rm -rf %{buildroot}

%post
%{_bindir}/dot -c

# if there is no dot after everything else is done, then remove config
%postun
if [ $1 -eq 0 ]; then
 rm -f %{_libdir}/graphviz/config || :
fi

%files
%defattr(-,root,wheel)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/*
%dir %{_libdir}/graphviz
%{_libdir}/*.*.dylib
%{_libdir}/graphviz/*.*.dylib
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*
%{_datadir}/graphviz

%files devel
%defattr(-,root,wheel)
%{_includedir}/graphviz
%{_libdir}/*.dylib
%{_libdir}/graphviz/*.dylib
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

%files doc
%defattr(-,root,wheel)
%doc __doc/*

%changelog
* Tue Dec 21 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 
- initial build for Mac OS X WorkShop 10.6

