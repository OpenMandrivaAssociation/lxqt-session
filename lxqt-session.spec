%define git 0

Name: lxqt-session
Version: 0.9.0
%if %git
Release: 0.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 2
Source0: http://lxqt.org/downloads/lxqt/%{version}/%{name}-%{version}.tar.xz
%endif
Summary: Session manager for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake
BuildRequires: pkgconfig(lxqt)
BuildRequires: qt5-devel
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: desktop-file-utils
Requires:	xdg-utils
%rename		razorqt-session

%description
Session manager for the LXQt desktop

%prep
%if %git
%setup -qn %{name}-%{git}
%else
%setup -q
%endif
%apply_patches
%cmake -DUSE_QT5:BOOL=ON -DBUNDLE_XDG_UTILS=No

%build
%make -C build

%install
%makeinstall_std -C build

# (tpg) fix for E: invalid-desktopfile (Badness: 1) /usr/share/applications/lxqt-shutdown.desktop value "LXQt;" 
# for key "OnlyShowIn" in group "Desktop Entry" contains an unregistered value "LXQt"; 
# values extending the format should start with "X-
for name in config-session hibernate lockscreen logout reboot shutdown suspend; do 
	desktop-file-edit --remove-category=LXQt --add-category=X-LXQt \
    --remove-only-show-in=LXQt --add-only-show-in=X-LXQt %{buildroot}%{_datadir}/applications/lxqt-${name}.desktop
done

%files
%{_bindir}/lxqt-session
%{_bindir}/lxqt-leave
%{_bindir}/lxqt-config-session
%{_datadir}/applications/lxqt-*.desktop
%{_datadir}/lxqt/translations/lxqt-session
%{_datadir}/lxqt/translations/lxqt-config-session
