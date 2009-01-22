#
# todo:
# - lib64 patch

%define 	module	psycopg2

Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl.UTF-8):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	2.0.8
Release:	4
License:	GPL
Group:		Libraries/Python
Source0:	http://initd.org/pub/software/psycopg/%{module}-%{version}.tar.gz
# Source0-md5:	2c31827878d436b0c89e777989ff55af
#Patch0:		%{name}-lib64.patch
URL:		http://www.initd.org/software/psycopg/
BuildRequires:	autoconf
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
Requires:	postgresql-libs
%pyrequires_eq	python-modules
%if "%{pld_release}" == "ac"
BuildRequires:	python-mx-DateTime-devel
Requires:	python-mx-DateTime
%else
# allow mx.DateTime to be optional
# don't use Suggest - it is rare to use mx.DateTime; python provides its
# own datetime implementation, now
BuildConflicts:   python-mx-DateTime
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
%if "%{pld_release}" == "ac"
%{py_sitedir}/*.egg-info
%endif
