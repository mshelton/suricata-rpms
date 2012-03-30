
Summary: Intrusion Detection System
Name: suricata
Version: 1.2.1
Release: 3%{?dist}
License: GPLv2
Group: Applications/Internet
URL: http://www.openinfosecfoundation.org
Source0: http://www.openinfosecfoundation.org/download/%{name}-%{version}.tar.gz
Source1: suricata.init
Source2: suricata.sysconfig
Source3: suricata.logrotate
Patch1:  suricata-1.1.1-flags.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libyaml-devel libprelude-devel
BuildRequires: libnfnetlink-devel libnetfilter_queue-devel libnet-devel
BuildRequires: zlib-devel libpcap-devel pcre-devel libcap-ng-devel
BuildRequires: file-devel
# Remove when rpath issues are fixed
BuildRequires: autoconf automake libtool
Requires: chkconfig

%description
The Suricata Engine is an Open Source Next Generation Intrusion
Detection and Prevention Engine. This engine is not intended to
just replace or emulate the existing tools in the industry, but
will bring new ideas and technologies to the field. This new Engine
supports Multi-threading, Automatic Protocol Detection (IP, TCP,
UDP, ICMP, HTTP, TLS, FTP and SMB! ), Gzip Decompression, Fast IP
Matching and coming soon hardware acceleration on CUDA and OpenCL
GPU cards.

%prep
%setup -q
%patch1 -p1
# This is to fix rpaths created by bad Makefile.in
autoreconf -fv --install

%build
%configure --enable-gccprotect --disable-gccmarch-native --enable-nfqueue --enable-prelude --enable-af-packet
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="${RPM_BUILD_ROOT}" "bindir=%{_sbindir}" install

# Setup etc directory
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/suricata/rules
install -m 600 suricata.yaml $RPM_BUILD_ROOT%{_sysconfdir}/suricata
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/suricata
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

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add suricata
/sbin/ldconfig

%preun
if [ $1 -eq 0 ]; then
   /sbin/service suricata stop > /dev/null 2>&1
   /sbin/chkconfig --del suricata
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING doc/INSTALL
%{_sbindir}/suricata
%{_libdir}/libhtp-*
%attr(750,root,root) %dir %{_var}/log/suricata
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/suricata/suricata.yaml
%dir %attr(750,root,root) %{_sysconfdir}/suricata
%dir %attr(750,root,root) %{_sysconfdir}/suricata/rules
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/suricata
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/suricata
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/suricata

%changelog
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

* Fri Jul 25 2011 Steve Grubb <sgrubb@redhat.com> 1.0.5-1
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

