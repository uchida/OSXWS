%define __python /usr/osxws/bin/python
%define modulename docutils

Summary: Python Documentation Utilities
Summary(ja): Python 文書処理ツール
Name: python-%{modulename}
Version: 0.7
Release: 0%{?_dist_release}
Source0: http://downloads.sourceforge.net/%{modulename}/%{modulename}-%{version}.tar.gz
License: public domain and Freely redistributable without restriction and PSF and GPL
Group: Applications/Text
URL: http://docutils.sourceforge.net/

Requires: python = 2.6.6
Requires: /usr/osxws/bin/python2.6
Requires: python-imaging
BuildRequires: python-devel = 2.6.6
BuildRequires: /Library/Frameworks/Python.framework/Versions/2.6/include
BuildRequires: python-imaging
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

%description
Docutils is a modular system for processing documentation
into useful formats, such as HTML, XML, and LaTeX.
For input Docutils supports reStructuredText, an easy-to-read,
what-you-see-is-what-you-get plaintext markup syntax.

%description -l ja
Docutils は読みやすく使いやすい WYSIWYG な
プレーンテキストのマークアップ言語である reStructuresText を
HTML や XML、LaTeX などの便利なフォーマットに変換するための
モジュール化された文書処理システムです。

%prep
%setup -q -n %{modulename}-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=${RPM_BUILD_ROOT} --install-scripts=%{_bindir}

for file in $RPM_BUILD_ROOT%{_bindir}/*.py; do
    mv $file `dirname $file`/`basename $file .py`
done
install extras/roman.py $RPM_BUILD_ROOT%{python_sitelib}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc BUGS.txt COPYING.txt FAQ.txt HISTORY.txt README.txt RELEASE-NOTES.txt THANKS.txt
%doc docs licenses
%{_bindir}/*
%{python_sitelib}/%{modulename}
%{python_sitelib}/roman.*
%{python_sitelib}/*.egg-info

%changelog
* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7-1
- fix requires python-imaging

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7-0
- initial build for Mac OS X WorkShop

