%define realname pulledpork

Summary:	A Snort Rule Management Tool
Name:		pulledpork
Version:	0.7.0
Release:	1%{?dist}
License:	GPLv2	
URL:		https://code.google.com/p/pulledpork/
Source0:	https://pulledpork.googlecode.com/files/%{realname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{realname}-%{version}-%{release}-root

Requires:	perl-libwww-perl
Requires:	perl-Crypt-SSLeay
Requires:	perl-Archive-Tar

# Don't build the -debug package.
%define debug_package %{nil}


%description
A Snort rule management tool.


%prep
%setup -q -n %{realname}-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT

%__mkdir_p -m 755 $RPM_BUILD_ROOT/opt/pulledpork/etc
%__mkdir_p -m 755 $RPM_BUILD_ROOT/etc/suricata/rules/iplists
%__mkdir_p -m 755 $RPM_BUILD_ROOT/opt/pulledpork/bin
for file in etc/*; do
    %__install -m 664 $file $RPM_BUILD_ROOT/opt/pulledpork/etc
done
%__install -m 755 pulledpork.pl $RPM_BUILD_ROOT/opt/pulledpork/bin/pulledpork

%files
%defattr(-,root,root,-)
/opt/pulledpork/bin/pulledpork
%config /opt/pulledpork/etc/*
%config /etc/suricata/rules/iplists
%doc LICENSE README doc/*


%changelog
* Wed Jul 15 2015 Matt Shelton <matthew.j.shelton@gmail.com> - 0.7.0-1
- Updated for 0.7.0 
- Changed root directory to /opt/pulledpork

* Fri Jan  4 2013 Jason Ish <ish@unx.ca> - 0.6.1-1
- First cut at a pulledpork package.

