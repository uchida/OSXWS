%define exec_texhash [ -x %{_prefix}/bin/texhash ] && /usr/bin/env - %{_prefix}/bin/texhash 2> /dev/null
%define texmf %{_prefix}/share/texmf
%define build_texmf $RPM_BUILD_ROOT%{texmf}

%define srcname expdlist

Summary: teTeX macro packages of expanded description environments.
Name: texmacro-%{srcname}
Version: 2.4
Release: 0%{?_dist_release}
BuildArch: noarch
Source0: http://mirror.ctan.org/macros/latex/contrib/expdlist.zip
URL: http://www.ctan.org/tex-archive/macros/latex/contrib/expdlist/
License: LPPL
Group: Applications/Publishing
BuildRequires: tetex dvipdfmx
Requires: tetex
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
The expanded description environment will not replace the LaTeX
description environment, but on request you will have some additional
features. It supports an easy possibility of changing the left margin.
Also there is with \listpart a new command available which is valid in
all list environments. It gives the possibility to break a list for a
comment without touching any counters.

%prep
%setup -q -n %{srcname}

%build
latex %{srcname}.ins

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{build_texmf}/tex/latex/%{srcname}
mv %{srcname}.sty %{build_texmf}/tex/latex/%{srcname}

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
%doc *.{pdf,txt}

%changelog 
* Thu Nov  4 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 2.4-0
- first release

