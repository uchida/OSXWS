Summary: a terminal multiplexer
Summary(ja): 端末多重化ユーティリティ
Name: tmux
Version: 1.4
Release: 1%{?_dist_release}
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# based on zsh patch http://www.zsh.org/mla/workers/2009/msg01145.html
Source1: tmux_zshcomp
Patch0: tmux-osxws.patch
License: BSD
Group: Applications/System
URL: http://tmux.sourceforge.net/

BuildRequires: ncurses-devel, libevent-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: fat

%description
tmux is a terminal multiplexer: it enables a number of terminals (or windows), each running a separate program, to be created, accessed, and controlled from a single screen.
tmux may be detached from a screen and continue running in the background, then later reattached.

%prep
%setup -q
%patch0 -p1

%build
export CFLAGS="-arch i386 -arch x86_64"
export CPPFLAGS="-I%{_includedir}"
export LDFLAGS="-L%{_libdir} -arch i386 -arch x86_64"
%configure \
    CC='/usr/bin/gcc-4.2 -arch i386 -arch x86_64' CPP="/usr/bin/gcc-4.2 -E"
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} MANDIR=%{_mandir}

# examples
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -rf examples $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

# zsh completion
zsh_completion_dir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
mkdir -p $zsh_completion_dir
install -m 644 %{SOURCE1} $zsh_completion_dir/_tmux

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}-%{version}/examples
%{_datadir}/zsh/site-functions/_tmux
%doc CHANGES FAQ NOTES TODO

%changelog
* Thu May 19 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.4-1
- rebuild with libevent 2.0.10

* Wed Jan  5 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.4-0
- update to tmux 1.4

* Mon Nov  8 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3-0
- initial build for Mac OS X WorkShop

