#!/usr/bin/python

import re
import time
import datetime
import threading
import sys
import random
import copy
from xml.dom.minidom import parseString
from optparse import OptionParser
import pydb
import matplotlib.pyplot as plt
import subprocess
import csv
#import pystuck
import os
import re


##########################################################
# Thermal Registers
##########################################################

class bit_defn:
	def __init__(self, bit_start, bit_end):
			length = bit_end - bit_start + 1 
			tmask = 0
			for i in range(length):
				tmask = tmask | (1 << i)
			self.bit_mask = tmask
			self.bit_start = bit_start
			self.bit_end = bit_end
	def get_value(self, value):
		temp_value = (value&self.bit_mask) << self.bit_start
		return temp_value
	def get_bitmask(self):
		return self.bit_mask
#
# Register definition for MEMORY_THROTTLE_CONTROL register
#
class throttle_apply_safe:
	enable  = 1
	disable = 0

class throttle_mode:
	disabled  = 0x0
	open_loop = 0x1
	closed_loop = 0x2 #Throttle when MC_CLOSED_LOOP.THROTTLE_NOW is set.
	closed_loop_v2 = 0x3 #Throttle when MC_DDR_THERM_COMMAND.THROTTLE is set
						 #and the MC_DDR_THERM pin is asserted OR OLTT will be implemented

class REG_MEMORY_THROTTLE_CONTROL:
	def __init__(self):
		#bits 0 - 1
		self.apply = throttle_apply_safe.disable
		self.apply_bitdefn = bit_defn(0, 1)
		#bit 2
		self.mode = throttle_mode.disabled
		self.mode_bitdefn = bit_defn(2,2)

	def set_mode(self, mode):
		self.mode = mode;
	def set_apply_safe(self, enable):
		self.apply = enable
	def get_reg(self):
		value = self.mode_bitdefn.get_value(self.mode)|\
				self.apply_bitdefn.get_value(self.apply)
		return value
	def reset_reg(self):
		self.apply = throttle_apply_safe.disable
		self.mode = throttle_mode.disabled

	def display(self):
		print "MEMORY_THROTTLE_CONTROL = ",hex(self.get_reg())

#
# Register definition for MC_CLOSED_LOOP register
#

class throttle_now:
	disable = 0
	enable  = 0xf

class ref_2x_now:
	disable = 0
	enable  = 1

#Platform specific values
class duty_cycle:
	max = 1023
	min = 1 

class REG_MC_CLOSED_LOOP:
	def __init__(self):
		#bits 0:4
		self.tnow = throttle_now.disable;
		self.tnow_bitdefn = bit_defn(0, 3)
		#bits 4
		self.r2xnow = ref_2x_now.disable
		self.r2xnow_bitdefn = bit_defn(4,4)
		#bits 8 : 17
		self.duty_cycle = 0
		self.duty_cycle_bitdefn = bit_defn(8, 17)

	def en_throttle_now(self):
		self.tnow = throttle_now.enable
	def dis_throttle_now(self):
		self.tnow = throttle_now.disable
	def set_duty_cycle(self, value):
		self.duty_cycle = value&self.duty_cycle_bitdefn.get_bitmask()
	def get_duty_cycle_min_max(self):
		return 64, 1023 #platform specific parameters
	def get_reg(self):
		value = self.tnow_bitdefn.get_value(self.tnow)| \
				self.r2xnow_bitdefn.get_value(self.r2xnow)| self.duty_cycle_bitdefn.get_value(self.duty_cycle)
		return value
	def reset_reg(self):
		self.tnow = throttle_now.enable
		self.duty_cycle = 0x40&self.duty_cycle_bitdefn.get_bitmask()

	def display(self):
		print "MC_CLOSED_LOOP = ",hex(self.get_reg())

#
# Memory Throttler Core class
#
class reg_offset:
	MEMORY_THROTTLE_CONTROL = 0x48
	MC_CLOSED_LOOP			= 0x84

