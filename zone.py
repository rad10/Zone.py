#!/usr/bin/python
import json
from sys import argv, exit
import urllib
#[Intro Config Variables]#
errors = name = dns = check = soa = a = aaaa = detail = mx = cname = b = txt = False
url = ""
#[/Intro Config Variables]#
#[Help]#


def help():
    print("Zone.py [OPTION] [WEBSITE]")
    print("Zone.py is an application used to get information about a website with its headers. It uses the website zone.vision to get all of its information. it will not longer work if the api is no longer existing or no longer free.")
    print("\nOPTIONS:\n")
    print("--all\t\tWill give all available infomration on the given website. Gives the same result as running with every option.")
    print("-name\t\tReturns the name of the website.")
    print("-dns\t\tReturns all dns servers that name the given website.")
    print("-soa\t\tReturns important information including the primary server and its serial number")
    print("-a\t\tReturns all IPv4 Authoritative servers with their ip addresses")
    print("-aaaa\t\tReturns all IPv6 Authoritative servers with their ipv6 addresses, if there are any")
    print("-mx\t\tReturns all mailing servers for the given website")
    print("-cname\t\tReturns the cname for the website")
    print("\nADDITIONAL OPTIONS:\n")
    print("-b\t\tReturns true or false whether or not the requested records are present. it prints true/false multiple times in order of first possible option to last.")
    print("  --detail\tReturns details of which specific records are present")
    print("-h/-help/--help\tReturns the help page")
    exit()


#[/Help]#
#[Config]#
for i in argv[1:]:  # grabs all args - zone.py
    if (i == "--all"):
        errors = name = dns = check = soa = a = aaaa = detail = mx = cname = True
    elif (i == "-name"):
        name = True
    elif (i == "-dns"):
        dns = True
    elif (i == "-check"):
        check = True
    elif (i == "-soa"):
        soa = True
    elif (i == "-a"):
        a = True
    elif (i == "-aaaa"):
        aaaa = True
    elif (i == "--detail"):
        detail = True
    elif (i == "-mx"):
        mx = True
    elif (i == "-cname"):
        cname = True
    elif (i == "-b"):
        b = True
    elif (i == "-txt"):
        txt = True
    elif (i == "-h" | i == "-help" | i == "--help"):
        help()
    elif (i[0] == "-"):
        print("Incorrect Command\n")
        help()
        exit()
    else:
        if (i[0:7] == "http://"):
            url = i[7:]
        elif (i[0:8] == "https://"):
            url = (i[8:])
        else:
            url = i
if(url == ""):
    print("Error: no website inputed. please input a website.\n")
    help()
    exit()
#[/Config]#
#[Import JSON info from site]#
try:
    sock = urllib.urlopen("http://api.zone.vision/"+url)
    jsonSite = sock.read()
    sock.close()
    #[/Import JSON from site]#
    jsonData = json.loads(jsonSite)  # Turn JSON into usable data
except:
    print("Error: cannot connect to site")
    exit()
#[Generator]#
if errors:
    print("Errors: "+str(jsonData["errors"]))
if name:
    print("url: "+str(jsonData["name"]))
#[Naming Servers]#
if dns:
    print("Naming Servers:")
    print("IPv4:")
    if(str(jsonData["parent"]["glue"]["v4"]) == "None"):
        print("+None")  # if theres no record, itll display it as no record
    else:
        for i in jsonData["parent"]["glue"]["v4"]:  # lists every server that uses ipv6
            print("+Name: "+i["name"])  # lists the name
            print("+Address: "+i["address"])  # lists the address
    print("IPv6:")
    if (str(jsonData["parent"]["glue"]["v6"]) == "None"):
        print("+None\n")  # if theres no record, itll display it as no record
    else:
        for i in jsonData["parent"]["glue"]["v6"]:  # lists every server that uses ipv6
            print("+name: "+i["name"])  # lists the name
            print("+Address: "+i["address"])  # lists the address
        print("")
