
%define 	module	psycopg

Summary:	psycopg is a PostgreSQL database adapter for Python
Summary(pl):	psycopg jest przeznaczonym dla Pythona interfejsem do bazy PostgreSQL
Name:		python-%{module}
Version:	1.1.20
Release:	1
License:	GPL
Group:		Libraries/Python
Source0:	http://initd.org/pub/software/psycopg/%{module}-%{version}.tar.gz
# Source0-md5:	530674a8a8abbcc27c26c85a87925a3d
Patch0:		%{name}-lib64.patch
URL:		http://www.initd.org/software/psycopg/
BuildRequires:	autoconf
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
BuildRequires:	python-mx-DateTime-devel
Requires:	postgresql-libs
%pyrequires_eq	python-modules
Requires:	python-mx-DateTime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define zope_subname ZPsycopgDA

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

%package -n Zope-%{zope_subname}
Summary:	Zope PostgreSQL database adapter
Summary(pl):	Interfejs bazy danych PostgreSQL do Zope
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	Zope
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description -n Zope-%{zope_subname}
Zope PostgreSQL database adapter.

%description -n Zope-%{zope_subname} -l pl
Interfejs bazy danych PostgreSQL do Zope.

%prep
%setup -q -n %{module}-%{version}
%if "%{_lib}" == "lib64"
%patch0 -p1
%endif

%build
%{__autoconf}

%configure \
	--with-python=%{_bindir}/python \
	--with-mxdatetime-includes=%{py_incdir}/mx \
	--with-postgres-includes=%{_includedir}/postgresql/server
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{py_sitedir},%{_datadir}/Zope-%{zope_subname}}

install psycopgmodule.so $RPM_BUILD_ROOT%{py_sitedir}

cp -ar %{zope_subname}/* $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}
%py_comp $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}
rm -f $RPM_BUILD_ROOT%{_datadir}/Zope-%{zope_subname}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%post -n Zope-%{zope_subname}
/usr/sbin/installzopeproduct %{_datadir}/Zope-%{zope_subname} %{zope_subname}
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun -n Zope-%{zope_subname}
if [ "$1" = "0" ]; then
	/usr/sbin/installzopeproduct -d %{zope_subname} 
	if [ -f /var/lock/subsys/zope ]; then
		/etc/rc.d/init.d/zope restart >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS FAQ NEWS README RELEASE-1.0 SUCCESS TODO doc
%attr(755,root,root) %{py_sitedir}/*.so

%files -n Zope-%{zope_subname}
%defattr(644,root,root,755)
%{_datadir}/Zope-%{zope_subname}
