Name:    halevt
Summary: Generic handler for HAL events
Version: 0.1.5
Release: %mkrel 4
License: GPLv2+
Group:   System/Configuration/Hardware
URL:     http://www.nongnu.org/halevt/
Source0: http://savannah.nongnu.org/download/halevt/%{name}-%{version}.tar.gz
Source1: %{name}.xml
Source2: %{name}-explore-directory
Source3: %{name}-explore-mount
Source4: %{name}.xinit
BuildRoot: %{_tmppath}/%{name}-%{version}

BuildRequires: dbus-glib-devel
BuildRequires: hal-devel
BuildRequires: libxml2-devel
BuildRequires: libboolstuff-devel >= 0.1.12
BuildRequires: gettext
BuildRequires: texinfo
BuildRequires: man

%description
Halevt (HAL events manager) is a daemon that executes arbitrary commands
when a device with certain properties is added to the system and when
device properties change. Halevt uses HAL to monitor the state of your
system's hardware. With the default config file, it can handle
the mounting of media as they are inserted/attached to the system.

Halevt comes with halevt-mount a program able to use HAL to mount, umount
devices and keep a list of devices handled by halevt-mount.

%package system
Summary: Run halevt system-wide
Group: System/Configuration/Hardware
Requires: %{name}

%description system
This package will make halevt run system-wide.

%package user
Summary: Run halevt as user
Group: System/Configuration/Hardware
Requires: %{name}

%description user
This package will make halevt run as user.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}%{_infodir}/dir

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d

install -m 0755 -p halevt-initscript %{buildroot}%{_sysconfdir}/rc.d/init.d/halevt

install -d %{buildroot}%{_sysconfdir}/%{name}
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/

install -m755 %{SOURCE2} %{SOURCE3} %{buildroot}%{_bindir}/

install -d %{buildroot}%{_sysconfdir}/X11/xinit.d
install -m755 %{SOURCE4} %{buildroot}%{_sysconfdir}/X11/xinit.d/%{name}

%find_lang %{name}
%find_lang %{name}-mount
cat %{name}-mount.lang >> %{name}.lang

%clean
rm -rf %{buildroot}

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/halevt /sbin/nologin

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name}

%post system
%_post_service %{name}

%preun system
%_preun_service service_name

%files -f %{name}.lang
%doc  AUTHORS README NEWS examples
%doc doc/*.html
%dir %{_sysconfdir}/halevt
%{_sysconfdir}/%{name}/%{name}.xml
%{_bindir}/halevt
%{_bindir}/halevt-mount
%{_bindir}/halevt-umount
%{_bindir}/halevt-explore-*
%{_bindir}/hvmount
%{_bindir}/hvumount
%{_bindir}/halevt_umount_from_tray-gtkdialog.sh
%{_bindir}/halevt_umount_from_tray-xmessage.sh
%{_bindir}/halevt_umount_report.sh
%{_infodir}/halevt.info*
%{_mandir}/man1/halevt*.1*
%{_mandir}/man1/hvm*.1*
%dir %attr(750,halevt,halevt) %{_localstatedir}/run/halevt
%dir %attr(755,halevt,halevt) %{_localstatedir}/lib/halevt

%files system
%defattr(-,root,root,-)
%{_sysconfdir}/rc.d/init.d/halevt

%files user
%defattr(-,root,root,-)
%{_sysconfdir}/X11/xinit.d/%{name}
