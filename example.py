''' Author: Deepankar Arya (deepankar1994@gmail.com) '''
from quesim import simulate_main
lamb = 0.5
mu = 0.8
delta = 1.0
j_cut = 2
num_servers = 5
w1, w2, w3, nq = simulate_main(lamb, mu, delta, j_cut, num_servers)
print w1, w2, w3, nq