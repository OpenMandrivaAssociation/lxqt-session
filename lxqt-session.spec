%define git 0

Name: lxqt-session
Version: 0.17.0
%if %git
Release: 1.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 1
Source0: https://github.com/lxqt/lxqt-session/releases/download/%{version}/lxqt-session-%{version}.tar.xz
%endif
Summary: Session manager for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
Patch0: lxqt-session-0.12.0-omv-settings.patch
Patch1: lxqt-session-0.12.0-startlxqt-omv-user-settings.patch
Patch2: lxqt-session-0.8.0-fix-path-to-openbox.patch
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: ninja
BuildRequires: cmake(KF5WindowSystem)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(qt5xdg)
BuildRequires: cmake(lxqt)
BuildRequires: cmake(lxqt-build-tools)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libprocps)
BuildRequires: xdg-user-dirs
Requires: xdg-utils
Requires: xdg-user-dirs
# dbus-launch is used by startlxqt
Requires: dbus-x11
# workaround for missing icons in desktop files on lxqt desktop
Requires: sed
Requires: breeze
Requires: breeze-icons
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

%cmake_qt5 -DPULL_TRANSLATIONS=NO -DBUNDLE_XDG_UTILS=NO -G Ninja

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

%find_lang %{name} --with-qt --all-name

%files -f %{name}.lang
%{_bindir}/startlxqt
%{_bindir}/lxqt-session
%{_bindir}/lxqt-leave
%{_bindir}/lxqt-config-session
%{_datadir}/applications/lxqt-*.desktop
%{_mandir}/man1/*
%{_datadir}/xsessions/lxqt.desktop
%{_sysconfdir}/xdg/autostart
%{_datadir}/lxqt/*.conf
%lang(arn) %{_datadir}/lxqt/translations/lxqt-config-session/lxqt-config-session_arn.qm
%lang(ast) %{_datadir}/lxqt/translations/lxqt-config-session/lxqt-config-session_ast.qm
%lang(arn) %{_datadir}/lxqt/translations/lxqt-leave/lxqt-leave_arn.qm
%lang(ast) %{_datadir}/lxqt/translations/lxqt-leave/lxqt-leave_ast.qm
%lang(arn) %{_datadir}/lxqt/translations/lxqt-session/lxqt-session_arn.qm
%lang(ast) %{_datadir}/lxqt/translations/lxqt-session/lxqt-session_ast.qm
