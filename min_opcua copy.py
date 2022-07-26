import sys
sys.path.insert(0, "..")


from opcua import Client


if __name__ == "__main__":

    # client = Client("opc.tcp://LAPTOP-AHKF6CEM:53530/OPCUA/SimulationServer")
    client = Client("opc.tcp://host.docker.internal:53530/OPCUA/SimulationServer")
    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        var = client.get_node("ns=3;i=1002")
        # ns为第几个namespace， 后面的s为你寻找参数的路径
        print("get a specific node knowing its node id: ", var.get_value())

        myobj = root.get_child(["0:Objects"]).get_child(["3:Simulation"]).get_child(["3:Counter"])
        print("myobj is: ", myobj)
        myval = root.get_child(["0:Objects"]).get_child(["3:Simulation"]).get_child(["3:Counter"]).get_value()
        print("myval is: ", myval)

    finally:
        client.disconnect()
