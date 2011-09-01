%define srcname docutils
%define elisppkgname rst-el
%define prereq_ge()  %(LC_ALL="C" rpm -q --queryformat 'Requires(post,preun):%%{NAME} >= %%{VERSION}' %1| grep -v "is not")
%define emacsen_pkgdir %{_libdir}/emacsen-common/packages

Summary: an open-source text processing system written in Python
Summary(ja): Pythonで書かれたテキスト処理システム
Name: python-%{srcname}
Version: 0.7
Release: 4%{?_dist_release}
Group: Development/Languages
License: Public Domain and MIT and Python and GPLv2
URL: http://docutils.sourceforge.net/
Source0: http://prdownloads.sourceforge.net/%{srcname}/%{srcname}-%{version}.tar.gz
## for rst-mode
Source1: %{elisppkgname}-install.sh
Source2: %{elisppkgname}-remove.sh
Source3: osxws-default-%{elisppkgname}.el
Source4: %{elisppkgname}-init.el

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python
BuildRequires: python-devel
%endif
BuildRequires: python-setuptools
BuildRequires: python-imaging
Requires: python-imaging

Provides: docutils = %{version}-%{release}
Obsoletes: docutils <= 0.5

%description
Docutils is an open-source text processing system for processing 
plaintext documentation into useful formats, such as HTML or LaTeX.
It includes reStructuredText, the easy to read, easy to use,
what-you-see-is-what-you-get plaintext markup language.

%description -l ja
Docutilsはオープンソースのテキスト処理システムで、プレーンテキストの
文書をHTMLやLaTeXなどの使いやすいフォーマットに変換するものです。
読みやすく使いやすくWYSIWYGなプレーンテキストのマークアップ言語である
reStructuresTextを含んでいます。

%package -n %{elisppkgname}
Summary: Emacs support for reStructuredText
Summary(ja): reStructuredText の Emacs サポート
Group: Applications/Editors/Emacs
Requires:     emacsen
Requires(post,preun):       emacsen
%prereq_ge    emacsen-common

%description -n %{elisppkgname}
Emacs support for reStructuredText.

%description -l ja -n %{elisppkgname}
reStructuredText の Emacs サポート

%prep
%setup -q -n %{srcname}-%{version}

# Remove a shebang from one of the library files
sed -i.tmp '1D' docutils/readers/python/pynodes.py
rm -f docutils/readers/python/pynodes.py.tmp

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=${RPM_BUILD_ROOT} --install-scripts=%{_bindir}

for file in $RPM_BUILD_ROOT%{_bindir}/*.py; do
    mv $file `dirname $file`/`basename $file .py`
done

# We want the licenses but don't need this build file
rm -f licenses/docutils.conf

# docutils only installs this if its not already on the system.  Due to the
# possibility that a previous version of docutils may be installed, we install
# it manually here.
install -m644 extras/roman.py ${RPM_BUILD_ROOT}/%{python_sitelib}/roman.py

## for Emacs package
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/%{elisppkgname}/packages
mkdir -p %{buildroot}%{emacsen_pkgdir}/install
mkdir -p %{buildroot}%{emacsen_pkgdir}/remove

#
# install el files
#
mv tools/editors/emacs/rst.el %{buildroot}%{_datadir}/emacs/site-lisp/%{elisppkgname}
cp -p %{SOURCE3} %{SOURCE4} %{buildroot}%{_datadir}/emacs/site-lisp/%{elisppkgname}

#
# install script (bytecompile el and install elc , remove)
#
%_installemacsenscript %{elisppkgname} %{SOURCE1}

%_removeemacsenscript  %{elisppkgname} %{SOURCE2}



%clean
rm -rf $RPM_BUILD_ROOT


%post -n %{elisppkgname}
#
# bytecompile and install
#
if [ "$1" = 2 ]; then

%_emacsenPackageRemove %{elisppkgname}

fi

%_addemacsenlist %{elisppkgname}

%_emacsenPackageInstall %{elisppkgname}


%preun -n %{elisppkgname}
if [ "$1" = 0 ]; then

%_emacsenPackageRemove %{elisppkgname}

%_removeemacsenlist %{elisppkgname}

fi



%files
%defattr(-,root,root)
%doc BUGS.txt HISTORY.txt RELEASE-NOTES.txt docs COPYING.txt THANKS.txt FAQ.txt README.txt
%doc licenses docs
%{_bindir}/*
%{python_sitelib}/%{srcname}/
%{python_sitelib}/roman.*
%{python_sitelib}/docutils-*.egg-info

%files -n %{elisppkgname}
%defattr(-,root,root)
%doc BUGS.txt HISTORY.txt RELEASE-NOTES.txt COPYING.txt THANKS.txt FAQ.txt README.txt
%doc licenses tools/editors
%{_datadir}/emacs/site-lisp/%{elisppkgname}
%{emacsen_pkgdir}/install/%{elisppkgname}
%{emacsen_pkgdir}/remove/%{elisppkgname}


%changelog
* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7-4
- mofify python requirements for OSXWS

* Sun Jul  3 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7-3
- fix path in rst-el-{install,remove}.sh

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7-2
- make more compatible with Vine Linux

* Mon Dec 20 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7-1
- fix requires python-imaging

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 0.7-0
- initial build for Mac OS X WorkShop

