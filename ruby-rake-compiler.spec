#
# Conditional build:
%bcond_with	tests		# build without tests

%define gemname rake-compiler
Summary:	Rake-based Ruby C Extension task generator
Name:		ruby-%{gemname}
Version:	0.8.3
Release:	2
License:	MIT
Group:		Development/Languages
Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
# Source0-md5:	1c05370b503649468b2e3ae50ba23ec0
# https://github.com/luislavena/rake-compiler/commit/19382092f6ffcbea16aa84
Patch0:		rubygem-rake-compiler-0.8.3-spec-with-ruby200.patch
URL:		http://rake-compiler.rubyforge.org/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
#BuildRequires:	ruby-cucumber
#BuildRequires:	ruby-isolate
#BuildRequires:	ruby-rake
#BuildRequires:	ruby-rcov
BuildRequires:	ruby-rspec
BuildRequires:	ruby-rubygems >= 1.3.5
%endif
Requires:	ruby-rake >= 0.8.3
Requires:	ruby-rubygems >= 1.3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rake-compiler aims to help Gem developers while dealing with Ruby C
extensions, simplifiying the code and reducing the duplication.

It follows *convention over configuration* and set an standarized
structure to build and package C extensions in your gems.

This is the result of expriences dealing with several Gems that
required native extensions across platforms and different user
configurations where details like portability and clarity of code were
lacking.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{gemname}-%{version}
%patch0 -p1

%build
%if %{with tests}
# Modify Isolate file
cp -p Isolate{,.orig}
sed -i -e 's|gem |# gem|' Isolate

# cucumber 0.10.0 needs fixing for newer rake (0.9.0 beta5)
# rake aborted!
# undefined method `desc' for #<Cucumber::Rake::Task:0xb742ebb0>
# rake spec
ruby -Ilib -S rspec spec/

# back to the original
mv -f Isolate{.orig,}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rdoc History.txt LICENSE.txt
%attr(755,root,root) %{_bindir}/rake-compiler
%dir %{ruby_vendorlibdir}/rake
%{ruby_vendorlibdir}/rake/baseextensiontask.rb
%{ruby_vendorlibdir}/rake/extensioncompiler.rb
%{ruby_vendorlibdir}/rake/extensiontask.rb
%{ruby_vendorlibdir}/rake/javaextensiontask.rb
