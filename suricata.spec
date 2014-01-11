
Summary: Intrusion Detection System
Name: suricata
Version: 1.4.7
Release: 2%{?dist}
License: GPLv2
Group: Applications/Internet
URL: http://www.openinfosecfoundation.org
Source0: http://www.openinfosecfoundation.org/download/%{name}-%{version}.tar.gz
Source1: suricata.service
Source2: suricata.sysconfig
Source3: suricata.logrotate
Source4: fedora.notes
Source5: suricata-tmpfiles.conf
Patch1:  suricata-1.1.1-flags.patch
Patch2: suricata-1.4.1-stack-protector-strong.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libyaml-devel 
BuildRequires: libnfnetlink-devel libnetfilter_queue-devel libnet-devel
BuildRequires: zlib-devel libpcap-devel pcre-devel libcap-ng-devel
BuildRequires: file-devel nspr-devel nss-devel nss-softokn-devel
BuildRequires: jansson-devel GeoIP-devel python-devel luajit-devel
BuildRequires: systemd
# Remove when rpath issues are fixed
BuildRequires: autoconf automake libtool
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
The Suricata Engine is an Open Source Next Generation Intrusion
Detection and Prevention Engine. This engine is not intended to
just replace or emulate the existing tools in the industry, but
will bring new ideas and technologies to the field. This new Engine
supports Multi-threading, Automatic Protocol Detection (IP, TCP,
UDP, ICMP, HTTP, TLS, FTP and SMB! ), Gzip Decompression, Fast IP
Matching, and GeoIP identification.

%prep
%setup -q
install -m 644 %{SOURCE4} doc/
%patch1 -p1
%patch2 -p1
# This is to fix rpaths created by bad Makefile.in
autoreconf -fv --install

%build
%configure --enable-gccprotect --disable-gccmarch-native --enable-nfqueue --enable-af-packet --with-libnspr-includes=/usr/include/nspr4 --with-libnss-includes=/usr/include/nss3 --enable-jansson --enable-geoip --enable-luajit
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="${RPM_BUILD_ROOT}" "bindir=%{_sbindir}" install

# Setup etc directory
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/suricata/rules
install -m 600 suricata.yaml $RPM_BUILD_ROOT%{_sysconfdir}/suricata
install -m 600 classification.config $RPM_BUILD_ROOT%{_sysconfdir}/suricata
install -m 600 reference.config $RPM_BUILD_ROOT%{_sysconfdir}/suricata
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/suricata
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/suricata

# Make logging directory
mkdir -p $RPM_BUILD_ROOT/%{_var}/log/suricata

# Remove a couple things so they don't get picked up
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libhtp.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libhtp.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libhtp.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig

# Setup tmpdirs
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf
mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
%systemd_post suricata.service

%preun
%systemd_preun suricata.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart suricata.service

%files
%defattr(-,root,root,-)
%doc COPYING doc/INSTALL doc/Basic_Setup.txt
%doc doc/Setting_up_IPSinline_for_Linux.txt doc/fedora.notes
%{_sbindir}/suricata
%{_bindir}/suricatasc
%{_libdir}/libhtp-*
%{python_sitelib}/suricatasc*.egg-info
%{python_sitelib}/suricatasc/*
%attr(750,root,root) %dir %{_var}/log/suricata
%config(noreplace) %{_sysconfdir}/suricata/suricata.yaml
%config(noreplace) %{_sysconfdir}/suricata/classification.config
%config(noreplace) %{_sysconfdir}/suricata/reference.config
%dir %attr(750,root,root) %{_sysconfdir}/suricata
%dir %attr(750,root,root) %{_sysconfdir}/suricata/rules
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/suricata
%attr(644,root,root) %{_unitdir}/suricata.service
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/suricata
%dir /run/%{name}/
%{_tmpfilesdir}/%{name}.conf

%changelog
* Sat Jan 11 2014 Steve Grubb <sgrubb@redhat.com> 1.4.7-2
- Enable luajit support

* Wed Dec 18 2013 Steve Grubb <sgrubb@redhat.com> 1.4.7-1
- New upstream bug fix release

* Fri Oct 04 2013 Steve Grubb <sgrubb@redhat.com> 1.4.6-1
- New upstream bug fix release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Steve Grubb <sgrubb@redhat.com> 1.4.3-2
- Drop prelude support

* Fri Jun 21 2013 Steve Grubb <sgrubb@redhat.com> 1.4.3-1
- New upstream bug fix release

* Mon Jun 03 2013 Steve Grubb <sgrubb@redhat.com> 1.4.2-1
- New upstream bug fix release

* Sun Mar 10 2013 Steve Grubb <sgrubb@redhat.com> 1.4.1-1
- New upstream bugfix release
- Enable libgeoip support
- Switch to stack-protector-all

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Steve Grubb <sgrubb@redhat.com> 1.4-1
- New upstream feature enhancement release

* Thu Dec 06 2012 Steve Grubb <sgrubb@redhat.com> 1.3.5-1
- New upstream bugfix release

* Tue Nov 27 2012 Steve Grubb <sgrubb@redhat.com> 1.3.4-1
- New upstream release

* Mon Nov 05 2012 Steve Grubb <sgrubb@redhat.com> 1.3.3-1
- New upstream release

* Tue Oct 09 2012 Steve Grubb <sgrubb@redhat.com> 1.3.2-2
- Add nss-devel build require and systemd macros

* Mon Oct 08 2012 Steve Grubb <sgrubb@redhat.com> 1.3.2-1
- New upstream release

* Sat Aug 25 2012 Steve Grubb <sgrubb@redhat.com> 1.3.1-1
- New upstream release
- Switch startup to use systemd

* Fri Jul 06 2012 Steve Grubb <sgrubb@redhat.com> 1.3-1
- New upstream release

* Fri Mar 30 2012 Jon Ciesla <limburgher@gmail.com> - 1.2.1-3
- Rebuild for updated libnet.

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.2.1-2
- Rebuild against PCRE 8.30

* Thu Feb 02 2012 Steve Grubb <sgrubb@redhat.com> 1.2.1-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Steve Grubb <sgrubb@redhat.com> 1.1.1-2
- Enable AF_PACKET support

* Wed Dec 07 2011 Steve Grubb <sgrubb@redhat.com> 1.1.1-1
- New upstream release

* Mon Jul 25 2011 Steve Grubb <sgrubb@redhat.com> 1.0.5-1
- New upstream release

* Fri Jun 24 2011 Steve Grubb <sgrubb@redhat.com> 1.0.4-1
- New upstream release

* Thu Apr 28 2011 Dan Horák <dan[at]danny.cz> 1.0.3-2
- don't override -march set by the buildsystem (fixes build on non-x86)

* Sat Apr 23 2011 Steve Grubb <sgrubb@redhat.com> 1.0.3-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Steve Grubb <sgrubb@redhat.com> 1.0.2-1
- New upstream release (#651978)

* Thu Jul 01 2010 Steve Grubb <sgrubb@redhat.com> 1.0.0-1
- New upstream release

* Fri May 07 2010 Steve Grubb <sgrubb@redhat.com> 0.9.0-1
- New upstream release

* Tue Apr 20 2010 Steve Grubb <sgrubb@redhat.com> 0.8.2-1
- New upstream release

* Sat Feb 27 2010 Steve Grubb <sgrubb@redhat.com> 0.8.1-1
- Initial packaging

