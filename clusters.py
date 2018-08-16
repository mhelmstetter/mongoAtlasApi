import requests
from requests.auth import HTTPDigestAuth
import json
import argparse
import sys
import copy



def getClusters():
    response = requests.get(clustersEndpoint
            ,auth=HTTPDigestAuth(args.username,args.apiKey), verify=False)
    response.raise_for_status()
    return response.json()

def createCluster():
    if ( args.clusterTemplate == "-" ):
        data = sys.stdin.read()
    else:
        data = open( args.clusterTemplate, 'r').read()
    clusterTemplate = json.loads(data)

    response = requests.post(clustersEndpoint,
                auth=HTTPDigestAuth(args.username,args.apiKey),
                data=json.dumps(clusterTemplate),
                headers=headers,
                verify=False)

    print "Result %s %s" % (response.status_code,response.reason)

    if (response.status_code != requests.codes.created):
        print "ERROR %s %s" % (response.status_code,response.reason)
        print(response.headers)
        print(response.content)
    else:
        response.raise_for_status()


def getAll():

    config = getClusters()
    new_config = copy.deepcopy(config)

    configStr = json.dumps(new_config, indent=4)
    print(configStr)



#
# main
#

headers = { "Content-Type" : "application/json" }
disabled = { "enabled" : "false" }
enabled = { "enabled" : "true" }

requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser(description="Manage users from MongoDB Ops/Cloud Manager")

requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("--group"
        ,help='the OpsMgr group id'
        ,required=True)
requiredNamed.add_argument("--username"
        ,help='OpsMgr user name'
        ,required=True)
requiredNamed.add_argument("--apiKey"
        ,help='OpsMgr api key for the user'
        ,required=True)

actionsParser = parser.add_argument_group('actions')
actionsParser.add_argument("--getAll",dest='action', action='store_const'
        ,const=getAll
        ,help='Get all clusters')
actionsParser.add_argument("--createCluster",dest='action', action='store_const'
        ,const=createCluster
        ,help='Create a new cluster')


optionsParser = parser.add_argument_group('options')
optionsParser.add_argument("--clusterTemplate"
        ,help='Input file containing cluster template JSON or "-" for STDIN (default: cluster.json)'
        ,default="cluster.json")


args = parser.parse_args()

if args.action is None:
    parser.parse_args(['-h'])

# /api/atlas/v1.0/groups/{GROUP-ID}/databaseUsers
clustersEndpoint = "https://cloud.mongodb.com/api/atlas/v1.0/groups/" + args.group +"/clusters"

# based on the argument passed, this will call the "const" function from the parser config
# e.g. --disableAlertConfigs argument will call disableAlerts()
args.action()




