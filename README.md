# DΕΤΕΧΑ: Declarative Extensible Text Exploration and Analysis

The repository contains a text mining library built on top of [YeSQL](https://github.com/athenarc/YeSQL/). 
The library maps several text mining functionalities to reusable scalar, aggregate, and polymorphic table UDFs written in Python. Due to the
performance characteristics of YeSQL and its design, the presented framework is
able to execute critical text mining analytical tasks faster than other popular solutions, and allows data scientists to implement end-to-end text analytic pipelines within a declarative extended SQL. 

## Instructions

Install PyPy3 from here https://www.pypy.org

Run `pypy3 DETEXA/mterm.py [-d database.db -f funcs]`

Terminal help with ` .h `

List all functions with ` .functions `

Explain a function with `.h functionname`

Optional: Implement your own functions in a funcs directory and give it as a terminal parameter.

The natively supported functions are stored in DETEXA/functions/[row/aggregate/vtable] directories.




## Publication

"DΕΤΕΧΑ: Declarative Extensible Text Exploration and Analysis", Yannis Foufoulas, Eleni Zacharia, Harry Dimitropoulos, Natalia Manola and Yannis Ioannidis, Theory and Practice of Digital Libraries (TPDL), 2022

## Note

The source code of the library and the experiments will be available here by 19/9/2022
