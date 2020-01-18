### Git submodules
### * i3ipcpp
%global commit1         21ce9060ac7c502225fdbd2f200b1cbdd8eca08d
%global shortcommit1    %(c=%{commit1}; echo ${c:0:7})

### * xpp
%global commit2         f70dd8bb50944ab64ab902d9d8ab555599249dc1
%global shortcommit2    %(c=%{commit2}; echo ${c:0:7})

%global url1    https://github.com/%{name}

Name:           polybar
Version:        3.4.2
Release:        2%{?dist}
Summary:        Fast and easy-to-use status bar

# BSD 2-clause "Simplified" License
# ---------------------------------
# lib/concurrentqueue/
#
# Expat License
# -------------
# lib/i3ipcpp/
# lib/xpp/
#
License:        MIT and BSD
URL:            https://polybar.github.io/
Source0:        %{url1}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

### Bundled libs
Source1:        %{url1}/i3ipcpp/archive/%{commit1}/i3ipcpp-%{shortcommit1}.tar.gz
Source2:        %{url1}/xpp/archive/%{commit2}/xpp-%{shortcommit2}.tar.gz

BuildRequires:  cmake >= 3.1
BuildRequires:  gcc-c++
BuildRequires:  i3-devel
BuildRequires:  libmpdclient-devel
BuildRequires:  libnl3-devel
BuildRequires:  python3 >= 3.5
BuildRequires:  python3-sphinx
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-xrm-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(jsoncpp) >= 1.7.7
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(xcb-proto)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcb)
Provides:       bundled(i3ipcpp) = 0.4
Provides:       bundled(xpp)

%description
Polybar aims to help users build beautiful and highly customizable status bars
for their desktop environment, without the need of having a black belt in shell
scripting.


%prep
%setup -q
%setup -q -D -T -a1
%setup -q -D -T -a2

mv i3ipcpp-%{commit1}/* lib/i3ipcpp
mv xpp-%{commit2}/*     lib/xpp

mkdir -p doc/%{_target_platform}
mkdir -p %{_target_platform}


%build
### Build man page
pushd doc/%{_target_platform}
%cmake  \
    ..
popd
%make_build -C doc/%{_target_platform} doc_man

pushd %{_target_platform}
%cmake                                  \
    -DBUILD_DOC=false                   \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo   \
    ..
popd
%make_build -C %{_target_platform}


%install
%make_install -C %{_target_platform}

### Install man page
install -m 0644 -Dp doc/%{_target_platform}/man/%{name}.1 \
    %{buildroot}/%{_mandir}/man1/%{name}.1


%files
%license LICENSE
%doc README.md SUPPORT.md
%{_bindir}/%{name}
%{_bindir}/%{name}-msg
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/
%{_docdir}/%{name}/config
%{_mandir}/man1/*


%changelog
* Sat Dec 28 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 3.4.2-2
- Replace wireless-tools-devel with libnl3-devel (upstream recommendation)

* Fri Dec 27 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Sat Dec 21 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 3.4.1-4
- Update to 3.4.1
- Packaging fixes

* Thu Sep 05 2019 Franco Comida <fcomida@users.sourceforge.net> - 3.4.0-1
- Version 3.4.0
