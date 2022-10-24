%global with_selinux 1
%global modulename mumble_server
%global selinuxtype targeted

Name:       mumble-server-selinux
Version:	1.0
Release:	3%{?dist}
Summary:	SELinux policy module for mumble-server

Group:	    System Environment/Base		
License:	GPLv2+	
Source0:    %{modulename}.te
Source1:	%{modulename}.if
Source2:    %{modulename}.fc
Source3:    LICENSE

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
BuildArch:      noarch
%{?selinux_requires}
%description
SELinux policy module for mumble-server.

%build
%if 0%{?with_selinux}
mkdir -p selinux
cp -p %{SOURCE0} selinux/
cp -p %{SOURCE1} selinux/
cp -p %{SOURCE2} selinux/
cp -p %{SOURCE3} selinux/

make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 -f %{modulename}.pp
%endif

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
install -D -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
install -D -p -m 0644 selinux/%{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%check

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

if [ "$1" -le "1" ]; then
   %systemd_postun_with_restart murmur.service
fi

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi

%files
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}
%license selinux/LICENSE
