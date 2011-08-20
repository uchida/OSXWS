Summary:	A version control system
Summary(ja):	GNU Arch バージョンコントロールシステム
Name:		tla
Version:	1.3.5
Release:        0%{?_dist_release}
License:	GPLv2+
Group:		Development/Tools
URL:		http://www.gnu.org/software/gnu-arch/
Source0:	ftp://ftp.gnu.org/gnu/gnu-arch/%{name}-%{version}.tar.gz
Source1:	%{name}-generate-manpage.pl
Source2:	%{name}-gpg-check.1

Patch1:		%{name}-%{version}-neon.patch
Patch2:		%{name}-%{version}-neon-327111.patch
Patch3:		%{name}-%{version}-posix.patch
Patch4:		%{name}-%{version}-remove-invariant.patch
Patch5:		%{name}-%{version}-segfault-ia64.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: fat

Requires:	diffutils
Requires:	patch
Requires:	tar

BuildRequires:	neon-devel

%description
GNU Arch 1 (also known as tla) is a revision control system, similar in
purpose to tools such as CVS, SCCS, and Subversion. It is used to keep track
of the changes made to a source tree and to help programmers combine and
otherwise manipulate changes made by multiple people or at different times.

TLA is a punning acronym that stands for either "true love, always" and "three
letter acronym".

%prep
%setup -q -c %{name}-%{version}
pushd %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
# Build against neon-devel.
rm -rf ./src/libneon
# Suppress rpmlint error.
iconv -f ISO8859-1 -t UTF-8 ./src/tla/AUTHORS \
  > AUTHORS.utf-8 && mv AUTHORS.utf-8 ./src/tla/AUTHORS
iconv -f ISO8859-1 -t UTF-8 ./src/tla/README \
  > README.utf-8 && mv README.utf-8 ./src/tla/README
popd

mv %{name}-%{version} INTEL
cp -Rp  INTEL X86_64


%build
export CC="/usr/bin/gcc"
export LDFLAGS="-L%{_libdir} -lssl -lcrypto -lz -Wl,-search_paths_first -lgssapi_krb5 -lkrb5 -lk5crypto -lcom_err -lresolv -lexpat"
pushd INTEL
  export CFLAGS="-O3 -arch i386 -mtune=pentium-m"
  mkdir build
  pushd build
    ../src/configure --prefix=%{_prefix} --with-cc="/usr/bin/gcc"
    # Parallel make does not work.
    make CFLAGS="$CFLAGS $(neon-config --cflags) -I%{_includedir}"
  popd
  # man page
  mkdir -p ./debian/tmp
  PATH="`pwd`/build/tla/tla:$PATH" perl %{SOURCE1} tla.1
  cp -fRP src/tla/README src/tla/AUTHORS ..
popd

pushd X86_64
  export CFLAGS="-O3 -arch x86_64 -mtune=core2"
  mkdir build
  pushd build
    ../src/configure --prefix=%{_prefix} --with-cc="/usr/bin/gcc"
    # Parallel make does not work.
    make CFLAGS="$CFLAGS $(neon-config --cflags) -I%{_includedir}"
  popd
popd


%install
rm -rf $RPM_BUILD_ROOT

PWD=`pwd`
for arch in INTEL X86_64; do
  pushd $arch
    rm -rf ${PWD}-root
    # Makefiles use destdir instead of DESTDIR.
    make -C build install destdir=${PWD}-root
  popd
done

## Make Universal Binaries
filelist=$(find ./INTEL-root -type f | xargs file | sed -e 's,^\./INTEL-root/,,g' | \
        grep -E \(Mach-O\)\|\(ar\ archive\) |sed -e 's,:.*,,g' -e '/\for\ architecture/d')
for i in $filelist; do
    /usr/bin/lipo -create INTEL-root/$i X86_64-root/$i -output `basename $i`
    cp -f `basename $i` INTEL-root/$i
done

install -m755 INTEL/build/links/{make,remove}-links INTEL-root/%{_bindir}
# install
mkdir -p $RPM_BUILD_ROOT
tar cf - -C INTEL-root . | tar xpf - -C $RPM_BUILD_ROOT

# remove extraneous
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

# man page
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
pushd INTEL
  install -p -m644 ./debian/tmp/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1
  install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1
popd

cp -rf INTEL/src/docs-tla docs-tla
find docs-tla -type f \! -name "*.css" -a \! -name "*.html" | xargs rm -f


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc docs-tla
%doc AUTHORS
%doc README
%{_bindir}/make-links
%{_bindir}/%{name}
%{_bindir}/remove-links
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/%{name}-gpg-check.1.gz

%changelog
* Sun Jul  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3.5-0
- initial build for Mac OS X WorkShop

