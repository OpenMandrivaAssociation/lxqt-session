Name: lxqt-session
Version: 0.7.0
Release: 2
Source0: http://lxqt.org/downloads/lxqt/%{version}/%{name}-%{version}.tar.xz
Summary: Session manager for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake
BuildRequires: cmake(lxqt)
BuildRequires: qt4-devel

%description
Session manager for the LXQt desktop

%prep
%setup -q -c %{name}-%{version}
%cmake

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
