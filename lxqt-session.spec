%define git 0

Name: lxqt-session
Version: 2.0.0
%if %git
Release: 0.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 6
Source0: https://github.com/lxqt/lxqt-session/releases/download/%{version}/lxqt-session-%{version}.tar.xz
%endif
Summary: Session manager for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
Patch0: lxqt-session-0.12.0-omv-settings.patch
Patch1: lxqt-session-0.12.0-startlxqt-omv-user-settings.patch
Patch2: lxqt-session-0.8.0-fix-path-to-openbox.patch
Patch3:	lxqt-session-config.patch
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: cmake(qt6xdg) >= 3.9.1
BuildRequires: cmake(qtxdg-tools) >= 4.0.0
BuildRequires: cmake(lxqt)
BuildRequires: cmake(lxqt2-build-tools)
BuildRequires: cmake(LayerShellQt)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libproc2)
BuildRequires: xdg-user-dirs
Requires: xdg-utils
Requires: qtxdg-tools
Requires: xdg-user-dirs
# dbus-launch is used by startlxqt
Requires: dbus-x11
# lxqt-session uses dbus-update-activiation-environment
Requires: dbus-tools
# workaround for missing icons in desktop files on lxqt desktop
Requires: sed
Requires: plasma6-breeze
Requires: kf6-breeze-icons
%rename razorqt-session
%rename lxqt-common

%description
Session manager for the LXQt desktop.

%prep
%if %git
%setup -qn %{name}-%{git}
%else
%setup -q
%endif
%autopatch -p1

find lxqt-leave -name "*.desktop.in" |xargs sed -i -e "s,^Categories=.*,&;,"
find lxqt-leave -name "*.desktop.in" |xargs sed -i -e "s,^OnlyShowIn=.*,&;,;s,;;,;,g"

%cmake -DPULL_TRANSLATIONS=NO -DBUNDLE_XDG_UTILS=NO -G Ninja

%build
# Need to be in a UTF-8 locale so grep (used by the desktop file
# translation generator) doesn't scream about translations containing
# "binary" (non-ascii) characters
export LANG=en_US.utf-8
export LC_ALL=en_US.utf-8
%ninja -C build

%install
# Need to be in a UTF-8 locale so grep (used by the desktop file
# translation generator) doesn't scream about translations containing
# "binary" (non-ascii) characters
export LANG=en_US.utf-8
export LC_ALL=en_US.utf-8
%ninja_install -C build

# (tpg) we do not have any KDM in 2015.0 or newer
rm -rf %{buildroot}%{_datadir}/kdm/sessions/lxqt.desktop

# We get the configs from distro-release
rm %{buildroot}%{_datadir}/lxqt/{lxqt,session}.conf

%find_lang %{name} --with-qt --all-name

%files -f %{name}.lang
%{_bindir}/startlxqt
%{_bindir}/lxqt-session
%{_bindir}/lxqt-leave
%{_bindir}/lxqt-config-session
%{_datadir}/applications/lxqt-*.desktop
# This is a list of all supported window managers - let's
# not move that to distro-release, no customization necessary
%{_datadir}/lxqt/windowmanagers.conf
%doc %{_mandir}/man1/*
%{_datadir}/xsessions/lxqt.desktop
%{_sysconfdir}/xdg/autostart/*
%dir %{_datadir}/lxqt/translations/*
