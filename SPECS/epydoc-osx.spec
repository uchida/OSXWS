Summary: Automatic API documentation generation tool for Python
Summary(ja): Python 用の自動 API ドキュメント生成ツール
Name: epydoc
Version: 3.0.1
Release: 3%{?_dist_release}
Group: Development/Tools
License: MIT
URL: http://epydoc.sourceforge.net/
Source0: http://pypi.python.org/packages/source/e/%{name}/%{name}-%{version}.tar.gz
Patch1: epydoc-3.0.1-giftopng.patch
Patch2: epydoc-3.0.1-new-docutils.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel
Provides: python-epydoc
BuildArch: noarch

%description
Epydoc is a tool for generating API documentation for Python modules,
based on their docstrings.  For an example of epydoc's output, see the
API documentation for epydoc itself (html, pdf). A lightweight markup
language called epytext can be used to format docstrings, and to add
information about specific fields, such as parameters and instance
variables.  Epydoc also understands docstrings written in
ReStructuredText, Javadoc, and plaintext.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Prevent having *.pyc and *.pyo in _bindir
mv $RPM_BUILD_ROOT%{_bindir}/apirst2html.py $RPM_BUILD_ROOT%{_bindir}/apirst2html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%doc LICENSE.txt README.txt doc/
%{_bindir}/apirst2html
%{_bindir}/epydoc
%{_bindir}/epydocgui
%{python_sitelib}/epydoc/
%{python_sitelib}/epydoc-*.egg-info
%{_mandir}/man1/*.1*


%changelog
* Wed Jun 29 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.0.1-3
- make more compatible with Vine Linux

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.0.1-2
- import patches from Fedora 15

* Sun Apr 24 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.0.1-1
- fix type in Group

* Wed Dec 22 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 3.0.1-0
- initial build for Mac OS X WorkShop 10.6

