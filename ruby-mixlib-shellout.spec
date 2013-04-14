%define gem_name mixlib-shellout
Summary:	Run external commands on Unix or Windows
Name:		ruby-%{gem_name}
Version:	1.1.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Source0-md5:	94d5aedb7c30a7b10d3b0da03bc4d62a
# Tests for this package are not in the gem. To update:
# git clone https://github.com/opscode/mixlib-shellout.git && cd mixlib-shellout
# git checkout 1.1.0
# tar czvf rubygem-mixlib-shellout-1.1.0-specs.tgz spec/
Source1:	rubygem-%{gem_name}-%{version}-specs.tgz
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
%setup -q -n %{gem_name}-%{version}

%build
%if %{with tests}
tar zxvf %{SOURCE1}
patch -p1 < %{PATCH0}
patch -p1 < %{PATCH1}
# One of the tests involves a fork && sleep 10 that may not finish before mock
rspec && sleep 10
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%{ruby_vendorlibdir}/mixlib/shellout.rb
%{ruby_vendorlibdir}/mixlib/shellout
