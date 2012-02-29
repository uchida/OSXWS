Name:           graphviz
Summary:        Graph Visualization Tools
Version:        2.28.0
Release:        0%{?_dist_release}
Group:          Applications/Graphics
License:        CPL
URL:            http://www.graphviz.org/

Source:         http://www.graphviz.org/pub/%{name}/stable/SOURCES/%{name}-%{version}.tar.gz
Patch0: graphviz-ptrdiff.patch
Patch2: graphviz-2.28.0-gvc.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires:  bison
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gd-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel 
BuildRequires:  zlib-devel
BuildRequires:  ghostscript-devel
BuildRequires:  pkgconfig
Requires:	urw-fonts

# only for this release
BuildConflicts: graphviz-devel

%description
A collection of tools and tcl packages for the manipulation and layout
of graphs (as in nodes and edges, not as in barcharts).

%package devel
Group:          Development/Libraries
Summary:        Development tools for version %{version} of %{name}
Requires:       %{name} = %{version}

%description devel
The %{name}-devel package contains the header files
and man3 pages necessary for developing programs
using version %{version} of the %{name} libraries.

%package doc
Summary: PDF and HTML documents for graphviz
Group:	 Applications/Documentation

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%prep
%setup -q
%patch0 -p1
%patch2 -p1

%build
export CFLAGS="-I/usr/X11/include -I%{_includedir}"
export CXXFLAGS="-I/usr/X11/include -I%{_includedir}"
export LDFLAGS="-L/usr/X11/lib -L%{_libdir}"
%configure \
    --without-x \
    --disable-static \
    --with-libgd \
    --with-ipsepcola \
    --with-pangocairo \
    --without-gtk \
    --without-gdk-pixbuf \
    --without-gtkgl \
    --without-gtkglext \
    --without-mylibgd \
    --without-ming \
    --without-lasi \
    --disable-sharp \
    --disable-guile \
    --disable-io \
    --disable-java \
    --disable-lua \
    --disable-ocaml \
    --disable-perl \
    --disable-php \
    --disable-python \
    --disable-r \
    --disable-ruby \
    --disable-tcl \
    --without-qt \
    --with-quartz \
    --with-ghostscript
sed -i.tag 's|LTOBJCCOMPILE = $(LIBTOOL)|LTOBJCCOMPILE = $(LIBTOOL) --tag=CC|g' plugin/quartz/Makefile
make

%install
rm -rf $RPM_BUILD_ROOT __doc
make DESTDIR=$RPM_BUILD_ROOT \
     docdir=$RPM_BUILD_ROOT%{_docdir}/%{name} \
     pkgconfigdir=%{_libdir}/pkgconfig \
     install

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
chmod -x $RPM_BUILD_ROOT%{_datadir}/%{name}/lefty/*
cp -a $RPM_BUILD_ROOT%{_datadir}/%{name}/doc __doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/doc

%clean
rm -rf $RPM_BUILD_ROOT

# run "dot -c" to generate plugin config in %{_libdir}/%{name}/config
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
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lefty
%{_mandir}/man1/*
%{_mandir}/man7/*
%dir %{_libdir}/%{name}
%{_libdir}/*.*.dylib
%{_libdir}/%{name}/*.*.dylib

%files devel
%defattr(-,root,wheel)
%{_includedir}/%{name}
%{_libdir}/*.dylib
%{_libdir}/%{name}/*.dylib
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{name}/graphs
%{_mandir}/man3/*.3.gz

%files doc
%defattr(-,root,wheel)
%doc __doc/*

%changelog
* Wed Feb 29 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.28.0-0
- update to 2.28.0

* Sat Feb 18 2012 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.26.3-2
- build x86_64 mono arch

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.26.3-1
- make more compatible with Vine Linux

* Tue Dec 21 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.26.3-0
- initial build for Mac OS X WorkShop 10.6

