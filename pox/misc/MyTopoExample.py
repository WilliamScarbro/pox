from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.topology.topology import *
from pox.misc.MyTopology import *

log = core.getLogger()



class MyTopoInterface (object):
  """
  A Tutorial object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}


  def resend_packet (self, packet_in, out_port):
    """
    Instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in

    #log.debug("Forwarding %s to port %s"%(packet_in,out_port))

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)


  def act_like_hub (self, packet, packet_in):
    """
    Implement hub-like behavior -- send all packets to all ports besides
    the input port.
    """

    # We want to output to all ports -- we do that using the special
    # OFPP_ALL port as the output port.  (We could have also used
    # OFPP_FLOOD.)
    self.resend_packet(packet_in, of.OFPP_ALL)

    # Note that if we didn't get a valid buffer_id, a slightly better
    # implementation would check that we got the full data before
    # sending it (len(packet_in.data) should be == packet_in.total_len)).


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
   
    
    # interface with MyTopology

    # fetch topology component
    topology = core.components['topology']

    # if we haven't seen this host before
    if topology.getEntityByID(packet.src)==None:
      
      # add new host to POX topology
      new_host=Host(id=packet.src)
      log.debug("adding host %s" % new_host)
      topology.addEntity(new_host)
      
      # for the current switch:
      sw=topology.getEntityByID(event.dpid)
      log.debug("Current switch: %s" % sw)

      # check we are receiving on a known port
      if not packet_in.in_port in sw.ports:
        log.debug("%s unknown port %s"% (sw,packet_in.in_port))
      else:
        # get appropriate port from current switch
        port=sw.ports[packet_in.in_port]

        # check the port is not already connected
        if not port.entities:
          log.debug("adding host %s on port %s" % (new_host,port))
      
          # add new host to the appropriate port
          port.entities={new_host}
        else:
          log.debug("port %s already connected to %s" % (port,port.entities))

      mt=MyTopology(topology)
      #log.debug(mt.getSwitchAdjacency())
      #log.debug(mt.host_path_bandwidth())
      log.debug("Throughput: %s"% mt.throughput())
    
    self.act_like_hub(packet, packet_in)
    


def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    MyTopoInterface(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)

  topology = core.components['topology']
  topology.listenTo(core)

