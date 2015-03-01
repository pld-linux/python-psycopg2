# TODO:
# - lib64 patch

# Conditional build:
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module

%define 	module	psycopg2
Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl.UTF-8):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	2.5.1
Release:	3
License:	GPL
Group:		Libraries/Python
Source0:	http://initd.org/psycopg/tarballs/PSYCOPG-2-5/%{module}-%{version}.tar.gz
# Source0-md5:	1b433f83d50d1bc61e09026e906d84c7
#Patch0:		%{name}-lib64.patch
URL:		http://www.initd.org/software/psycopg/
BuildRequires:	autoconf
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
%{?with_python2:BuildRequires:	python-devel >= 2.5}
%{?with_python3:BuildRequires:	python3-devel}
BuildRequires:	rpm-pythonprov
Requires:	postgresql-libs
Requires:	python-modules
Requires:	python-pytz
%if "%{pld_release}" == "ac"
BuildRequires:	python-mx-DateTime-devel
Requires:	python-mx-DateTime
%else
# if somebody really needs mx.DateTime, then one can request mx.Datetime
# usage on runtime;
# it is pointless to use 'Requires' or 'Suggest' field because
# - python provides its own datetime implementation
# - one can request it on runtime (as said above)
# - usage of mx.DateTime type is application specific
# Sure, but make mx-DateTime conditional build work
BuildConflicts:	python-egenix-mx-base
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch
with the aim of being very small and fast, and stable as a rock. The
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%description -l pl.UTF-8
psycopg jest przeznaczonym dla Pythona interfejsem do bazy danych
PostgreSQL (tak jak pygresql i popy). Został zakodowany od początku z
założeniem że ma być bardzo mały, szybki i stabilny. Główna zaletą
psycopg jest, że w jest pełni zgodny z standardem DBAPI-2.0 i jest
'thread safe' na poziomie 2.

%package -n python3-%{module}
Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl.UTF-8):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Group:		Libraries/Python
Requires:	python3-modules
Requires:	python3-pytz

%description -n python3-%{module}
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch
with the aim of being very small and fast, and stable as a rock. The
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%description -n python3-%{module} -l pl.UTF-8
psycopg jest przeznaczonym dla Pythona interfejsem do bazy danych
PostgreSQL (tak jak pygresql i popy). Został zakodowany od początku z
założeniem że ma być bardzo mały, szybki i stabilny. Główna zaletą
psycopg jest, że w jest pełni zgodny z standardem DBAPI-2.0 i jest
'thread safe' na poziomie 2.

%prep
%setup -q -n %{module}-%{version}
#%if "%{_lib}" == "lib64"
#%patch0 -p1
#%endif

%build
%if %{with python2}
%{__python} setup.py build
%endif
%if %{with python3}
%{__python3} setup.py build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif
%if %{with python3}
%{__python3} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc NEWS AUTHORS README doc/HACKING doc/SUCCESS
%dir %{py_sitedir}/%{module}
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py[co]
%if "%{pld_release}" != "ac"
%{py_sitedir}/*.egg-info
%endif
%{py_sitedir}/%{module}/tests
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc NEWS AUTHORS README doc/HACKING doc/SUCCESS
%dir %{py3_sitedir}/%{module}
%dir %{py3_sitedir}/%{module}/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__/*.py*
%{py3_sitedir}/*.egg-info
%{py3_sitedir}/%{module}/tests
%endif
