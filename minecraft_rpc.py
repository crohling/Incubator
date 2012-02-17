import xmlrpclib, sys

class minecraft_server():

    def __init__(self, username, password, hostname, port, proc_name='minecraft'):
        self.proc_name=proc_name
        self.server = xmlrpclib.Server('http://'+username+':'+password+'@'+hostname+':'+port)
    def send_command(self, command):
        self.server.supervisor.sendProcessStdin(self.proc_name,command + '\n')
        return self.server.supervisor.tailProcessStderrLog(self.proc_name, -1, 256)[0].split('\n')[-2]
    
    def give_item(self, player, item_number, number_per_stack, number_of_stacks):
        for i in range(number_of_stacks):
            self.send_command('give ' + player + ' ' + str(item_number) + ' ' + str(number_per_stack))
    
    def respawn(self, player):
        self.send_command('give '+player+' 276')
        self.send_command('give '+player+' 277')
        self.send_command('give '+player+' 278')
        self.send_command('give '+player+' 279')
        self.send_command('give '+player+' 310')
        self.send_command('give '+player+' 311')
        self.send_command('give '+player+' 312')
        self.send_command('give '+player+' 313')
        self.send_command('give '+player+' 322 64')
        self.send_command('give '+player+' 326')
        self.send_command('give '+player+' 327')
