#!/usr/bin/env python3
import asyncio
import random
from time import sleep
import json
from multiprocessing import Process, Pool
from threading import Thread

class Node(Process):
	# Time in ms
	MIN_NOMINATION_DURATION = 750 # Min Buffer Time before candidate declaration
	MAX_NOMINATION_DURATION = 250 # Max Buffer Time before candidate declaration
	ELECTION_DURATION = 500 # Wait Time to receive votes
	SESSION_TIMER = 1800000 # Session duration before next election
	RESULT_CONFIRMATION_TIMER = 60000 # Wait Time to receive submissions from all followers
	CLUSTER_SIZE = 5 # Size of a cluster, set by default

	def __init__(self, node_id):
		self.id = node_id # Port No a node is running on
		self.history = [] # Set of all computations done
		self.CL = 5000 # Central Leader of a node
		self.LL = None # Local Leader of a node
		self.task_queue = [] # Tasks a CL is running
		self.no_of_tasks_queued = 0 # No of tasks a CL has iin its queue that have not been processed
		self.local_leaders = [] # List of all Local Leaders
		self.number_of_clusters = 0 # Total number of clusters
		self.all_node_info = [] # Dict of all active ports to cluster no on the network
		self.ll_vote_count = -1 # Vote Count if this node is a local leader candidate
		self.cl_vote_count = -1  # Vote Count if this node is a central leader candidate
		self.has_ll_voted = False # True, if this node has voted during election
		self.has_cl_voted = False # True, if this node is LL and voted for a central leader
		self.is_election = False # True, if election is happening rn. Does not accept tasks if set to true

		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind((socket.gethostname(), self.id))
		self.serversocket.listen(10)  # upto 10 connections can be held in queue

	# Create Task and send to CL
	def submit_to_leader(task):
		pass


	# Run a Task, done by followers
	def compute_data():
		pass


	# Pre Election Broadcast from CL about current history 
	def add_to_history(self, tx_history):
		self.history.append(tx_history)


	# Open socket connection listening for other nodes
	# During Cluster Election,
	# 	Accept from same cluster only
	# During Central Election,
	# 	Accept from other LL only if LL
	# When not election,
	# 	Accept from CL and LL
	def socket_listen():
		while True:
			(clientsocket, address) = self.serversocket.accept()
			data = clientsocket.recv(4096)
			if not data:
				print("Sadly, something went wrong lol")
			data = json.loads(data)
			if data['type'] == 'sometype':
				# call the correct method with the right parameters


	def send_data_to_node(type_of_message, data, port):
		mySocket = socket.socket()
		sending_data = {
			'type': type_of_message,
			'data': data
		}
		sending_data = json.dumps(sending_data).encode('utf-8')
		mySocket.connect((socket.gethostname(), port))
		mySocket.sendall(data)


	# Handles all election calls, runs on a thread
	def election_handler(self):
		while True:
			self.is_election = True
			self.has_ll_voted = False
			cluster_election(self)
			self.has_voted = False
			self.has_cl_voted = False
			network_election(self)
			self.is_election = False
			sleep(SESSION_TIMER)


	# Assign Cluster Ids for every node, only used by CL
	def assign_cluster(self):
		num_nodes = len(self.all_node_info)
		num_clusters = num_nodes // Node.CLUSTER_SIZE
		
		random_assign = []
		for x in range(0, num_clusters):
			for y in range(0, Node.CLUSTER_SIZE):
				random_assign.append(x)
		random.shuffle(random_assign)
		
		index = 0
		for key in self.all_node_info:
			self.all_node_info[key] = random_assign[index]
			index += 1

		for key in self.all_node_info:
			self.send_data_to_node('cluster', self.all_node_info, key)

	# Update all node cluster info
	def receive_cluster_info(self, all_node_info):
		self.all_node_info = all_node_info


	# Cluster election happens
	# Wait for randomized nomination time, Send vote request to every one in cluster
	# Wait for responses, if majority, send to every cluster node saying I am LL
	# Send information to CL
	def cluster_election(self):
		if self.has_ll_voted:
			return
		
		# Wait for Nomination Buffer Time
		nomination_wait_time = random.randint(Node.MIN_NOMINATION_DURATION, Node.MAX_NOMINATION_DURATION)
		sleep(nomination_wait_time / 1000)

		if self.has_ll_voted:
			return

		# Send vote requests
		cluster_no = self.all_node_info[self.id]
		self.ll_vote_count = 1
		self.has_ll_voted = True
		for key in self.all_node_info:
			if self.all_node_info[key] == cluster_no:  # same cluster
				self.send_data_to_node('vote_request', 'NIL', key)
		
		# Wait for everyone to send votes
		sleep(Node.ELECTION_DURATION / 1000)

		# If majority, Send to all nodes in network
		if vote_count >= (Node.CLUSTER_COUNT // 2):
			for key in self.all_node_info.keys():
				if (self.all_node_info[key] == cluster_no):
					self.send_data_to_node('i_am_ll', 'NIL', key)


	# Called when central leader sends local leader information
	def receive_ll_info(self, local_leaders):
		self.local_leaders = local_leaders


	def receive_ll_vote_request(self, id):
		if(self.has_ll_voted == False)
			self.has_ll_voted = True
			# Socket send vote to recipient accepting vote request.


	# Central Leader Election
	# Randomly select one central leader out of existing LLs
	# Transfer cluster data to every node
	def network_election(self):
		if(self.local_leaders[self.all_node_info[id]] == id):
			if self.has_cl_voted:
				return
			
			nomination_wait_time = random.randint(MIN_NOMINATION_DURATION, MAX_NOMINATION_DURATION)
			sleep(nomination_wait_time / 1000)

			if self.has_cl_voted:
				return

			# Send vote requests
			self.cl_vote_count = 1
			self.has_cl_voted = True
			for key, value in self.all_node_info.items():
				if(key == self.local_leader[self.all_node_info[key]]):
					# Socket send vote request to node
			
			sleep(Node.ELECTION_DURATION / 1000)

			if vote_count >= (CLUSTER_COUNT // 2):
				for key in self.all_node_info.items():
					self.send_data_to_node('i_am_cc', 'NIL', key)


	# Called by CL, once election is over
	def assign_to_LL():
		pass


	def assign_to_followers():
		pass

	def send_to_LL():
		pass
	
	def validate_answer():
		pass
	
	def send_to_CL():
		pass
