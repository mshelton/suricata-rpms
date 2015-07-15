#!/bin/sh

# Install packages
sudo yum -y install rpm-build libnfnetlink-devel libyaml-devel libnetfilter_queue-devel libnet-devel zlib-devel libpcap-devel pcre-devel libcap-ng-devel nspr-devel nss-devel nss-softokn-devel file-devel jansson-devel GeoIP-devel python2-devel lua-devel autoconf automake libtool gcc gcc-c++ lua-devel 

# Copy all of the RPM files to the appropriate directory.
if [ ! -e "${HOME}/rpmbuild/SOURCES" ]; then
    mkdir -p ${HOME}/rpmbuild/SOURCES
fi
cp suricata/* ${HOME}/rpmbuild/SOURCES/
cp pulledpork/* ${HOME}/rpmbuild/SOURCES/

# Download the Suricata source code
wget http://www.openinfosecfoundation.org/download/suricata-2.0.8.tar.gz
mv suricata-2.0.8.tar.gz ${HOME}/rpmbuild/SOURCES/

# Download the Pulled Pork source code
wget https://pulledpork.googlecode.com/files/pulledpork-0.7.0.tar.gz
mv pulledpork-0.7.0.tar.gz ${HOME}/rpmbuild/SOURCES/

# Build the RPMs
rpmbuild -bb suricata/suricata.spec
rpmbuild -bb pulledpork/pulledpork.spec


