#
# Conditional build:
%bcond_without	tests		# build without tests

%define pkgname mixlib-shellout
Summary:	Run external commands on Unix or Windows
Name:		ruby-%{pkgname}
Version:	1.1.0
Release:	2
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	94d5aedb7c30a7b10d3b0da03bc4d62a
# Tests for this package are not in the gem. To update:
# git clone https://github.com/opscode/mixlib-shellout.git && cd mixlib-shellout
# git checkout 1.1.0
# tar czvf rubygem-mixlib-shellout-1.1.0-specs.tgz spec/
Source1:	rubygem-%{pkgname}-%{version}-specs.tgz
# Source1-md5:	60630f23b9a4da1036f3fd8c33e47585
# Patch for UsrMove, see http://tickets.opscode.com/browse/MIXLIB-6
Patch0:		mixlib-shellout-usrmove.patch
# Patch for removal of awesomeprint, see http://tickets.opscode.com/browse/MIXLIB-7
Patch1:		mixlib-shellout-awesomeprint-removal.patch
URL:		https://github.com/opscode/mixlib-shellout
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-rspec
BuildRequires:	ruby-rubygems
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
%patch0 -p1
%patch1 -p1

%build
%__gem_helper spec

%if %{with tests}
# One of the tests involves a fork && sleep 10 that may not finish before mock
rspec && sleep 10
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
