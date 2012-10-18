#!/usr/bin/python

import urllib2, json, time, smtplib
from optparse import OptionParser

previous_state = True

if __name__=="__main__":
    optp = OptionParser()
    optp.add_option("-c", "--config", dest="config",
                     help="The JSON config file")
    opts, args = optp.parse_args()
    if opts.config:
        config_file = open(opts.config,'r')
        config = json.load(config_file)
    else:
        optp.print_help()
        sys.exit(1)
    previous_state = json.loads(urllib2.urlopen('http://us.battle.net/api/wow/realm/status?realms=%s' % config['realm']).read())['realms'][0]['status']
    while True:
        realm_map = json.loads(urllib2.urlopen('http://us.battle.net/api/wow/realm/status?realms=%s' % config['realm']).read())
        if(previous_state != realm_map['realms'][0]['status']):
            smtpObj = smtplib.SMTP(config['smtp_server'], int(config['smtp_port']))
            for reciever in recievers:
                message = "From: Realm Daemon <%s>\nTo: Antilus <%s>\nSubject:Realm Status Change - %s\n\nBlack Dragonflight is now %s" % (config['sender'], reciever, config['realm'], ("Online" if realm_map['realms'][0]['status'] else "Offline"))
            smtpObj.sendmail(config['sender'], config['recievers'], message)
            print realm_map
        previous_state = realm_map['realms'][0]['status']
        time.sleep(30)
