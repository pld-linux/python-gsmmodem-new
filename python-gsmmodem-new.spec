# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		gsmmodem
%define		egg_name	python_gsmmodem_new
%define		pypi_name	gsmmodem-new
Summary:	GSM modem module for Python
Name:		python-%{pypi_name}
Version:	0.12
Release:	4
License:	LGPL v3+
Group:		Libraries/Python
Source0:	https://github.com/babca/python-gsmmodem/archive/%{version}.tar.gz
# Source0-md5:	797db0e6c9068daa4d3c88d8425a3ccd
URL:		https://github.com/babca/python-gsmmodem
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
%{?with_tests:BuildRequires:	python-serial}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
%{?with_tests:BuildRequires:	python3-serial}
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
Requires:	python-serial
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows easy control of a GSM modem attached to the system. It also
includes a couple of useful commandline utilities for interacting with
a GSM modem.

%package -n python3-%{pypi_name}
Summary:	GSM modem module for Python
Group:		Libraries/Python
Requires:	python3-modules
Requires:	python3-serial

%description -n python3-%{pypi_name}
Allows easy control of a GSM modem attached to the system. It also
includes a couple of useful commandline utilities for interacting with
a GSM modem.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n python-gsmmodem-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/gsmtermlib
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python-%{pypi_name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gsmterm.py
%attr(755,root,root) %{_bindir}/identify-modem.py
%attr(755,root,root) %{_bindir}/sendsms.py
%doc AUTHORS ChangeLog README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/gsmtermlib
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{pypi_name}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
