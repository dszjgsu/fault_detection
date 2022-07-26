import sys
sys.path.insert(0, "..")
import logging
import time

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client
from opcua import ua


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    client = Client("opc.tcp://LAPTOP-AHKF6CEM:53530/OPCUA/SimulationServer")
    try:
        client.connect()
        client.load_type_definitions()  # load definition of server specific structures/extension objects

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Root is: ", root)
        print("Root node is: ", root.get_children()[0].get_children())
        objects = client.get_objects_node()
        print("Objects node is: ", objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())
        # print("Children of objects are: ", objects.get_child(85))

        # get a specific node knowing its node id
        # var22 = client.get_node(ua.NodeId(1002, 3))
        var = client.get_node("ns=3;i=1002")
        # ns为第几个namespace， 后面的s为你寻找参数的路径
        print("get a specific node knowing its node id: ", var.get_value())
        #var = client.get_node("ns=2;g=1be5ba38-d004-46bd-aa3a-b5b87940c698")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # gettting our namespace idx
        # uri = "http://examples.freeopcua.github.io"
        # uri = "http://www.prosysopc.com/OPCUA/SimulationNodes/ "
        # uri = "http://opcfoundation.org/UA/"
        # uri = "urn:host.docker.internal:OPCUA:SimulationServer"
        uri = "http://www.prosysopc.com/OPCUA/SimulationNodes/"
        idx = client.get_namespace_index(uri)
        print("idx: ", idx)
        # Now getting a variable node using its browse path
        # myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])
        myvar = root.get_child(["0:Objects"]).get_child(["3:Simulation"]).get_child(["3:Counter"])
        print("myvar is: ", myvar)
        # obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])

        # subscribing to a variable node
        # handler = SubHandler()
        # sub = client.create_subscription(500, handler)
        # handle = sub.subscribe_data_change(myvar)
        # time.sleep(0.1)

        # we can also subscribe to events from server
        # sub.subscribe_events()
        # sub.unsubscribe(handle)
        # sub.delete()

        # calling a method on server
        # res = obj.call_method("{}:multiply".format(idx), 3, "klk")
        # print("method result is: ", res)

        # embed()
    finally:
        client.disconnect()