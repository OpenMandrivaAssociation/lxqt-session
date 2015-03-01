%define git 0

Name: lxqt-session
Version: 0.9.0
%if %git
Release: 0.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 6
Source0: http://lxqt.org/downloads/lxqt/%{version}/%{name}-%{version}.tar.xz
%endif
Summary: Session manager for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
Patch0: lxqt-session-0.9.0-fix-desktop-files.patch
BuildRequires: cmake
BuildRequires: pkgconfig(lxqt)
BuildRequires: qt5-devel
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(Qt5X11Extras)
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


%find_lang %{name} --with-qt
%find_lang lxqt-config-session --with-qt

%files -f %{name}.lang -f lxqt-config-session.lang
%{_bindir}/lxqt-session
%{_bindir}/lxqt-leave
%{_bindir}/lxqt-config-session
%{_datadir}/applications/lxqt-*.desktop
%{_datadir}/lxqt/translations/lxqt-session/lxqt-session_*.qm
