
%include	/usr/lib/rpm/macros.python
%define 	module psycopg

Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	1.1.2
Release:	1
License:	GPL
Group:		Libraries/Python
Source0:	http://initd.org/pub/software/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	8e12369d92c1a949ff24a685eb82c37d
Patch0:		%{name}-dumb-ac-fix.patch
URL:		http://www.initd.org/software/psycopg/
BuildRequires:	postgresql-backend-devel
BuildRequires:	python-devel
BuildRequires:	python-mx-DateTime-devel
Requires:	postgresql-libs
Requires:	python
Requires:	python-mx-DateTime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch
with the aim of being very small and fast, and stable as a rock. The
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%description -l pl
psycopg jest przeznaczonym dla Pythona interfejsem do bazy danych
PostgreSQL (tak jak pygresql i popy). Zosta³ zakodowany od pocz±tku
z za³o¿eniem ¿e ma byæ bardzo ma³y, szybki i stabilny. G³ówna zalet±
psycopg jest, ¿e w jest pe³ni zgodny z standardem DBAPI-2.0 i jest
'thread safe' na poziomie 2.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%{__autoconf}

%configure \
	--with-python=%{_bindir}/python \
	--with-mxdatetime-includes=%{py_incdir}/mx \
	--with-postgres-includes=%{_includedir}/postgresql/server
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}

install psycopgmodule.so $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS FAQ NEWS README RELEASE-1.0 SUCCESS TODO doc
%attr(755,root,root) %{py_sitedir}/*.so
