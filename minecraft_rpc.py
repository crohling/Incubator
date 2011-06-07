import xmlrpclib, sys

def send_command(server, command):
    server.supervisor.sendProcessStdin('minecraft',command + '\n')
    return server.supervisor.tailProcessStderrLog('minecraft', -1, 256)[0].split('\n')[-2]

def give_item(server,player, item_number, number_per_stack, number_of_stacks):
    for i in range(number_of_stacks):
        send_command(server,'give ' + player + ' ' + str(item_number) + ' ' + str(number_per_stack))

def respawn(server, player):
    send_command(server,'give '+player+' 276 64')
    send_command(server,'give '+player+' 277 64')
    send_command(server,'give '+player+' 278 64')
    send_command(server,'give '+player+' 279 64')
    send_command(server,'give '+player+' 310 64')
    send_command(server,'give '+player+' 311 64')
    send_command(server,'give '+player+' 312 64')
    send_command(server,'give '+player+' 313 64')
    send_command(server,'give '+player+' 322 64')
    send_command(server,'give '+player+' 326 64')
    send_command(server,'give '+player+' 327 64')

def make_server(username, password, hostname, port):
    return xmlrpclib.Server('http://'+username+':'+password+'@'+hostname+':'+port)

if __name__=="__main__":
"""
	Dinky CLI
"""
    print sys.argv
    server = xmlrpclib.Server('http://'+sys.argv[1]+':'+sys.argv[2]+'@'+sys.argv[3]+':'+sys.argv[4])
    num = 1
    while True:
        try:
            sys.stdout.write('In ['+str(num)+']: ')
            command_split = sys.stdin.readline().split(' ')
            if 'quit' in command_split[0]:
                print '\tQuitting'
                break
            try:
                command = ' '.join(command_split[:-1])
                times = int(command_split[-1:][0])
                for i in range(times):
                    print '\tOut['+str(num)+']: ' + str(send_command(server, command))
            except Exception as excep:
                print excep
            num += 1

        except KeyboardInterrupt:
            print '\tQuitting'
            break
