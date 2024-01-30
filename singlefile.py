# -*- coding: utf-8 -*-
import subprocess
import time

class SingleFile(object):
    def __init__(self, chrome_cwd, single_file_cwd):
        self.chrome_cwd = chrome_cwd
        self.single_file_cwd = single_file_cwd

    def prepare_env(self):
        #  1. node  env
        #  2. chrome env
        pass

    def execute(self, url: str) -> str:
        command = f'''node single-file --browser-executable-path {self.chrome_cwd} {url} --back-end=puppeteer --dump-content'''
        print(command)
        args = command.split(" ")
        args = list(filter(lambda x: x is not None and x != '' and x != '\n', args))
        completed_process = subprocess.run(args,
                                           shell=False,
                                           capture_output=True,
                                           cwd=self.single_file_cwd,
                                           encoding="utf-8")
        return str(completed_process.stdout)


if __name__ == '__main__':
    start_time = time.time()
    single_file = SingleFile(chrome_cwd="/usr/bin/google-chrome-stable", single_file_cwd="/workspaces/workflow-flask/PySingleFile/single-file-cli")
    res = single_file.execute("https://pornhub.com")
    with open(r'tmp2.html', mode='w') as fw:
        fw.write(res)
        fw.flush()
    print(f'==>cost = {time.time()- start_time} ms')