class mem_throttler:
	def __init__(self, node, pci_id):
		self.pci_id = pci_id
		self.node   = node
		self.ctrl = REG_MEMORY_THROTTLE_CONTROL()
		self.loop = REG_MC_CLOSED_LOOP()
	def getPCIID(self):
		return self.pci_id

	def progpci(self):
		#program MC_CLOSED_LOOP
		os.system("setpci -s "+ self.pci_id + " " + str(hex(reg_offset.MC_CLOSED_LOOP)) +".L="+str(hex(self.loop.get_reg())))
		#program MEMORY_THROTTLE_CONTROL
		os.system("setpci -s "+ self.pci_id + " " +  str(hex(reg_offset.MEMORY_THROTTLE_CONTROL)) +".L="+str(hex(self.ctrl.get_reg())))

	#Throttles to a given duty cycle as represetned by value
	def throttle(self, value):
		#setup MC_CLOSED_LOOP
		self.loop.en_throttle_now()
		self.loop.set_duty_cycle(value)
		#setup MEMORY_THROTTLE_CONTROL
		self.ctrl.set_apply_safe(throttle_mode.closed_loop)
		#program PCI registers to throttle
		self.progpci()

	#disables throttling totally
	def dethrottle(self):
		self.loop.reset_reg()
		self.ctrl.reset_reg()
		self.progpci()

	def display(self):
		print "Numa Node = ", self.node, "PCI ID = ",self.pci_id
		self.ctrl.display()
		self.loop.display()

############################################################
# Display Methods
############################################################
def display_throttle_device(device_list):
	print "PCI device list that supports thermal throttling"
	for dev in device_list:
		print dev

def display_per_node_throttle_devices(node_dict):
	print "PCI Throttle Device ID's"
	nodenum = 0
	for node in node_dict:
		print "NUMA Node : ", nodenum
		for device in node_dict[node]:
			print "\tPCI_ID: ", device
		nodenum += 1
def display_reg_details(reg_list):
	for reg in reg_list:
		reg.display()

#Note: speeds must be sent in the sorted order
def display_ddr_bw(speed_list):
	node = 0
	for speed in speed_list:
		print "Node#", node, " =", speed," MBPS"
		node = node +1 

def display_ddr_throttle_values(node_throt_dict):
	#pydb.set_trace()
	for nid in node_throt_dict:
		print "Numa Node# ",nid
		for tlvl in node_throt_dict[nid]:
				print "\tThrottle Level = ", str(tlvl)+"x"
				print "\t\tDuty Cycle = ", hex(node_throt_dict[nid][tlvl][0])
				print "\t\tComputed Speed in MBPS = ", node_throt_dict[nid][tlvl][1]


################################################################
# Utility Methods
################################################################

#Method that scans PCI devices and detects the throttling devices
def parseoutput(output, string, string1):
	opsample = output.split("\n");
	oplist = []
	for op in opsample:
		if re.search(string, op) :
			if string1 :
				if re.search(string1, op):
					oplist.append(op)
			else:
				oplist.append(op)
	return oplist


#Method looks at the PCI device 
def get_pernode_throttle_dev(device_list):
	node_dict = dict()
	#pydb.set_trace()
	for dev in device_list:
		dump = dev.split(":")
		devfn = int(dump[0], 16)
		if devfn in node_dict:
			node_dict[devfn].append(dev)
		else:
			node_dict[devfn] = [dev]
	return node_dict


#returns speed in MBPS
def compute_ddrbw(memnode):
	#pydb.set_trace()
	#op = subprocess.check_output(["numactl --membind="+str(memnode), " ./stream_c.exe"])
	os.system("numactl --membind="+str(memnode)+" ./stream_c.exe > dump.txt")
	f = open("dump.txt",'r')
	op = f.read()
	f.close()
	os.system("rm dump.txt")
	slist = parseoutput(op, "Copy:", "")
	params = slist[0].split(" ")
	#print params
	speed = 0
	#pydb.set_trace()
	for i in range(1, len(params)):
		if params[i]:
			speed = float(params[i])
			break
	#print speed 
	return speed

