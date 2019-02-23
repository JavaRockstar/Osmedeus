import os, time
from core import execute
from core import utils

class TakeOverScanning(object):
    def __init__(self, options):
        utils.print_banner("Scanning for Subdomain TakeOver")
        self.module_name = self.__class__.__name__
        self.options = options
        self.initial()
        utils.just_waiting(self.module_name)
        self.conclude()


    def initial(self):
        self.tko_subs()
        self.subjack()

    def tko_subs(self):
        utils.print_good('Starting tko-subs')
        cmd = '$GO_PATH/tko-subs -data $PLUGINS_PATH/providers-data.csv -domains $WORKSPACE/subdomain/final-$TARGET.txt -output $WORKSPACE/subdomain/takeover-$TARGET-tko-subs.txt'

        cmd = utils.replace_argument(self.options, cmd)
        output_path = utils.replace_argument(self.options, '$WORKSPACE/subdomain/takeover-$TARGET-tko-subs.txt')
        std_path = utils.replace_argument(self.options, '$WORKSPACE/subdomain/std-takeover-$TARGET-tko-subs.std')
        execute.send_cmd(cmd, output_path, std_path, self.module_name)

    def subjack(self):
        utils.print_good('Starting subjack')
        cmd = '$GO_PATH/subjack -w $WORKSPACE/subdomain/final-$TARGET.txt -t 100 -timeout 30 -o $WORKSPACE/subdomain/takeover-$TARGET-subjack.txt -ssl'

        cmd = utils.replace_argument(self.options, cmd)
        output_path = utils.replace_argument(self.options, '$WORKSPACE/subdomain/takeover-$TARGET-subjack.txt')
        std_path = utils.replace_argument(self.options, '$WORKSPACE/subdomain/std-takeover-$TARGET-subjack.std')
        execute.send_cmd(cmd, output_path, std_path, self.module_name)

    #update the main json file
    def conclude(self):
        main_json = utils.reading_json(utils.replace_argument(self.options, '$WORKSPACE/$COMPANY.json'))
        main_json['Modules'][self.module_name] = utils.checking_done(module=self.module_name, get_json=True)

        #write that json again
        utils.just_write(utils.reading_json(utils.replace_argument(self.options, '$WORKSPACE/$COMPANY.json')), main_json, is_json=True)
            
        #logging
        logfile = utils.replace_argument(self.options, '$WORKSPACE/log.json')
        utils.save_all_cmd(logfile)





