%global pkg_name maven-release
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.2.1
Release:        12.14%{?dist}
Summary:        Release a project updating the POM and tagging in the SCM

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-release-plugin/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/release/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip
# Remove deps needed for tests, till jmock gets packaged
Patch1:         002-mavenrelease-fixbuild.patch
Patch2:         003-fixing-migration-to-component-metadata.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}maven-scm-test
BuildRequires:  %{?scl_prefix}maven-antrun-plugin
BuildRequires:  %{?scl_prefix}maven-jar-plugin
BuildRequires:  %{?scl_prefix}maven-javadoc-plugin
BuildRequires:  %{?scl_prefix}maven-source-plugin
BuildRequires:  %{?scl_prefix}maven-compiler-plugin
BuildRequires:  %{?scl_prefix}maven-install-plugin
BuildRequires:  %{?scl_prefix}maven-plugin-plugin
BuildRequires:  %{?scl_prefix}maven-resources-plugin
BuildRequires:  %{?scl_prefix}maven-site-plugin
BuildRequires:  %{?scl_prefix}maven-plugin-testing-harness
BuildRequires:  %{?scl_prefix}plexus-containers-component-metadata
BuildRequires:  %{?scl_prefix}plexus-utils
BuildRequires:  %{?scl_prefix}maven-surefire-plugin
BuildRequires:  %{?scl_prefix}maven-enforcer-plugin
BuildRequires:  %{?scl_prefix_java_common}jaxen


%description
This plugin is used to release a project with Maven, saving a lot of 
repetitive, manual work. Releasing a project is made in two steps: 
prepare and perform.


%package manager
Summary:        Release a project updating the POM and tagging in the SCM
Requires:       %{name} = %{version}-%{release}

%description manager
This package contains %{pkg_name}-manager needed by %{pkg_name}-plugin.


%package plugin
Summary:        Release a project updating the POM and tagging in the SCM
Requires:       %{name}-manager = %{version}-%{release}

%description plugin
This plugin is used to release a project with Maven, saving a lot of
repetitive, manual work. Releasing a project is made in two steps:
prepare and perform.


%package javadoc
Summary:        Javadocs for %{pkg_name}
Requires:       %{name} = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

%patch1 -p1
%patch2 -p1

# Jmock and mockito are not present
%pom_remove_dep jmock:
%pom_remove_dep jmock: maven-release-plugin
%pom_remove_dep jmock: maven-release-manager
%pom_remove_dep org.mockito: maven-release-manager

cat > README << EOT
%{pkg_name}-%{version}

This plugin is used to release a project with Maven, saving a lot of
repetitive, manual work. Releasing a project is made in two steps:
prepare and perform.
EOT

%mvn_file ":%{pkg_name}-{*}" %{pkg_name}-@1

%mvn_package :maven-release maven-release
%mvn_package ":maven-release-{*}" maven-release-@1
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Skip tests because we don't have dependencies (jmock)
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles-maven-release
%dir %{_mavenpomdir}/%{pkg_name}
%doc README LICENSE NOTICE

%files manager -f .mfiles-maven-release-manager
%doc LICENSE NOTICE

%files plugin -f .mfiles-maven-release-plugin
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 2.2.1-12.14
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.2.1-12.13
- maven33 rebuild

* Thu Jan 15 2015 Michal Srb <msrb@redhat.com> - 2.2.1-12.12
- Fix directory ownership

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.2.1-12.11
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.2.1-12.10
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.9
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.8
- Mass rebuild 2014-02-19

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.7
- Rebuild to get rid of auto-requires on java-devel

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.6
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.5
- Remove requires on java

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.4
- Rebuild to fix incorrect auto-requires

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-12.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.2.1-12
- Mass rebuild 2013-12-27

* Mon Aug 26 2013 Michal Srb <msrb@redhat.com> - 2.2.1-11
- Migrate away from mvn-rpmbuild (Resolves: #997504)

* Tue Jul 30 2013 Tomas Radej <tradej@redhat.com> - 2.2.1-10
- Removed Jmock + mockito

* Wed Jul 17 2013 Tomas Radej <tradej@redhat.com> - 2.2.1-9
- Installed LICENSE and NOTICE

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-8
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Sep 17 2012 Jaromir Capik <jcapik@redhat.com> - 2.2.1-5
- Fixing incomplete migration to component metadata

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-4
- Remove BR: maven-scm-test

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-1
- Update to latest upstream release.
- Adapt to current guidelines.

* Tue Jul 26 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-3
- Reinclude maven-scm-test in BRs

* Tue Jul 26 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-2
- Import patch provided by Jaromír Cápík (#725088)

* Mon Jul 18 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-1
- Update to 2.2
- Update to current guidelines
- Build with maven 3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 2.0-2
- Drop tomcat5 BRs.
- Drop versioned jars.

* Mon Sep 13 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-1
- Update to upstream 2.0

* Sat Sep 11 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.4
- Fix build requires
- Use javadoc:aggregate goal

* Tue May 25 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.3
- Fix build requires

* Mon May 10 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.2
- Fix release tag
- Better macro usage

* Mon Apr 26 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.1
- Install maven-release-parent pom in dedicated package
- Patch maven-release-plugin to skip helpmojo goal
- Patch to skip tests depending on (unpackaged) jmock

* Fri Apr 16 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn
- Initial packaging
