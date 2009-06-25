Name:    halevt
Summary: Generic handler for HAL events
Version: 0.1.4
Release: %mkrel 1
License: GPLv2+
Group:   System/Configuration/Hardware

URL:       http://www.environnement.ens.fr/perso/dumas/halevt.html
Source0:   http://www.environnement.ens.fr/perso/dumas/halevt-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dbus-glib-devel
BuildRequires: hal-devel
BuildRequires: libxml2-devel
BuildRequires: libboolstuff-devel >= 0.1.12
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: %{_bindir}/makeinfo
BuildRequires: %{_bindir}/man2html

Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(post):  info
Requires(preun): info
Requires(pre):   shadow-utils

%description
Halevt (HAL events manager) is a daemon that executes arbitrary commands
when a device with certain properties is added to the system and when
device properties change. Halevt uses HAL to monitor the state of your
system's hardware. With the default config file, it can handle
the mounting of media as they are inserted/attached to the system.

Halevt comes with halevt-mount a program able to use HAL to mount, umount
devices and keep a list of devices handled by halevt-mount.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

install -m 0755 -p halevt-initscript $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/halevt

%find_lang %{name}
%find_lang %{name}-mount
cat %{name}-mount.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group halevt >/dev/null || groupadd -r halevt
getent passwd halevt >/dev/null || \
useradd -r -g halevt -d %{_localstatedir}/lib/halevt -s /sbin/nologin \
    -c "Halevt system user" halevt
exit 0

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add halevt
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
        /sbin/service halevt stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del halevt

        /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS README NEWS halevt-hvmount.xml
%doc doc/*.html
%dir %{_sysconfdir}/halevt
%{_sysconfdir}/rc.d/init.d/halevt
%{_bindir}/halevt
%{_bindir}/halevt-mount
%{_bindir}/halevt-umount
%{_bindir}/hvmount
%{_bindir}/hvumount
%{_infodir}/halevt.info*
%dir %{_datadir}/halevt
%{_datadir}/halevt/halevt.xml
%{_mandir}/man1/halevt*.1*
%{_mandir}/man1/hvm*.1*
%dir %attr(750,halevt,halevt) %{_localstatedir}/run/halevt
%dir %attr(755,halevt,halevt) %{_localstatedir}/lib/halevt
