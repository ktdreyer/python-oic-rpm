%global pypi_name oic
%global pypi_version 1.3.0

# Some test dependencies not yet available
%bcond_with tests

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Python implementation of OAuth2 and OpenID Connect

License:        Apache 2.0
URL:            https://github.com/OpenIDC/pyoidc/
Source0:        %{pypi_source}
Source1:        %{pypi_name}-%{version}-tests.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%if %{with tests}
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(defusedxml)
BuildRequires:  python3dist(freezegun)
BuildRequires:  python3dist(mako)
# pyldap -> python-ldap @ https://github.com/OpenIDC/pyoidc/issues/797
BuildRequires:  python3dist(pyldap)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(requests)
BuildRequires:  python3dist(responses)
BuildRequires:  python3dist(testfixtures)
%endif

%description
This is a complete implementation of OpenID Connect as specified in the OpenID
Connect Core specification. And as a side effect, a complete implementation of
OAuth2.0 too.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
%description -n python3-%{pypi_name}
This is a complete implementation of OpenID Connect as specified in the OpenID
Connect Core specification. And as a side effect, a complete implementation of
OAuth2.0 too.

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# These libraries are only used in the code examples on GitHub,
# not in main library code on PyPI:
sed -i '/"beaker"/d' setup.py
sed -i '/"pycryptodomex"/d' setup.py
sed -i '/"pyjwkest/d' setup.py

%if %{with tests}
%autosetup -T -D -b1 -n %{pypi_name}-%{pypi_version}
%endif

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%if 0%{with tests}
%check
py.test oic-%{version}/tests
%endif

%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{_bindir}/oic-client-management
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/oic/extension
%{python3_sitelib}/oic/oauth2
%{python3_sitelib}/oic/oic
%{python3_sitelib}/oic/utils
%{python3_sitelib}/oic/utils/authn
%{python3_sitelib}/oic/utils/rp
%{python3_sitelib}/oic/utils/userinfo
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Mon Sep 20 2021 Ken Dreyer <kdreyer@redhat.com> - 1.3.0-1
- Initial package.
