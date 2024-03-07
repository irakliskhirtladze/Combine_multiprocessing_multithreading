# Multiprocessing combined with multithreading

### Description

Run 'products.py' to obtain 100 JSON-formated products from a server. It uses PyQt5 library for GUI.

This app demonstrates how to combine myltiprocessing with multithreading. 

The goal is to run selected number (N) of processes, each having predetermined number of threads.

First we create a list of 100 URLs, then it is divided into N sublists. Each sublist contains as many URLs as there are corresponding number of threads for N processes.

The ProcessPoolExecutor class from concurrent.futures library creates N processes for each sublist.
Each process then creates corresponding number of threads using ThreadPoolExecutor from the same library by calling custom threader() function.
Each thread also calls custom get_product() function, which is responsible for obtaining a product from the server.

Products are added to a list which in the end is written to a JSON file.

### Author's observation

For this task more processes with less threads in each, generally increases required time.

### Requirements

Python 3.x (recommended 3.9)

PyQt5

requests