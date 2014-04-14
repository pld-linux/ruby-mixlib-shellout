#
# Conditional build:
%bcond_without	tests		# build without tests

%if 0
# Tests for this package are not in the gem. To update:
V=1.4.0
git clone https://github.com/opscode/mixlib-shellout.git
GIT_DIR=mixlib-shellout/.git git fetch origin $V
GIT_DIR=mixlib-shellout/.git git archive $V spec/ | bzip2 -9 > mixlib-shellout-specs-$V.tar.bz2
./dropin mixlib-shellout-specs-$V.tar.bz2 &
%endif

%define pkgname mixlib-shellout
Summary:	Run external commands on Unix or Windows
Name:		ruby-%{pkgname}
Version:	1.4.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	1f5d0e776ef20332634f31ada8022d66
Source1:	%{pkgname}-specs-%{version}.tar.bz2
# Source1-md5:	e1c9c7aefba7f9db112e903f7b2f8824
URL:		https://github.com/opscode/mixlib-shellout
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-rubygems
%if %{with tests}
BuildRequires:	ruby-rspec < 3
BuildRequires:	ruby-rspec >= 2.0
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Run external commands on Unix or Windows

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -n %{pkgname}-%{version} -a1

%build
%__gem_helper spec

%if %{with tests}
# One of the tests involves a fork && sleep 10 that may not finish before mock
rspec
sleep 10
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%{ruby_vendorlibdir}/mixlib/shellout.rb
%{ruby_vendorlibdir}/mixlib/shellout
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