#[/Naming Servers]#
#[SOA]#
if soa:
    total = 0  # holds tally for all servers that say true
    size = 0  # tallys all servers, true or not
    for i in jsonData["diagnostics"]["results"][6]["sources"]:
        if jsonData["diagnostics"]["results"][6]["sources"][i]:
            total = total+1
        size = size+1
    if b:  # Only enacts if the program requests a boolean with -b
        if detail:  # This setting allows to get details on subject
            if (total == size):
                print("All SOA Records are present")
            else:
                print("Not all SOA Records are present")
            for i in jsonData["diagnostics"]["results"][6]["sources"]:
                # goes through all servers and sends the name and the info bound to the server name
                print(i+": "+str(jsonData["diagnostics"]
                                 ["results"][6]["sources"][i]))
        else:
            if (total == size):
                # this side of script just gives true or false for automation
                print(True)
            else:
                print(False)
    else:
        if (total == size):
            print("All SOA Records are present")
            # used to select all sources possible
            for i in range(0, len(jsonData["authoritative"]["soa"])):
                print(jsonData["authoritative"]["soa"][i]
                      ["source"])  # Prints the server name
                # Prints the websites name
                print(
                    "+Name: "+str(jsonData["authoritative"]["soa"][i]["records"][0]["name"]))
                print("+Primary Server: " +
                      str(jsonData["authoritative"]["soa"][i]["records"][0]["mname"]))
                print("+Responsible Party: " +
                      str(jsonData["authoritative"]["soa"][i]["records"][0]["rname"]))
                print("+Serial Number: " +
                      str(jsonData["authoritative"]["soa"][i]["records"][0]["serial"]))
            print("")
        else:
            # Will only print this is there no record info to be found
            print("There is no SOA Record info available\n")
#[/SOA]#
#[A]#
if a:
    total = 0  # holds tally for all servers that say true
    size = 0  # tallys all servers, true or not
    for i in jsonData["diagnostics"]["results"][7]["sources"]:
        if jsonData["diagnostics"]["results"][7]["sources"][i]:
            total = total+1
        size = size+1
    if b:  # Only enacts if the program requests a boolean with -b
        if detail:  # This setting allows to get details on subject
            if (total == size):
                print("All A Records are present")
            else:
                print("Not all A Records are present")
            for i in jsonData["diagnostics"]["results"][7]["sources"]:
                # goes through all servers and sends the name and the info bound to the server name
                print(i+": "+str(jsonData["diagnostics"]
                                 ["results"][7]["sources"][i]))
        else:
            if (total == size):
                # this side of script just gives true or false for automation
                print(True)
            else:
                print(False)
    else:
        if (total == size):
            print("All A Records are present")
            # used to select all sources possible
            for i in range(0, len(jsonData["authoritative"]["a"])):
                print(jsonData["authoritative"]["a"][i]
                      ["source"])  # Prints the server name
                # Prints the websites name
                print(
                    "+Name: "+str(jsonData["authoritative"]["a"][i]["records"][0]["name"]))
                # Prints the info given
                print(
                    "+Address: "+str(jsonData["authoritative"]["a"][i]["records"][0]["address"]))
            print("")
        else:
            # Will only print this is there no record info to be found
            print("There is no A Record info available\n")
