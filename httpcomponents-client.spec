Name:              httpcomponents-client
Summary:           HTTP agent implementation based on httpcomponents HttpCore
Version:           4.0.3
Release:           5
Group:             Development/Java
License:           ASL 2.0
URL:               http://hc.apache.org/
Source0:           http://www.apache.org/dist/httpcomponents/httpclient/source/httpcomponents-client-%{version}-src.tar.gz
# Remove optional build deps not available in Fedora
Patch0:            0001-Cleanup-pom.patch

BuildArch:         noarch


BuildRequires:     httpcomponents-project
BuildRequires:     httpcomponents-core


Requires:          java >= 0:1.6.0
Requires:          jpackage-utils
Requires:          httpcomponents-core

Requires(post):    jpackage-utils
Requires(postun):  jpackage-utils

%description
HttpClient is a HTTP/1.1 compliant HTTP agent implementation based on
httpcomponents HttpCore. It also provides reusable components for
client-side authentication, HTTP state management, and HTTP connection
management. HttpComponents Client is a successor of and replacement
for Commons HttpClient 3.x. Users of Commons HttpClient are strongly
encouraged to upgrade.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description    javadoc
%{summary}.


%prep
%setup -q
%patch0 -p1

%build
# skip httpmime, httpclient only. For httpmime we need org.apache.james:apache-mime4j
cd httpclient
export maven_repo_local=$(pwd)/.m2/repository
install -d $maven_repo_local

mvn-jpp -Dmaven.repo.local=$maven_repo_local \
        install javadoc:javadoc


%install
cd httpclient
# jars
install -D -m 0644 target/httpclient-%{version}.jar %{buildroot}%{_javadir}/%{name}/httpclient.jar

# pom
install -D -m 0644 pom.xml \
    %{buildroot}/%{_mavenpomdir}/JPP.%{name}-httpclient.pom
%add_to_maven_depmap org.apache.httpcomponents httpclient %{version} JPP/%{name} httpclient

# main pom
install -D -m 0644 ../pom.xml \
    %{buildroot}/%{_mavenpomdir}/JPP.%{name}-httpcomponents-client.pom
%add_to_maven_depmap org.apache.httpcomponents httpcomponents-client %{version} JPP/%{name} httpcomponents-client

# javadocs
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}


%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt RELEASE_NOTES.txt
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/JPP.%{name}*.pom
%{_javadir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%doc %{_javadocdir}/*