#
#get_throttle_factor : Interface to determiny duty cycle 
# nid => Numa node #, start from 0
# thrtl_lvl => throttle levels supported
# reg => mem_throttler register object list
# node => pci device id lists for gven nid
# maxspeed => max speed without throttling on node "nid
#
def get_throttle_factor(nid, thrtl_lvl, reg, node, maxspeed):
	#Throttle dictionary performs following
	throttle_dict = dict()
	# we will scan it for each throttle level
	#pydb.set_trace()
	for lvl in thrtl_lvl:
		#we will iterate from max to min in a binary manner
		max = duty_cycle.max
		min = duty_cycle.min
		loop = 1
		target = maxspeed/float(lvl)
		error = sys.maxint
		prev_error = sys.maxint
		tcycle = min
		tspeed = 0
		while ((max - min) > 1)  :
			cycle = (min + max)/2
			for dev in reg:
				dev.throttle(cycle)
			newspeed = float(compute_ddrbw(nid))
			diff = abs(target - newspeed)
			if(error > diff) :
				tcycle = cycle
				error = diff
				tspeed = newspeed
			if(target > newspeed):
				min = cycle
			else:
				max = cycle
		#pydb.set_trace()
		tlist = [tcycle, tspeed]
		throttle_dict[lvl] = tlist

	return throttle_dict

def get_throttle_params(node_dict, thrtl_lvl):
	#create a throttle dictionary
	reg_dict = dict()
	#create throttle objects
	nodeid = 0
	#pydb.set_trace()
	for node in node_dict:
		tlist = []
		for device in node_dict[node]:
			reg = mem_throttler(nodeid, device)
			tlist.append(reg)
		reg_dict[nodeid] = tlist
		nodeid = nodeid + 1
	#reset the throttling
	for regsd in reg_dict:
		for reg in reg_dict[regsd]:
			reg.dethrottle()
	
	#1. First compute default speed for each node
	maxspeed = []
	for i in range(len(node_dict)):
		maxspeed.append(float(compute_ddrbw(i)))
	print "Maximum Bandwidth computed using stream_c.exe"
	display_ddr_bw(maxspeed)

	#2. let's try to throttle node 1
	#display_reg_details(reg_dict[1])
	#for reg in reg_dict[1]:
	#	reg.throttle(0x3ff)

	#3. check updated speed
	#newspeed = []
	#for i in range(len(node_dict)):
	#	newspeed.append(float(compute_ddrbw(i)))
	#print "After Throttling"
	#display_ddr_bw(newspeed)

	#Let's get fine tuned parameter
	# node -> throtle dictiorary
	#pydb.set_trace()
	node_throt_dict = dict()
	nid = 0
	for node in node_dict:
		#throt_dict => throttle factor -> cycle factor
		print "Computing for node# ", nid
		throt_dict = get_throttle_factor(nid, thrtl_lvl, reg_dict[nid], node_dict[node], maxspeed[nid])
		node_throt_dict[nid] = throt_dict
		nid = nid + 1

	#4. Restore back
	#pydb.set_trace()
	for regsd in reg_dict:
		for reg in reg_dict[regsd]:
			reg.dethrottle()
	display_ddr_throttle_values(node_throt_dict)

	#newspeed = []
	#for i in range(len(node_dict)):
	#	newspeed.append(float(compute_ddrbw(i)))
	#print "After dethrottling"
	#display_ddr_bw(newspeed)

def scan_throttledevices():
	#1. Scan pci devices to find out throttling devices
	op = subprocess.check_output(["lspci"])

	#parse the output
	devlist = parseoutput(op, "Integrated Memory Controller", "Thermal Control")
	throttle_pci_list = []
	#pydb.set_trace()
	
	for dev in devlist:
		dump = dev.split(" ")
		throttle_pci_list.append(dump[0])
	
	#display_throttle_device(throttle_pci_list)
	node_dict = get_pernode_throttle_dev(throttle_pci_list)
	display_per_node_throttle_devices(node_dict)
	#Now we need to train and get list of possible options
	throttle_level = [2, 5, 7, 9, 10]
	get_throttle_params(node_dict, throttle_level)

