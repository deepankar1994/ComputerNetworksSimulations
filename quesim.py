''' Author: Deepankar Arya (deepankar1994@gmail.com) '''
import numpy as np
from random import randint

class Person:
	def __init__(self, jock_allow=False, arrival_time=0.0, serve_time=0.0, finish_time=0.0):
		self.jock_allow = jock_allow
		self.arrival_time = arrival_time
		self.serve_time = serve_time
		self.finish_time = finish_time
		self.succ_jock = False
	def __str__(self):
		string = str(self.jock_prob) + ',' + str(self.arrival_time)  + ',' + str(self.serve_time) + ',' + str(self.finish_time)
		return string


all_arrivals = []
wait_time_jock = []
wait_time_no_jock = []
que_dict = {}

def simulate_main(l, m, delta, j_cut, num_servers = 5):
	''' Parameters:
		l: arrival rate, m: service rate, delta: Probability that a packet has jockeying behavior
		j_cut: minimum size difference in queues needed for a person to consider jockeying
		num_servers: number of servers
		Return values:
		average waiting time for jockeying customers,
		average waiting time for non-jockeying customers,
		average waiting time for all customers,
		average queue size
	'''
	inf = 1e16
	global all_arrivals
	global wait_time_jock
	global wait_time_no_jock
	global que_dict
	lam = l
	mu = m

	jock_prob = delta

	param_1 = 1.0 / lam
	param_2 = 1.0 / mu


	#all_arrivals = []
	all_arrivals = []
	num_people = 100000
	num_q = []
	def sim_arrivals():
		global all_arrivals
		curr_time = 0.0
		for i in range(num_people):
			next_arr = curr_time + np.random.exponential(param_1)
			prob = np.random.uniform(0, 1)
			jock_allow = False
			if prob <= jock_prob:
				jock_allow = True
			per = Person(jock_allow, next_arr, 0.0, 0.0)
			all_arrivals.append(per)
			curr_time = next_arr

	sim_arrivals()
	wait_time_jock = []
	wait_time_no_jock = []
	'''for i in all_arrivals:
		print i'''
	que_dict = {}
	#next_free = []
	for i in range(num_servers):
		que_dict[i] = []
		#next_free.append(0.0)



	def get_len(curr_time):
		q_size = []
		tot_q = 0
		global que_dict
		for i in range(num_servers):
			sz = 0
			nw_list = []
			for j in que_dict[i]:
				if(all_arrivals[j].finish_time > curr_time):
					sz += 1
					nw_list.append(j)
			que_dict[i] = nw_list
	 		q_size.append(sz)
	 		tot_q += sz
		return q_size, tot_q




	jock_cuttoff = j_cut

	for per_idx, per in enumerate(all_arrivals):
		c_time = per.arrival_time
		min_sz = inf
		min_idx = randint(0, num_servers - 1)
		q_size, qs = get_len(c_time)
		#print q_size
		num_q.append(qs)

		'''for i, sz in enumerate(q_size):
			if sz <= min_sz:
				min_sz = sz 
				min_idx = i '''
		min_sz = q_size[min_idx]
		sv_time = np.random.exponential(param_2)
		if min_sz == 0:
			per.serve_time = c_time
			per.finish_time = c_time + sv_time
		else:
			per.serve_time = all_arrivals[que_dict[min_idx][min_sz - 1]].finish_time
			per.finish_time = all_arrivals[que_dict[min_idx][min_sz - 1]].finish_time + sv_time
		que_dict[min_idx].append(per_idx)
		q_size[min_idx] += 1
		swt_dict = {}
		for i, sz_1 in enumerate(q_size):
			for j, sz_2 in enumerate(q_size):
				if(sz_1 - sz_2 >= jock_cuttoff and all_arrivals[que_dict[i][-1]].jock_allow):
					#swt_list.append((i, j))
					swt_dict[i] = j
		#print 'Start'
		for key, value in swt_dict.iteritems():
			lst_val = que_dict[key][-1]
			sv_tim = all_arrivals[lst_val].finish_time - all_arrivals[lst_val].serve_time
			if q_size[value] == 0:
				all_arrivals[lst_val].serve_time = c_time
				all_arrivals[lst_val].finish_time = c_time + sv_tim
			else:
				l_val = que_dict[value][-1]
				all_arrivals[lst_val].serve_time = all_arrivals[l_val].finish_time
				all_arrivals[lst_val].finish_time = all_arrivals[lst_val].serve_time + sv_tim


			all_arrivals[lst_val].succ_jock = True
			del que_dict[key][-1]
			que_dict[value].append(lst_val)
			#print q_size
			q_size[value] += 1
			q_size[key] -= 1
			#print q_size







	def cal_stats():
		all_waiting = []
		jock_wait = []
		not_jock_wait = []

		for per in all_arrivals:
			wt = per.serve_time - per.arrival_time
			if per.succ_jock:	
				jock_wait.append(wt)
			else:
				not_jock_wait.append(wt)
		#print len(jock_wait)
		#print len(not_jock_wait)
		j_m = 0
		nj_m = 0
		if len(jock_wait):
			j_m = np.mean(jock_wait)
		if len(not_jock_wait):
			nj_m = np.mean(not_jock_wait)
		#return np.mean(jock_wait), np.mean(not_jock_wait)
		tot_wt = jock_wait + not_jock_wait
		tw = np.mean(tot_wt)
		return j_m, nj_m, tw, np.mean(num_q)



	'''for i in all_arrivals:
		print i'''

	return cal_stats()
