from blocks.wire import Wire
from blocks.activator import Activator
from blocks.NOT import NOT
from blocks.logic_gate import LogicGate
from blocks.armored_wire import ArmoredWire
from blocks.diode import Diode
from blocks.output import Output
from blocks.wire_box import WireBox
from blocks.memory import Memory
from blocks.sensor import Sensor
from blocks.energy_block import EnergyBlock
from blocks.button_block import ButtonBlock
from blocks.piston import Piston
from blocks.brick import Brick
from blocks.piston_head import PistonHead
from blocks.no_pushable import NoPushable
from blocks.air import Air
from blocks.block import *

def get_block(world, pos, type, glassed=0, data=None):
    if type == "air":
        return(Air(world, pos, glassed, data))
    elif type == "block":
        return(Brick(world, pos, glassed, data))
    elif type == "wire":
        return(Wire(world, pos, glassed, data))
    elif type == "activator":
        return(Activator(world, pos, glassed, data))
    elif type == "NOT":
        return(NOT(world, pos, glassed, data))
    elif type == "XOR" or type == "AND":
        return(LogicGate(world, pos, type, glassed, data))
    elif type == "armored wire":
        return(ArmoredWire(world, pos, glassed, data))
    elif type == "diode":
        return(Diode(world, pos, glassed, data))
    elif type == "output":
        return(Output(world, pos, glassed, data))
    elif type == "wire box":
        return(WireBox(world, pos, glassed, data))
    elif type == "memory":
        return(Memory(world, pos, glassed, data))
    elif type == "sensor":
        return(Sensor(world, pos, glassed, data))
    elif type == "energy block":
        return(EnergyBlock(world, pos, glassed, data))
    elif type == "button":
        return(ButtonBlock(world, pos, glassed, data))
    elif type == "piston" or type == "sticky piston":
        return(Piston(world, pos, type, glassed, data))
    elif type == "piston head":
        return(PistonHead(world, pos, glassed, data))
    elif type == "no pushable":
        return(NoPushable(world, pos, glassed, data))
    return(Block(world, pos, type, glassed, data))

def get_block_params(type):
    if type == "wire":
        return({"activated" : 0})
    elif type == "activator":
        return({"activated" : 0})
    elif type == "NOT":
        return({"activated1" : 0, "activated" : 0, "rotate" : 0})
    elif type == "XOR" or type == "AND":
        return({"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0})
    elif type == "armored wire":
        return({"activated": 0, "connections" : [0, 0, 0, 0]})
    elif type == "diode":
        return({"activated1": 0, "activated2": 0, "rotate" : 0})
    elif type == "output":
        return({"activated" : 0, "rotate" : 0})
    elif type == "wire box":
        return({"activated1" : 0, "activated2" : 0})
    elif type == "memory":
        return({"activated1" : 0, "activated2" : 0, "activated" : 0, "rotate" : 0, "inverted" : 0})
    elif type == "sensor":
        return({"activated" : 0, "rotate" : 0})
    elif type == "energy block":
        return({"activated" : 1})
    elif type == "button":
        return({"activated" : 0})
    elif type == "piston" or type == "sticky piston":
        return({"activated" : 0, "rotate" : 0, "power" : 12})
    elif type == "piston head":
        return({"rotate": 0, "sticky" : 0})
    else:
        return({})