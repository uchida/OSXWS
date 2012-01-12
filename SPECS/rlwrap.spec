Name:           rlwrap
Version:        0.37
Release:        2%{?dist}
Summary:        Wrapper for GNU readline

Group:          Applications/Text
License:        GPLv2+
URL:            http://utopia.knoware.nl/~hlub/rlwrap/
Source0:        http://utopia.knoware.nl/~hlub/rlwrap/rlwrap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel
#Requires:       

%description
rlwrap is a 'readline wrapper' that uses the GNU readline library to
allow the editing of keyboard input for any other command. Input
history is remembered across invocations, separately for each command;
history completion and search work as in bash and completion word
lists can be specified on the command line.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
(cd $RPM_BUILD_ROOT%{_datadir}/rlwrap/filters
# these are not scripts
chmod -x README
chmod -x RlwrapFilter.*pm
)


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/rlwrap
%{_mandir}/*/rlwrap.*
%{_mandir}/man3/RlwrapFilter.*
%{_datadir}/rlwrap



%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  1 2010 Michel Salim <salimma@fedoraproject.org> - 0.37-1
- Update to 0.37

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.30-2
- Autorebuild for GCC 4.3

* Thu Jan 10 2008 Michel Salim <michel.sylvan@gmail.com> 0.30-1
- Update to 0.30

* Thu Sep 20 2007 Michel Salim <michel.sylvan@gmail.com> 0.28-3
- License field updated

* Mon Feb  5 2007 Michel Salim <michel.salim@gmail.com> 0.28-2
- Rebuild for Fedora 7, removing dependency on libtermcap

* Tue Nov 28 2006 Michel Salim <michel.salim@gmail.com> 0.28-1
- Initial package
