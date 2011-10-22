Name:           python-pygments
Version:        1.4
Release:        0%{?_dist_release}
Summary:        A syntax highlighting engine written in Python

Group:          Development/Libraries
License:        BSD
URL:            http://pygments.org/
Source0:        http://pypi.python.org/packages/source/P/Pygments/Pygments-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python >= 2.4
BuildRequires: python-devel >= 2.4
%endif
BuildRequires:  python-setuptools, python-nose
Requires:       python-setuptools, python-imaging


%description
Pygments is a generic syntax highlighter for general use in all kinds
of software such as forum systems, wikis or other applications that
need to prettify source code. Highlights are:

  * a wide range of common languages and markup formats is supported
  * special attention is paid to details that increase highlighting
    quality
  * support for new languages and formats are added easily; most
    languages use a simple regex-based lexing mechanism
  * a number of output formats is available, among them HTML, RTF,
    LaTeX and ANSI sequences
  * it is usable as a command-line tool and as a library
  * ... and it highlights even Brainf*ck!

%description -l ja
ソースコードの装飾が必要となるフォーラム、Wiki 等の全てのソフトウェアのための構文ハイライトパッケージです。
ハイライト機能は
- 広範な言語とマークアップに対応
- 細部にまでこだわった高い品質
- 新たな言語への拡張も容易
- 多彩な出力形式 HTML, LaTeX, RTF, SVG、PIL に対応する全ての画像形式、ASCII
- コマンドラインツールやライブラリとしても利用可能
- Brainfuck! にさえ対応


%prep
%setup -q -n Pygments-%{version}

%build
python setup.py build
sed -i.tmp 's/\r//' LICENSE
rm -f LICENSE.tmp

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
pushd docs
mkdir -p %{buildroot}%{_mandir}/man1
mv pygmentize.1 $RPM_BUILD_ROOT%{_mandir}/man1/pygmentize.1
mv build html
mv src reST
popd

# bash-completion
bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 external/pygments.bashcomp $bash_completion_dir/pygments

%clean
rm -rf $RPM_BUILD_ROOT


%check
make test


%files
%defattr(-,root,wheel)
%doc AUTHORS CHANGES docs/html docs/reST LICENSE TODO
%doc external/*.py
# For noarch packages: sitelib
%{python_sitelib}/*
%{_bindir}/pygmentize
%lang(en) %{_mandir}/man1/pygmentize.1.gz
%{_sysconfdir}/bash_completion.d/pygments


%changelog
* Fri Oct 21 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.4-0
- update to 1.4

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3.1-3
- mofify python requirements for OSXWS

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3.1-2
- make more compatible with Vine Linux

* Sat Apr 23 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3.1-1
- add bash_completion support for pygmentize command
- add *.py in external to documents

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3.1-0
- initial build for Mac OS X WorkShop 10.6

