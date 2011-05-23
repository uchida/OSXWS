Summary: the mutt of rss feed reader
Name: newsbeuter
Version: 2.4
Release: 0%{?_dist_release}
License: MIT
Group: Applications/Internet
Source: http://www.newsbeuter.org/downloads/%{name}-%{version}.tar.gz
Patch0: newsbeuter-sqlite3.patch
Patch1: newsbeuter-ncurses.patch
URL: http://www.newsbeuter.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: stfl-devel
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildArch: fat

%description
Newsbeuter is an open-source RSS/Atom feed reader for text terminals.
It runs on Linux, FreeBSD, Mac OS X and other Unix-like operating systems.
Newsbeuter's great configurability and vast number of features
make it a perfect choice for people that need a slick and fast feed reader
that can be completely controlled via keyboard.

A summary of some of its features:

- Subscribe to RSS 0.9x, 1.0, 2.0 and Atom feeds
- Download podcasts
- Freely configure your keyboard shortcuts
- Search through all downloaded articles
- Categorize and query your subscriptions with a flexible tag system
- Integrate any data source through a flexible filter and plugin system
- Automatically remove unwanted articles through a "killfile"
- Define "meta feeds" using a powerful query language
- Synchronize newsbeuter with your bloglines.com account
- Import and exporting your subscriptions with the widely used OPML format
- Freely define newsbeuter's look'n'feel through free color configurability and format strings
- Keep all your feeds in sync with Google Reader

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export CXXFLAGS='-arch i386 -arch x86_64'
export LDFLAGS='-arch i386 -arch x86_64'
make prefix=%{_prefix} \
     mandir=%{_mandir} \
     datadir=%{_datarootdir} \
     localedir=%{_localedir}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT \
     prefix=%{_prefix} \
     mandir=%{_mandir} \
     datadir=%{_datarootdir} \
     localedir=%{_localedir}
mv $RPM_BUILD_ROOT%{_datarootdir}/doc/%{name}/* doc/
mv doc/example-bookmark-plugin.sh doc/examples

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_localedir}/*
%doc AUTHORS CHANGES LICENSE README TODO
%doc doc/newsbeuter.html doc/examples doc/hackers-guide.txt

%changelog
* Wed Apr 20 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.24-0
- update to 0.24

* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.23-0
- initial build for Mac OS X WorkShop

