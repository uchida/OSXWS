%define exec_texhash [ -x %{_prefix}/bin/texhash ] && /usr/bin/env - %{_prefix}/bin/texhash 2> /dev/null
%define texmf %{_prefix}/share/texmf
%define build_texmf $RPM_BUILD_ROOT%{texmf}

%define srcname unicode

Summary: Extended UTF-8 input encoding for LaTeX
Name: texmacro-%{srcname}
Version: 20041017
Release: 0%{?_dist_release}
BuildArch: noarch
Source0: http://mirror.ctan.org/macros/latex/contrib/unicode.zip
Source1: http://www.unicode.org/Public/UNIDATA/UnicodeData.txt
URL: http://www.ctan.org/tex-archive/macros/latex/contrib/unicode/
License: LPPL
Group: Applications/Publishing
BuildRequires: tetex
Requires: tetex
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
This package contains support for using UTF-8 as input encoding in
LaTeX documents.

%prep
%setup -q -n %{srcname}
cp -pf %{SOURCE1} .

%build
perl makeunidef.pl -t data --nocomments config/*.ucf config/*.ucf.gz

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{build_texmf}/tex/latex/%{srcname}
mv *.sty *.def data %{build_texmf}/tex/latex/%{srcname}

%post
%{exec_texhash}
exit 0

%postun
%{exec_texhash}
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{texmf}/tex/latex/%{srcname}/*
%doc FAQ INSTALL languages.pdf LICENSE README VERSION

%changelog 
* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 20041017-0
- first release

