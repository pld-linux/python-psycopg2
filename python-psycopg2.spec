#
# todo:
# - lib64 patch

%define 	module	psycopg2

Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl.UTF-8):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	2.0.11
Release:	3
License:	GPL
Group:		Libraries/Python
Source0:	http://initd.org/pub/software/psycopg/%{module}-%{version}.tar.gz
# Source0-md5:	eec2a45bcea75a00cbf20a15ab1b8bae
#Patch0:		%{name}-lib64.patch
URL:		http://www.initd.org/software/psycopg/
BuildRequires:	autoconf
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
Requires:	postgresql-libs
Requires:	python-modules
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
BuildConflicts:   python-egenix-mx-base
%endif
Requires:	python-pytz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch
with the aim of being very small and fast, and stable as a rock. The
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%description -l pl.UTF-8
psycopg jest przeznaczonym dla Pythona interfejsem do bazy danych
PostgreSQL (tak jak pygresql i popy). Został zakodowany od początku
z założeniem że ma być bardzo mały, szybki i stabilny. Główna zaletą
psycopg jest, że w jest pełni zgodny z standardem DBAPI-2.0 i jest
'thread safe' na poziomie 2.

%prep
%setup -q -n %{module}-%{version}
#%if "%{_lib}" == "lib64"
#%patch0 -p1
#%endif

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --optimize=2 --root=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{py_libdir} -type f -name "*.py" | xargs rm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog AUTHORS README doc/HACKING doc/SUCCESS doc/TODO
%dir %{py_sitedir}/%{module}
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py[co]
%if "%{pld_release}" != "ac"
%{py_sitedir}/*.egg-info
%endif
