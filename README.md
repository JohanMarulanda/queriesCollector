# DNS QUERIES COLLECTOR
Project to capture information from DNS servers and send it to an API. basically it is a python script which receives a file, parses it, and sends it by packets of 500 rows to later be sent to a LUMU API.

# INSTALLATION
The project is located in [Github](https://github.com/JohanMarulanda/queriesCollector), you can clone it with `git clone`.

# HOW RUN THE PROJECT
You can use it or not a virtualenv with the libraries in the requirements.txt, for run the project you run:
```
$ python ./queries_collector.py <path_to_file>
```

# COMPLEXITY OF THE ALGORITTHM
The complexity of the algorithm is O(n) since it is based on the size of the lines that the file has to carry out its execution, finally, by increasing the number of lines in the file, the execution time of the project also increases.