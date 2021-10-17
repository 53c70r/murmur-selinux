# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/sbin/murmurd; \
restorecon -R /var/lib/mumble-server; \


Name:   murmur-selinux
Version:	1.0
Release:	2%{?dist}
Summary:	SELinux policy module for murmur

Group:	System Environment/Base		
License:	GPLv2+	
URL:		https://github.com/53c70r/murmur-selinux
Source0:	murmur.pp
Source1:	murmur.if
Source2:	murmur_selinux.8
Source3:    LICENSE

Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
Requires: murmur
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for murmur.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/murmur_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/
install -m 644 %{SOURCE3} %{_builddir}/LICENSE


%post
semodule -n -i %{_datadir}/selinux/packages/murmur.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r murmur
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/murmur.pp
%{_datadir}/selinux/devel/include/contrib/murmur.if
%{_mandir}/man8/murmur_selinux.8.*
%license LICENSE

%changelog
* Wed Mar 24 2021 Silvan Nagl <mail@53c70r.de> 1.0-1
- Initial version

