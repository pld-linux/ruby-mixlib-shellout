#
# Conditional build:
%bcond_with	tests		# build with tests (not in gem)

%define pkgname mixlib-shellout
Summary:	Run external commands on Unix or Windows
Name:		ruby-%{pkgname}
Version:	3.4.10
Release:	1
License:	Apache v2.0
Group:		Development/Languages
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	2723cf6a9cc45d9443e547b48425069b
URL:		https://github.com/chef/mixlib-shellout
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
BuildRequires:	ruby-rspec
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Run external commands on Unix or Windows

%prep
%setup -q -n %{pkgname}-%{version}

%build
%__gem_helper spec

%if %{with tests}
rspec
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
%doc LICENSE
%{ruby_vendorlibdir}/mixlib/shellout.rb
%{ruby_vendorlibdir}/mixlib/shellout
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
%dir %{ruby_vendorlibdir}/mixlib
