This the implementation of the following paper:

CITATION:

Khan, Arif and Halappanavar, Mahantesh and Hagge, Tobias and Kowalski, Karol and Pothen, Alex and Krishnamoorthy, Sriram, Mapping Arbitrarily Sparse Two-Body Interactions on One-Dimensional Quantum Circuits, IEEE 26th International Conference on High Performance Computing, Data, and Analytics (HiPC), 2019

ABSTRACT: 

We consider an assignment problem arising in Fermionic-swap based mapping of the one-body and two-body interaction terms in simulating time evolution of a sparse second-quantized electronic structure Hamiltonian on a quantum computer. Relative efficiency of different assignment algorithms depends on the relative costs of performing a swap and computing a Hamiltonian interaction term. Under the assumption that the interaction term cost dominates the computation, we develop an iterative algorithm that uses minimum cost linear assignment (MINLA) and matching for one-body interactions, and hypergraph optimal linear arrangement (HOLA) and partial distance-2 coloring for two-body interactions, to exploit arbitrary sparsity in the Hamiltonian for efficient computation. Using a set of 122 problems from computational chemistry, we demonstrate performance improvements up to 100% relative to the state-ofthe-art approach for one-body terms and up to 86% utilization for two-body terms relative to a theoretical peak utilization. To the best of our knowledge, this is the first study to exploit arbitrary sparsity in orbital interactions for efficient computation on one-dimensional qubit connectivity layouts. The proposed algorithms lay a foundation for extension to map general k-body interactions that arise in many domains onto generalized qubit connectivity layouts available in current and future quantum systems.

CONTACT:

Arif Khan, ariful.khan@pnnl.gov Alex Pothen, apothen@purdue.edu Mahantesh Halappanavar, hala@pnnl.gov


RUNNING THE CODE:

The python implementation is in the /src directory.

Example driver code is is written in QMAP.py 
