%define srcname igwn-auth-utils
%define version 1.0.1
%define release 1

Name:      python-%{srcname}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   Authorisation utilities for IGWN

License:   BSD-3-Clause
Url:       https://igwn-auth-utils.readthedocs.io
Source0:   %pypi_source

Packager:  Duncan Macleod <duncan.macleod@ligo.org>
Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch
Prefix:    %{_prefix}

# rpmbuild dependencies
BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros

# build dependencies
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-setuptools >= 38.2.5
BuildRequires: python%{python3_pkgversion}-setuptools_scm
BuildRequires: python%{python3_pkgversion}-wheel

%description
Python library functions to simplify using IGWN authorisation credentials.
This project is primarily aimed at discovering X.509 credentials and
SciTokens for use with HTTP(S) requests to IGWN-operated services.

# -- python-3X-igwn-auth-utils

%package -n python%{python3_pkgversion}-%{srcname}
Requires: python%{python3_pkgversion}-cryptography >= 2.3
Requires: python%{python3_pkgversion}-requests >= 2.14
Requires: python%{python3_pkgversion}-safe-netrc >= 1.0.0
Requires: python%{python3_pkgversion}-scitokens >= 1.7.0
Summary:  %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
Python library functions to simplify using IGWN authorisation credentials.
This project is primarily aimed at discovering X.509 credentials and
SciTokens for use with HTTP(S) requests to IGWN-operated services.

# -- build steps

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel igwn_auth_utils-%{version}-*.whl

%check
cd %{_buildrootdir}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
%{__python3} -m pip show %{srcname}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog

%changelog
* Wed Aug 16 2023 Duncan Macleod <duncan.macleod@ligo.org> - 1.0.1-1
- update to 1.0.1

* Wed Aug 16 2023 Duncan Macleod <duncan.macleod@ligo.org> - 1.0.0-1
- update to 1.0.0
- add BuildRequires: python3-devel
- add BuildRequires: python3-pip

* Tue Jan 17 2023 Duncan Macleod <duncan.macleod@ligo.org> - 0.4.0-1
- update to 0.4.0

* Sun Sep 18 2022 Duncan Macleod <duncan.macleod@ligo.org> - 0.3.1-1
- update to 0.3.1, 0.3.0 was forgotten in RPM
- promote requests interface requirements from suggested to requires

* Thu Jun 16 2022 Duncan Macleod <duncan.macleod@ligo.org> - 0.2.3-1
- update to 0.2.3

* Thu Apr 07 2022 Duncan Macleod <duncan.macleod@ligo.org> - 0.2.2-1
- update to 0.2.2
- add minimum versions for all runtime requirements

* Mon Apr 04 2022 Duncan Macleod <duncan.macleod@ligo.org> - 0.2.1-1
- update to 0.2.1
- bump scitokens requirement
- rename srpm to python-igwn-auth-utils

* Tue Dec 21 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.2.0-2
- remove unused buildrequires

* Mon Dec 20 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.2.0-1
- update to 0.2.0

* Thu Oct 7 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.1.0-1
- initial release
