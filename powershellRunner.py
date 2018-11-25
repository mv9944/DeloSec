import subprocess
import os


def t1(username,password):
    psxmlgen = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                        '-ExecutionPolicy',
                        'Unrestricted',
                        './365ScriptPyhton.ps1',
                        username,password], cwd=os.getcwd())
    result = psxmlgen.wait()


def t2(username,password):
    psxmlgen = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                        '-ExecutionPolicy',
                        'Unrestricted',
                        './ruleFinderScript.ps1',
                        username, password], cwd=os.getcwd())
    result = psxmlgen.wait()

def t3():
    psxmlgen = subprocess.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                        '-ExecutionPolicy',
                        'Unrestricted',
                        './LogonAnalyzer.ps1',
                        ], cwd=os.getcwd())
    result = psxmlgen.wait()