def parse_configuration_file(options):
	#pydb.set_trace()
	cfg = open(options.cfg_file, "r")
	trained = open(options.trained_file, "a+")
	trained.seek(0, 0)
	throttle_level = []
	node_id = []
	maxspeed = []

	#load the configuration files
	for line in cfg:
		#skip lines with comments
		if line[0] == '#':
			continue
		params = line.strip()
		params = params.split(":")
		conf = params[0].strip()
		if conf == "Throttling Factor":
			numfactors = params[1].split(",")
			for i in range(len(numfactors)):
				throttle_level.append(int(numfactors[i].strip()))
		elif conf == "Nodes":
			numfactors = params[1].split(",")
			for i in range(len(numfactors)):
				node_id.append(int(numfactors[i].strip()))
	#now popuate the trained map
	node_throt_dict = dict()
	nodeparse = 0
	lvl = -1
	throt_dict = []
	#create as many dictionaries as nodes
	for node in node_id: # 
		throt_dict.append(dict())
		maxspeed.append(0.0)

	throt_list = []
	pciid_tree = dict()
	nid = -1
	#pydb.set_trace()
	for line in trained:
		#skip lines with comments
		#print line
		if (line[0] == '#') or (len(line) == 1):
			continue
		params = line.strip()
		if re.search('=', params) :
			params = params.split("=")
		elif re.search(':', params) :
			params = params.split(":")

		conf = params[0].strip()
		if conf == "Numa Node":
			#start populating
			if nid != -1:
				node_throt_dict[nid] = throt_dict[nid]
			nid = int(params[1].strip())
			#throt_dict.append(dict())
		elif conf == "Throttle Level":
			lvl = int(params[1].strip())
		elif conf == "Duty Cycle":
			dc = params[1].strip()
			if dc[0] == '0' and dc[1] == 'x':
				throt_list.append(int(dc, 16))
			else:
				throt_list.append(int(dc))
		elif conf == "Computed Speed in MBPS":
			throt_list.append(float(params[1].strip()))
			throt_dict[nid][lvl] = throt_list
			throt_list = []
		elif conf == "PCI_IDs":
			numfactors = params[1].split(",")
			pci_ids = []
			for i in range(len(numfactors)):
				pci_ids.append(numfactors[i].strip())
			pciid_tree[nid] = pci_ids
		elif conf == "MAXSPEED":
			maxspeed[nid] = float(params[1].strip())
			
	if nid != -1:
		node_throt_dict[nid] = throt_dict[nid]
	cfg.close()
	trained.close()
	#pydb.set_trace()
	#display_ddr_throttle_values(node_throt_dict)
	return node_id, throttle_level, node_throt_dict, pciid_tree, maxspeed 

def scan_pcidevices():
	#1. Scan pci devices to find out throttling devices
	op = subprocess.check_output(["lspci"])

	#parse the output
	devlist = parseoutput(op, "Integrated Memory Controller", "Thermal Control")
	throttle_pci_list = []
	#pydb.set_trace()
	
	for dev in devlist:
		dump = dev.split(" ")
		throttle_pci_list.append(dump[0])
	
	#display_throttle_device(throttle_pci_list)
	#node_dict = get_pernode_throttle_dev(throttle_pci_list)
	node_dict = dict()
	devid_dict = dict()
	nid = 0
	for dev in throttle_pci_list:
		dump = dev.split(":")
		devfn = int(dump[0], 16)
		if devid_dict.has_key(devfn) == False:
			devid_dict[devfn] = nid
			nid = nid + 1

		tnid = devid_dict[devfn]
		if devid_dict[devfn] in node_dict:
			node_dict[tnid].append(dev)
		else:
			node_dict[tnid] = [dev]
			
	return node_dict

def create_reg_objects(pcid_dict):
	reg_dict = dict()
	for nid in pcid_dict:
		tlist = []
		for device in pcid_dict[nid]:
			reg = mem_throttler(nid, device)
			tlist.append(reg)
		reg_dict[nid] = tlist
	return reg_dict

def compute_duty_cycle(nid, lvl, reg, maxspeed):
		max = duty_cycle.max
		min = duty_cycle.min
		loop = 1
		target = maxspeed[nid]/float(lvl)
		error = sys.maxint
		prev_error = sys.maxint
		tcycle = min
		tspeed = 0
		while ((max - min) > 1)  :
			cycle = (min + max)/2
			for dev in reg:
				dev.throttle(cycle)
			newspeed = float(compute_ddrbw(nid))
			diff = abs(target - newspeed)
			if(error > diff) :
				tcycle = cycle
				error = diff
				tspeed = newspeed
			if(target > newspeed):
				min = cycle
			else:
				max = cycle
		#pydb.set_trace()
		return tcycle, tspeed

