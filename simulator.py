from sys import argv
import pprint
import collections


# read in topology file, store into list
# instanciate each node obj and store into network dictionary
# begin simulation on the network
# test for network convergence each round and exit when convergence is determined
# prompt user for path testing
# display path along network
class Node:
    def __init__(self, name):
        self.name = name
        self.RT = {}
        self.outB = {}
        self.inB = []
        self.neighborList = []
        self.conv = False

    def printData(self):
        nodeObj = {"name": self.name,
                   "RT": self.RT,
                   "outB": self.outB,
                   "inB": self.inB,
                   "neighborList": self.neighborList,
                   "conv?": self.conv}
        return nodeObj

    def rtMasterUpdate(self):
        pass


def topoRead():
    # fname = "topology.txt"
    fname = None
    rounds = None
    # print(len(argv))
    if len(argv) > 2:
        fname = argv[1]
        rounds = argv[2]
    else:
        print("Input Error")
        exit(-1)

    with open(fname, 'r') as f:
        topo = [l.split() for l in f]

    # print(fname, rounds, topo, sep='\n')

    return topo, rounds


def RTUpdate(nodeobj, dest, cost, nexthop):
    rtDict = {}
    curDict = nodeobj.RT
    if dest not in curDict or not bool(curDict):
        # create table entry
        rtDict = {"cost": cost, "nexthop": nexthop}
        nodeobj.RT[dest] = rtDict
        return nodeobj
    else:
        # key is there compare the cost between old and new
        oldCost = curDict[dest]["cost"]
        newCost = cost
        if newCost > oldCost:
            rtDict = {"cost": cost, "nexthop": nexthop}
            nodeobj.RT[dest].update(rtDict)
            return nodeobj
        else:
            print(oldCost, " is cheaper than ", newCost)
            return nodeobj
            # use this none to catch weather or not the dictionary was updated


def createNode(net, edge, nodelist):
    n1, n2, cost = tuple(edge)
    cost = int(cost)
    print(n1, n2, cost, edge, sep="\n")

    # Create Nodes
    if n1 in nodelist:
        node1 = net[n1]
        pass
    else:
        # create node 1
        node1 = Node(n1)
        nodelist.append(n1)
        pass

    if n2 in nodelist:
        node2 = net[n2]
        pass
    else:
        # create node 2
        node2 = Node(n2)
        nodelist.append(n2)
        pass

    # Update Node1 RT, and neighbors
    node1.neighborList.append(n2)
    nodeNew = RTUpdate(node1, dest=n2, cost=cost, nexthop=n2)
    if nodeNew is None:
        pass
    else:
        node1 = nodeNew

    # Update Node2 RT, and neighbors
    node2.neighborList.append(n1)
    nodeNew = RTUpdate(node2, dest=n1, cost=cost, nexthop=n1)
    if nodeNew is None:
        pass
    else:
        node2 = nodeNew

    # add the objects to the Network

    net[n1] = node1
    net[n2] = node2

    return net, nodelist


def sendDV(net, n, nodelist):
    return net


def main():
    net = {}
    nodelist = []
    convYes = []
    convNo = []
    topo, rounds = topoRead()
    # initialize network nodes with starting values
    for l in topo:
        # print(l)
        net, nodelist = createNode(net, l, nodelist)
        # print(net, nodelist, sep="\n")
    for c in net:
        print("\n", "NODE:", c)
        pprint.pprint(net[c].printData(), width=1, )

    # SIMULATION START
    convNo = nodelist
    for r in range(1, int(rounds) + 1):
        print("\n\n***ROUND: ", r)
        # build DV packets
        for n in net:
            print("\n", "DV PACKET NODE:", n)
            net[n].outB = net[n].RT
            pprint.pprint(net[n].outB)
            # send DV packets
        for n in net:
            net = sendDV(net, n, nodelist)
            # Have each Node update Master RT
        for n in net:
            net[n].rtMasterUpdate()
            # test for overall convergence
        if set(convYes) == set(nodelist):
            print("NETWORK HAS CONVERGED ON ROUND ", r)
            return

    print("\n\nSIMULATION OVER")
    return


if __name__ == '__main__':
    main()
