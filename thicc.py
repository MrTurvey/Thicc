import argparse
import psutil
import os
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--app", dest = "application", help="application name")
parser.add_argument("-Pe", "--PEnable", dest = "PEnable", help="Proxy Enable")
parser.add_argument("-Pd", "--PDisable", dest = "PDisable", help="Proxy Disable", action="store_true")
args = parser.parse_args()


class Processes():
    def getProcesses(appName):
        allIps = []
        allProcesses = psutil.process_iter()
        for Process in allProcesses:
            if appName in Process.name():
                procName = Process.name()
                allConnections = Process.connections("inet4")
                for connections in allConnections:
                    if connections.raddr:
                        if connections.raddr.ip != "127.0.0.1":
                            allIps.append(connections.raddr.ip)
        return allIps, procName
    
    def regCreate(allIps):
        createdRegex = []
        for theIPs in allIps:
            ipParts = theIPs.split('.')
            createdRegex.append("^"+ipParts[0]+"\."+ipParts[1]+"\."+ipParts[2]+"\."+ipParts[3]+"$")
        return createdRegex




if __name__ == "__main__":
    
    if args.application:
        FindApp = (Processes.getProcesses(args.application))
        allIps = FindApp[0]
        procName = FindApp[1]
        print ("\n ## Thicc - Your Thick App Testing Friend ## \n")
        print ("The process we are dealing with is " + procName +"\n")
        print ("Set these RegExes in Burpsuites Proxy > Options > TLS PassThrough options \n")
        print (*Processes.regCreate(allIps),sep='\n')
        print ("\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b")
        answer = input("\nDo you want to set burp as your system proxy? Y/N \n")
        if answer.lower() == "y":
            try:
                proxyAddr = input("\nEnter Burps Listener Address - Usually 127.0.0.1:8080 \n")
                os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyServer /t REG_SZ /d " + proxyAddr + " -f")
                os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 1 -f")
                print ("Proxy enabled and set to " + proxyAddr)
            except Exception as e:
                print ("\nYou need to run this as Admin to set a proxy")
                print ("\nOr just set the system proxy yourself to burps listener")
    if args.PEnable:
        os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyServer /t REG_SZ /d " + args.PEnable + " -f")
        os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 1 -f")
        print ("Proxy enabled and set to " + args.PEnable)
    if args.PDisable:
        os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 0 -f")



