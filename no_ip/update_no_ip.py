import urllib2, socket, dns.resolver, getpass, sys
from optparse import OptionParser


if __name__ == '__main__':
        
    optp = OptionParser()
    optp.add_option("-n", "--dyndns_name", dest="dns_name",
                    help="The dynamic dns hostname that needs to be monitored.")
    optp.add_option("-s", "--ip_service", dest="ip_service", default="http://whatismyip.org",
                    help="The external IP detection service used to get the current IP.")
    optp.add_option("-a", "--account_name", dest="account_name",
                    help="The no-ip account name for HTTP authentication")
    optp.add_option("-p", "--password", dest="password", 
                    help="The no-ip account password for HTTP authentication")
    

    opts, args = optp.parse_args()

    if None in [opts.dns_name, opts.ip_service, opts.account_name]:
        optp.print_help()
        sys.exit(1)
    ext_ip = urllib2.urlopen(opts.ip_service).read()
    for e in dns.resolver.query(opts.dns_name):
        dns_ip = e
    if ext_ip == dns_ip.to_text():
        print "No change in IP, %s points to %s" % (opts.dns_name, ext_ip)
        sys.exit(1)
    auth_man = urllib2.HTTPPasswordMgrWithDefaultRealm()
    auth_man.add_password(None, 'http://dynupdate.no-ip.com/nic/update', opts.account_name, (getpass.getpass() if not opts.password else opts.password))
    auth_handle = urllib2.HTTPBasicAuthHandler(auth_man)
    opener = urllib2.build_opener(auth_handle)
    urllib2.install_opener(opener)
    data = urllib2.urlopen('https://dynupdate.no-ip.com/nic/update?hostname=%s&myip=%s' % (opts.dns_name, ext_ip)).read()
    print '%s has changed from %s to %s' % (opts.dns_name, dns_ip.to_text() , ext_ip)
    print data
