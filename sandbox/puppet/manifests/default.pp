class site {
    # Using puppet for provisioning requires a puppet group
    group {"puppet":
        ensure => present,
    }
}

Exec { path => [ "/usr/local/bin", "/bin", "/sbin", "/usr/bin", "/usr/sbin" ] }
include site