%define name    igwn-auth-utils
%define version 0.2.0
%define release 1

Name:      %{name}
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
BuildRequires: python%{python3_pkgversion}-setuptools >= 38.2.5
BuildRequires: python%{python3_pkgversion}-setuptools_scm
BuildRequires: python%{python3_pkgversion}-wheel

# test dependencies
BuildRequires: python%{python3_pkgversion}-cryptography
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-scitokens >= 1.5.0

%description
Python library functions to simplify using IGWN authorisation credentials.
This project is primarily aimed at discovering X.509 credentials and
SciTokens for use with HTTP(S) requests to IGWN-operated services.

# -- python-3X-igwn-auth-utils

%package -n python%{python3_pkgversion}-%{name}
Requires: python%{python3_pkgversion}-cryptography
Requires: python%{python3_pkgversion}-scitokens >= 1.5.0
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
Recommends: python%{python3_pkgversion}-requests
Recommends: python%{python3_pkgversion}-safe-netrc
%endif
Summary:  %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%description -n python%{python3_pkgversion}-%{name}
Python library functions to simplify using IGWN authorisation credentials.
This project is primarily aimed at discovering X.509 credentials and
SciTokens for use with HTTP(S) requests to IGWN-operated services.

# -- build steps

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%check
cd %{_buildrootdir}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
%{__python3} -m pip show %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog

%changelog
* Mon Dec 20 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.2.0-1
- update to 0.2.0

* Thu Oct 7 2021 Duncan Macleod <duncan.macleod@ligo.org> - 0.1.0-1
- initial release
