
%include	/usr/lib/rpm/macros.python
%define 	module psycopg
%define 	version 1.0.12

%define 	release 0.9

Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl):	psycopg jest przeznaczyonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	%{version}
Release:	%{release}
Source0:	http://initd.org/pub/software/%{module}/%{module}-%{version}.tar.gz
Patch0:		%{name}-dumb-ac-fix.patch

Copyright:	GNU GPL
Group:		Applications/Databases
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Url:		http://www.initd.org/software/psycopg/
BuildRequires:	python-devel postgresql-backend-devel python-mx-DateTime-devel
Requires:	python python-egenix-mx-base postgresql-libs

%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch
with the aim of being very small and fast, and stable as a rock. The
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%description -l pl
psycopg jest przeznaczonym dla Pythona interfejsem do bazy danych
Postgresql (tak jak pygrsql i popy). Zosta³ zakodowany od pocz±tku
z za³o¿eniem ¿e ma byæ bardzo ma³y, szybki i stabilny. G³ówna zalet±
psycopg jest, ¿e w jest pe³ni zgodny z standardem DBAPI-2.0 i jest
'thread safe' na poziomie 2.


%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%{__autoconf}

%configure --with-python=%{_bindir}/python \
      --with-mxdatetime-includes=%{py_sitedir}/mx/DateTime/mxDateTime  \
      --with-postgres-includes=%{_includedir}/postgresql/server
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}
install -m 555 psycopgmodule.so $RPM_BUILD_ROOT%{py_sitedir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{py_sitedir}/*.so

#%files doc
%defattr(644,root,root,755)
%doc AUTHORS  COPYING  CREDITS  FAQ  INSTALL  NEWS  README  RELEASE-1.0  SUCCESS  TODO doc