#[/A]#
#[AAAA]#
if aaaa:
    total = 0  # holds tally for all servers that say true
    size = 0  # tallys all servers, true or not
    for i in jsonData["diagnostics"]["results"][8]["sources"]:
        if jsonData["diagnostics"]["results"][8]["sources"][i]:
            total = total+1
        size = size+1
    if b:  # Only enacts if the program requests a boolean with -b
        if detail:  # This setting allows to get details on subject
            if (total == size):
                print("All AAAA Records are present")
            else:
                print("Not all AAAA Records are present")
            for i in jsonData["diagnostics"]["results"][8]["sources"]:
                # goes through all servers and sends the name and the info bound to the server name
                print(i+": "+str(jsonData["diagnostics"]
                                 ["results"][8]["sources"][i]))
        else:
            if (total == size):
                # this side of script just gives true or false for automation
                print(True)
            else:
                print(False)
    else:
        if (total == size):
            print("All AAAA Records are present")
            # used to select all sources possible
            for i in range(0, len(jsonData["authoritative"]["aaaa"])):
                print(jsonData["authoritative"]["aaaa"][i]
                      ["source"])  # Prints the server name
                # Prints the websites name
                print(
                    "+Name: "+str(jsonData["authoritative"]["aaaa"][i]["records"][0]["name"]))
                # Prints the info given
                print(
                    "+Address: "+str(jsonData["authoritative"]["aaaa"][i]["records"][0]["address"]))
            print("")
        else:
            # Will only print this is there no record info to be found
            print("There is no AAAA Record info available\n")
#[/AAAA]#
#[MX]#
if mx:
    total = 0  # holds tally for all servers that say true
    size = 0  # tallys all servers, true or not
    for i in jsonData["diagnostics"]["results"][9]["sources"]:
        if jsonData["diagnostics"]["results"][9]["sources"][i]:
            total = total+1
        size = size+1
    if b:  # Only enacts if the program requests a boolean with -b
        if detail:  # This setting allows to get details on subject
            if (total == size):
                print("All MX Records are present")
            else:
                print("Not all MX Records are present")
            for i in jsonData["diagnostics"]["results"][9]["sources"]:
                # goes through all servers and sends the name and the info bound to the server name
                print(i+": "+str(jsonData["diagnostics"]
                                 ["results"][9]["sources"][i]))
        else:
            if (total == size):
                # this side of script just gives true or false for automation
                print(True)
            else:
                print(False)
    else:
        if (total == size):
            print("All MX Records are present")
            # used to select all sources possible
            for i in range(0, len(jsonData["authoritative"]["mx"])):
                print(jsonData["authoritative"]["mx"][i]
                      ["source"])  # Prints the server name
                # Prints the websites name
                print(
                    "+Name: "+str(jsonData["authoritative"]["mx"][i]["records"][0]["name"]))
                # Prints the info given
                print(
                    "+Address: "+str(jsonData["authoritative"]["mx"][i]["records"][0]["exchange"]))
            print("")
        else:
            # Will only print this is there no record info to be found
            print("There is no MX Record info available\n")
#[/MX]#
#[CNAME]#
if cname:
    total = 0  # holds tally for all servers that say true
    size = 0  # tallys all servers, true or not
    for i in jsonData["diagnostics"]["results"][10]["sources"]:
        if jsonData["diagnostics"]["results"][10]["sources"][i]:
            total = total+1
        size = size+1
    if b:  # Only enacts if the program requests a boolean with -b
        if detail:  # This setting allows to get details on subject
            if (total == size):
                print("All CNAME Records are present")
            else:
                print("Not all CNAME Records are present")
            for i in jsonData["diagnostics"]["results"][10]["sources"]:
                # goes through all servers and sends the name and the info bound to the server name
                print(i+": "+str(jsonData["diagnostics"]
                                 ["results"][10]["sources"][i]))
        else:
            if (total == size):
                # this side of script just gives true or false for automation
                print(True)
            else:
                print(False)
    else:
        if (total == size):
            print("All CNAME Records are present")
            # used to select all sources possible
            for i in range(0, len(jsonData["authoritative"]["cname"])):
                print(jsonData["authoritative"]["cname"][i]
                      ["source"])  # Prints the server name
                # Prints the websites name
                print(
                    "+Name: "+str(jsonData["authoritative"]["cname"][i]["records"][0]["name"]))
                # print("+Address: "+str(jsonData["authoritative"]["cname"][i]["records"][0]["address"])) #Prints the info given
            print("")
        else:
            # Will only print this is there no record info to be found
            print("There is no CNAME Record info available\n")
#[/CNAME]#
#[/Generator]#
