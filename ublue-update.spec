Name:          {{{ git_dir_name }}}
Vendor:        ublue-os
Version:       {{{ ublue_update_version }}}
Release:       1%{?dist}
Summary:       Centralized update service/checker made for Universal Blue
License:       Apache-2.0
URL:           https://github.com/%{vendor}/%{name}
# Detailed information about the source Git repository and the source commit
# for the created rpm package
VCS:           {{{ git_dir_vcs }}}

# git_dir_pack macro places the repository content (the source files) into a tarball
# and returns its filename. The tarball will be used to build the rpm.
Source:        {{{ git_dir_pack }}}

BuildArch:     noarch
Supplements:   rpm-ostree flatpak
BuildRequires: just
BuildRequires: systemd-rpm-macros
BuildRequires: black
BuildRequires: python-flake8
BuildRequires: python-build
BuildRequires: python-setuptools
BuildRequires: python
BuildRequires: python-pip
BuildRequires: python-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: python-setuptools_scm
BuildRequires: python-wheel
Requires:      skopeo
Requires:      libnotify
Requires:      systemd

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-", ""); print(t)}

%description
Installs and configures ublue-update script, systemd services, and systemd timers for auto update

%prep
{{{ git_dir_setup_macro }}}

%build
ls
ls src
black src
flake8 src
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files ublue_update
cp -rp files/usr %{buildroot}

%pre
if [ ! -x /usr/bin/topgrade ]
then
    echo "Topgrade not installed. Please install Topgrade (https://github.com/topgrade-rs/topgrade) to use %{NAME}."
    exit 1
fi

%post
%systemd_post %{NAME}.timer

%preun
%systemd_preun %{NAME}.timer

%files -f %{pyproject_files}
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/%{NAME}.service
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/%{NAME}.timer
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system-preset/60-%{NAME}.preset
%attr(0644,root,root) %{_exec_prefix}/etc/%{NAME}/*.toml
%attr(0644,root,root) %{_datadir}/%{NAME}/*.toml
%attr(0644,root,root) %{_datadir}/polkit-1/rules.d/%{NAME}.rules

%changelog
%autochangelog