def reset_bw(reg_dict):
	#reset the throttling
	for regsd in reg_dict:
		for reg in reg_dict[regsd]:
			reg.dethrottle()

def compute_maxspeed(node_id, reg_dict):
	reset_bw(reg_dict)
	maxspeed = []
	for node in node_id:
		maxspeed.append(float(compute_ddrbw(node)))
	return maxspeed

def write_trained_file(tfname, node_id, node_throt_dict, pciid_dict, maxspeed):
	f = open(tfname, 'w')
	for nid in node_id:
		f.write("Numa Node:"+str(nid)+"\n")
		for tlvl in node_throt_dict[nid]:
				f.write("Throttle Level = "+str(tlvl)+"\n")
				f.write("Duty Cycle = "+hex(node_throt_dict[nid][tlvl][0])+"\n")
				f.write("Computed Speed in MBPS = "+str(node_throt_dict[nid][tlvl][1])+"\n")
		#now write the line with PCI ID's
		f.write("PCI_IDs = ")
		for i in range(len(pciid_dict[nid])):
			if i == len(pciid_dict[nid]) - 1:
				f.write(pciid_dict[nid][i]+"\n")
			else:
				f.write(pciid_dict[nid][i] + ", ")
		f.write("MAXSPEED:" + str(maxspeed[nid])+"\n")
	f.close()

def verify_and_update(tfname, node_id, throttle_levels, node_throt_dict, pciid_dict, maxspeed):
	#scan the pci devices
	scaned_pciid_dict = scan_pcidevices()
	for nid in range(len(node_id), len(scaned_pciid_dict)):
		node_id.append(nid)

	#Now update the pci device list
	for node in node_id:
		if pciid_dict.has_key(node) == False:
			pciid_dict[node] = scaned_pciid_dict[node]
		elif len(pciid_dict[node]) !=  len(scaned_pciid_dict[node]):
			pciid_dict[node] = scaned_pciid_dict[node]

	# create register dictionary. This is the actual data structure
	# used for updating PCI registers
	reg_dict = create_reg_objects(pciid_dict)

	# compute default speed for each node
	if len(maxspeed) != len(node_id):
		maxspeed = compute_maxspeed(node_id, reg_dict)

	#first check data exists for each throttle level
	for nid in node_id:
		if node_throt_dict.has_key(nid) == False:
			node_throt_dict[nid] = dict()

	#now check if all throttle level's are covered
	for nid in node_id:
		for lvl in throttle_levels:
			if node_throt_dict[nid].has_key(lvl) == False:
				dc, speed = compute_duty_cycle(nid, lvl, reg_dict[nid], maxspeed)
				node_throt_dict[nid][lvl] = [dc, speed]
	#update the training file
	if len(tfname) > 1:
		write_trained_file(tfname, node_id, node_throt_dict, pciid_dict, maxspeed)
	return reg_dict

def throttle_device(throttle_factor, node_id, node_throt_dict, reg_dict, maxspeed):
	update_tf = False
	if node_throt_dict.has_key(node_id) == True and reg_dict.has_key(node_id) == True:
		if node_throt_dict[node_id].has_key(throttle_factor) == True:
			duty_cycle = node_throt_dict[node_id][throttle_factor][0]
		else:
			#generate the duty cycle and append it to the list
			duty_cycle, speed = compute_duty_cycle(node_id, throttle_factor, reg_dict[node_id], maxspeed)
			node_throt_dict[node_id][throttle_factor] = [duty_cycle, speed]
			update_tf = True
			
		for pci_reg in reg_dict[node_id]:
			pci_reg.throttle(duty_cycle)
		print "Node", node_id,"with maxspeed",maxspeed[node_id], "throttled to speed = ", compute_ddrbw(node_id), "with scale :", throttle_factor
	else:
		print "Invalid Node ID = ", node_id
	return update_tf

