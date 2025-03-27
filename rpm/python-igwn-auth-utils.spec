%define srcname igwn-auth-utils
%global distname %{lua:name = string.gsub(rpm.expand("%{srcname}"), "[.-]", "_"); print(name)}
%define version 1.3.1
%define release 1

Name:      python-%{srcname}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   Authorisation utilities for IGWN

License:   BSD-3-Clause
Url:       https://igwn-auth-utils.readthedocs.io
Source0:   %pypi_source %distname

Packager:  Duncan Macleod <duncan.macleod@ligo.org>
Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch
Prefix:    %{_prefix}

# build dependencies
BuildRequires: python3-devel
BuildRequires: python3dist(pip)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(setuptools-scm)
BuildRequires: python3dist(wheel)

%description
Python library functions to simplify using IGWN authorisation credentials.
This project is primarily aimed at discovering X.509 credentials and
SciTokens for use with HTTP(S) requests to IGWN-operated services.

# -- python-3X-igwn-auth-utils

%package -n python3-%{srcname}
Summary:  %{summary}
Recommends: python3dist(gssapi)
Recommends: python3dist(htgettoken)
%description -n python3-%{srcname}
Python library functions to simplify using IGWN authorisation credentials.
This project is primarily aimed at discovering X.509 credentials and
SciTokens for use with HTTP(S) requests to IGWN-operated services.
%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- build steps

%prep
%autosetup -n %{distname}-%{version}

%if 0%{?rhel} && 0%{?rhel} < 10
echo "Writing setup.cfg for setuptools %{setuptools_version}"
# hack together setup.cfg for old setuptools to parse
cat > setup.cfg << SETUP_CFG
[metadata]
name = %{srcname}
version = %{version}
author-email = %{packager}
description = %{summary}
license = %{license}
license_files = LICENSE
url = %{url}
[options]
packages = find:
python_requires = >=%{python3_version}
install_requires =
  cryptography
  requests
  safe-netrc >= 1.0
  scitokens >= 1.8
[options.extras_require]
kerberos =
  gssapi
gettoken =
  htgettoken >= 2.1
SETUP_CFG
%endif

%if %{undefined pyproject_wheel}
echo "Writing setup.py for py3_build_wheel"
# write a setup.py to be called explicitly
cat > setup.py << SETUP_PY
from setuptools import setup
setup(use_scm_version=True)
SETUP_PY
%endif

%build
# build a wheel
%if %{defined pyproject_wheel}
%pyproject_wheel
%else
%py3_build_wheel
%endif

%install
# install the wheel
%if %{defined pyproject_wheel}
%pyproject_install
%else
%py3_install_wheel %{distname}-%{version}-*.whl
%endif

%check
cd %{_buildrootdir}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
%{__python3} -m pip show %{srcname}

%clean
rm -rf $RPM_BUILD_ROOT

# -- changelog

%changelog
* Wed Mar 26 2025 Duncan Macleod <duncan.macleod@ligo.org> - 1.3.1-1
- Update to 1.3.1
- Move python3-gssapi and python3-htgettoken from Requires to Recommends

* Wed Mar 26 2025 Duncan Macleod <duncan.macleod@ligo.org> - 1.3.0-1
- Update to 1.3.0
- Remove some version requirements for baseos/epel packages
- Add requirement on python3dist(htgettoken)

* Tue Mar 18 2025 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.1-1
- update to 1.2.1

* Mon Feb 24 2025 Duncan Macleod <duncan.macleod@ligo.org> - 1.2.0-1
- update to 1.2.0
- update requirements versions

* Fri Sep 06 2024 Duncan Macleod <duncan.macleod@ligo.org> - 1.1.1-1
- update to 1.1.1
- update build to use pyproject.toml for all metadata

* Wed Oct 18 2023 Duncan Macleod <duncan.macleod@ligo.org> - 1.1.0-1
- update to 1.1.0

* Thu Aug 24 2023 Duncan Macleod <duncan.macleod@ligo.org> - 1.0.2-1
- update to 1.0.2

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
