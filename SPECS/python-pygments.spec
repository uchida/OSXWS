%define __python /usr/osxws/bin/python
%define modulename pygments

Summary: Pygments is a syntax highlighting package written in Python.
Summary(ja): Python で書かれた構文ハイライト用パッケージ
Name: python-%{modulename}
Version: 1.3.1
Release: 1%{?_dist_release}
Source0: http://pypi.python.org/packages/source/P/Pygments/Pygments-%{version}.tar.gz
License: BSD
Group: Development/Languages
URL: http://pygments.org/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: bash-completion
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-nose
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
It is a generic syntax highlighter for general use in all kinds of software such as forum systems, 
wikis or other applications that need to prettify source code. Highlights are:
- a wide range of common languages and markup formats is supported
- special attention is paid to details, increasing quality by a fair amount
- support for new languages and formats are added easily
- a number of output formats, presently HTML, LaTeX, RTF, SVG, all image formats that PIL supports and ANSI sequences
- it is usable as a command-line tool and as a library
- .. and it highlights even Brainfuck!

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
%setup -q -n %{modulename}-%{version}

%build
python setup.py build
make test

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install docs/pygmentize.1 $RPM_BUILD_ROOT%{_mandir}/man1/
mv docs/build docs/html

# bash-completion
bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 external/pygments.bashcomp $bash_completion_dir/pygments

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%{_bindir}/*
%{_mandir}/man1/pygmentize.1*
%{python_sitelib}/*
%{_sysconfdir}/bash_completion.d/pygments
%doc external/*.py
%doc AUTHORS CHANGES LICENSE TODO
%doc docs/html

%changelog
* Sat Apr 23 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3.1-1
- add bash_completion support for pygmentize command
- add *.py in external to documents

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.3.1-0
- initial build for Mac OS X WorkShop 10.6