def dethrottle_device(node_id, node_throt_dict, reg_dict):
	if node_throt_dict.has_key(node_id) == True and reg_dict.has_key(node_id) == True:
		for pci_reg in reg_dict[node_id]:
			pci_reg.dethrottle()
		print "Node", node_id, "speed after dethrottling = ", compute_ddrbw(node_id)
	else:
		print "Invalid Node ID = ", node_id

def show_currently_applied_configs(node_id_list, maxspeed):
	print "Listing Currently applied thorttling configurations"
	for nid in node_id_list:
		currspeed = compute_ddrbw(nid)
		factor = float(maxspeed[nid])/float(currspeed)
		print "Node", nid, "current speed = ", currspeed, "Max Speed =", maxspeed[nid], "approx throttling factor =", factor
		
def main():
	parser = OptionParser()
	parser.add_option("-c", type="string", dest="cfg_file",default="default.cfg", help="Input/Output configuration file")
	parser.add_option("-i", type="string", dest="trained_file",default="default_trained.cfg", help="Input/Output configuration file")
	parser.add_option("-t", type="int", dest="do_train", default=0,
                      help="finds duty cycle for various scaling factors 1= needed, 0 = not needed [default: %default]")
	parser.add_option("-f", type="int", dest="throttle_factor", default=-1,
                      help="throttles the memory by this factor [default: %default]")
	parser.add_option("-n", type="int", dest="node_id", default=-1,
                      help="throttles the memory on node nid [default: %default]")
	parser.add_option("-v", type="int", dest="verbose", default=0,
                      help="1 = show the current configuration on this platform [default: %default]")
	parser.add_option("--verify", type="int", dest="verify", default=0,
                      help="1 = verify and update the current platform parameters [default: %default]")
	parser.add_option("-o", type="string", dest="tfname", default="",
                      help="1 = verify and update the current platform parameters [default: %default]")
	parser.add_option("--show", type="int", dest="show", default=0, help="1 = display current cached configuration [default: %default]")
	parser.add_option("--currbw", type="int", dest="cbw", default=0, help="1 = show current bandwidth and scale factors applied to each node [default: %default]")
	parser.add_option("--lspci", type="int", dest="lspci", default=0, help="1 = show PCI ID's of throttling devices [default: %default]")

	(options, args) = parser.parse_args()
	#pydb.set_trace()
	#first parse the configuration file
	#pydb.set_trace()
	node_id_list, throttle_level, node_throt_dict, pciid_dict, maxspeed = parse_configuration_file(options)
	#pydb.set_trace()

	#if options.verbose
	#scan hardware and get the list of devices
	#scan_throttledevices()

	#pydb.set_trace()
	if options.do_train==1 :
		print "Started Training"
		reg_dict = verify_and_update(options.trained_file, node_id_list, throttle_level, node_throt_dict, pciid_dict,maxspeed)
		print "Training Complete"
	else :
		reg_dict = verify_and_update(options.tfname, node_id_list, throttle_level, node_throt_dict, pciid_dict,maxspeed)

	#pydb.set_trace()
	#command to throttle the device
	if options.throttle_factor != -1:
		if options.node_id >= 0 and options.node_id < len(node_id_list):
			if options.throttle_factor != 0:
				update = throttle_device(options.throttle_factor, options.node_id, node_throt_dict, reg_dict, maxspeed)
				if update == True:
					write_trained_file(options.trained_file, node_id_list, node_throt_dict, pciid_dict,maxspeed)
			else:
				print "dethrottling Node#", options.node_id
				dethrottle_device(options.node_id, node_throt_dict, reg_dict)
		else:
			print "Invalid node id# ",options.node_id
			sys.exit(-1)
		
	if options.show == 1:
		display_ddr_throttle_values(node_throt_dict)
		print "Maximum Bandwidth as computed via stream_c"
		for nid in node_id_list:
			print "Node#",nid,"=",maxspeed[nid],"MBPS"

	if options.cbw == 1:
		show_currently_applied_configs(node_id_list, maxspeed)

	if options.lspci == 1:
		print "PCI Devices supporting throttling"
		devlist = scan_pcidevices()
		for dev in devlist:
			print "Node #:", dev, devlist[dev]

if __name__ == '__main__':
    main()

