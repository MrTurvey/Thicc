import argparse
from asyncio.windows_events import NULL
import psutil
import os
parser = argparse.ArgumentParser()
parser.add_argument("-a", dest = "application", help="Generate Burp Suite settings for Thick App test")
parser.add_argument("-Pe", dest = "PROXY", help="Enable Proxy. e.g 127.0.0.1:8080")
parser.add_argument("-Pd", dest = "PDisable", help="Disable Proxy", action="store_true")
parser.add_argument("-L", dest = "AllProcess", help="Show All Processes", action="store_true")
parser.add_argument("-S", dest = "Process", help="Search Processes")
args = parser.parse_args()


class Processes():
    def allProcesses():
        theProcessesList = psutil.process_iter()
        return theProcessesList
    
    def searchProcesses(appName):
        procName = "NotFound"
        allNames = []
        allProcesses = psutil.process_iter()
        for Process in allProcesses:
            if appName.lower() in Process.name().lower():
                if Process.name().lower() not in allNames:
                    allNames.append(Process.name().lower())
        return allNames

    def getProcesses(appName):
        procName = []
        allIps = []
        allProcesses = psutil.process_iter()
        tooManyProcs = 0
        for Process in allProcesses:
            if appName.lower() in Process.name().lower():
                if Process.name().lower() not in procName:
                    if len(procName) == 0:
                        procName.append(Process.name().lower())
                        allConnections = Process.connections("inet4")
                        for connections in allConnections:
                            if connections.raddr:
                                if connections.raddr.ip != "127.0.0.1":
                                    if connections.raddr.ip not in allIps:
                                        allIps.append(connections.raddr.ip)
                    else:
                        if Process.name().lower() not in procName:
                            procName.append(Process.name().lower())
                            tooManyProcs = 1
                else:
                    allConnections = Process.connections("inet4")
                    for connections in allConnections:
                        if connections.raddr:
                            if connections.raddr.ip != "127.0.0.1":
                                if connections.raddr.ip not in allIps:
                                    allIps.append(connections.raddr.ip)
                                             
        return allIps, procName, tooManyProcs
    
    def regCreate(allIps):
        createdRegex = []
        for theIPs in allIps:
            ipParts = theIPs.split('.')
            createdRegex.append("^"+ipParts[0]+"\."+ipParts[1]+"\."+ipParts[2]+"\."+ipParts[3]+"$")
        return createdRegex

class main():
    if args.application:
        FindApp = (Processes.getProcesses(args.application))
        allIps = FindApp[0]
        procName = FindApp[1]
        tooManyProcs = FindApp[2]
        if tooManyProcs != 1:
            if allIps:
                print ("\nThe process we are dealing with is " + procName[0] +"\n")
                print ("Set this RegEx in the Burp Suites Proxy > Options > TLS PassThrough options \n")
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
            else:
                print ("No external IPs have been detected for " + procName[0])
        else:
            print ("Specific service/app not found. Be more specific with one of these that were found?\n")
            for pName in procName:
                print (pName)

    if args.PROXY:
        try:
            os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyServer /t REG_SZ /d " + args.PEnable + " -f")
            os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 1 -f")
            print ("Proxy enabled and set to " + args.PEnable)
        except Exception as e:
            print ("\nYou need to run this as Admin to set a proxy")
            print ("\nOr just set the system proxy yourself to burps listener")
    if args.PDisable:
        try:
            os.system("reg add \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\" /v ProxyEnable /t REG_DWORD /d 0 -f")
        except Exception as e:
            print ("\nYou need to run this as Admin to disable the proxy")
    if args.AllProcess:
        ProcList = []
        allProcesses = psutil.process_iter()
        for Process in allProcesses:
            if Process.name() not in ProcList:
                ProcList.append(Process.name())
        print ("The running process on your host are: \n")
        for all in ProcList:
            print (all)
    if args.Process:
        allProcessNames = Processes.searchProcesses(args.Process)
        print ("\nThe processes that match " + args.Process + " are: \n")
        for name in allProcessNames:
            print (name)



if __name__ == "__main__":
    main()



