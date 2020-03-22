#
# Conditional build:
%bcond_with	tests		# build without tests

%define gemname rake-compiler
Summary:	Rake-based Ruby C Extension task generator
Summary(pl.UTF-8):	Generator zadań Rake'a do budowania rozszerzeń języka Ruby napisanych w C
Name:		ruby-%{gemname}
Version:	1.0.7
Release:	2
License:	MIT
Group:		Development/Languages
Source0:	https://rubygems.org/downloads/%{gemname}-%{version}.gem
# Source0-md5:	ec3acc332e3c86760b3f4dbdc5351192
URL:		https://rubygems.org/gems/rake-compiler/
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

This is the result of experiences dealing with several Gems that
required native extensions across platforms and different user
configurations where details like portability and clarity of code were
lacking.

%description -l pl.UTF-8
rake-compiler ma na celu pomoc twórcom rozszerzeń Gem przy obsłudze
rozszerzeń języka Ruby napisanych w C, upraszczając kod i zmniejszając
duplikację.

Jest zgodny z paradygmatem "konwencja ponad konfiguracją" i tworzy
ustandaryzowaną strukturę do budowania i pakietowania rozszerzeń w C
do plików gem.

Moduł jest wynikiem doświadczeń przy różnych Gemach, wymagających
natywnych rozszerzeń na różnych platformach, z różną konfiguracją
użytkownika, gdzie zabrakło przenośności i czytelności kodu.

%package doc
Summary:	Documentation for Ruby rake-compiler module
Summary(pl.UTF-8):	Dokumentacja modułu języka Ruby rake-compiler
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains documentation for Ruby rake-compiler module.

%description doc -l pl.UTF-8
Ten pakiet zawiera dokumentację do modułu języka Ruby rake-compiler.

%prep
%setup -q -n %{gemname}-%{version}

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+ruby(\s|$),#!%{__ruby}\1,' bin/rake-compiler

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
%{__mv} Isolate{.orig,}
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
