Name:       python-sphinx
Version:    1.1.2
Release:    1%{?_dist_release}
Summary:    Python documentation generator

Group:      Development/Tools

# Unless otherwise noted, the license for code is BSD
# sphinx/util/stemmer.py Public Domain
# sphinx/pycode/pgen2 Python
# jquery (MIT or GPLv2)
License: BSD and Public Domain and Python and (MIT or GPLv2)
URL:        http://sphinx.pocoo.org/
Source0:    http://pypi.python.org/packages/source/S/Sphinx/Sphinx-%{version}.tar.gz
#
Patch1: sphinx-ptex.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
%if "%{?_dist_release}" == "osx10.6"
Requires: python > 2.6.1
BuildRequires: python-devel > 2.6.1
%else
Requires: python >= 2.4
BuildRequires: python-devel >= 2.4
%endif
BuildRequires: python-setuptools
BuildRequires: python-docutils
BuildRequires: python-jinja2
BuildRequires: python-nose
Requires:      python-docutils
Requires:      python-jinja2
Requires:      python-pygments
Requires:      python-setuptools
BuildRequires:  texlive-collection-basic, dvipng
BuildRequires:  texlive-collection-latexextra
Requires:  texlive-collection-basic, dvipng
Requires:  texlive-collection-latexextra

%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

Sphinx uses reStructuredText as its markup language, and many of its
strengths come from the power and straightforwardness of
reStructuredText and its parsing and translating suite, the Docutils.

Although it is still under constant development, the following
features are already present, work fine and can be seen "in action" in
the Python docs:

    * Output formats: HTML (including Windows HTML Help) and LaTeX,
      for printable PDF versions
    * Extensive cross-references: semantic markup and automatic links
      for functions, classes, glossary terms and similar pieces of
      information
    * Hierarchical structure: easy definition of a document tree, with
      automatic links to siblings, parents and children
    * Automatic indices: general index as well as a module index
    * Code handling: automatic highlighting using the Pygments highlighter
    * Various extensions are available, e.g. for automatic testing of
      snippets and inclusion of appropriately formatted docstrings.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    BSD
Requires:   %{name} = %{version}-%{release}


%description doc
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

This package contains documentation in reST and HTML formats.

%prep
%setup -q -n Sphinx-%{version}
#%patch1 -p1
sed -i.tmp '1d' sphinx/pycode/pgen2/token.py
rm -f sphinx/pycode/pgen2/token.py.tmp

%build
python setup.py build

pushd doc
make html
rm -rf _build/html/.buildinfo
mv _build/html ..
make latexpdf
mv _build/latex/sphinx.pdf ..
make man
mv _build/man ..
rm -rf _*
popd

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --skip-build --root=$RPM_BUILD_ROOT --install-scripts=%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Deliver rst files
mv doc reST

%clean
rm -rf $RPM_BUILD_ROOT

%check
make test

%files
%defattr(-,root,wheel)
%doc AUTHORS CHANGES EXAMPLES LICENSE README TODO
%{_bindir}/sphinx-*
%{python_sitelib}/*
%{_mandir}/man1/*

%files doc
%defattr(-,root,wheel)
%doc html reST sphinx.pdf

%changelog
* Tue Nov 22 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.1.2-1
- improve pLaTeX support

* Sat Nov 05 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.1.2-0
- update to 1.1.2

* Wed Aug 31 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.7-3
- mofify python requirements for OSXWS

* Mon Aug 22 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.7-2
- switchover from tetex to texlive

* Thu Jun 30 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.7-1
- make more compatible with Vine Linux

* Fri Apr  1 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.7-0
- update to 1.0.7
- replace setuptools with distribute

* Fri Jan  7 2011 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.6-0
- update to 1.0.6

* Tue Dec 21 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.5-0
- update to 1.0.5
- added Japanese LaTeX support
- added Japanese documents

* Tue Nov  9 2010 Akihiro Uchida <uchida@ike-dyn.ritsumei.ac.jp> 1.0.4-0
- initial build for Mac OS X WorkShop 10.6
