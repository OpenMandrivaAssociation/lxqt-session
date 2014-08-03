%define git 20140803

Name: lxqt-session
Version: 0.8.0
%if %git
Release: 0.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 1
Source0: http://lxqt.org/downloads/lxqt/%{version}/%{name}-%{version}.tar.xz
%endif
Summary: Session manager for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake
BuildRequires: cmake(lxqt-qt5)
BuildRequires: qt5-devel
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	cmake(Qt5X11Extras)

%description
Session manager for the LXQt desktop

%prep
%if %git
%setup -qn %{name}-%{git}
%else
%setup -q -c %{name}-%{version}
%endif
%cmake -DUSE_QT5:BOOL=ON

%build
%make -C build

%install
%makeinstall_std -C build

%files
%{_bindir}/lxqt-session
%{_bindir}/lxqt-config-session
%{_datadir}/lxqt/lxqt-session
%{_datadir}/lxqt/lxqt-config-session
%{_libdir}/lxqt-xdg-tools
%{_datadir}/applications/lxqt-config-session.desktop
