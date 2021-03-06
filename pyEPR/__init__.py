# This file is part of pyEPR: Energy participation ratio (EPR) design of quantum circuits in python
#
#    Copyright (c) 2015 and later, Zlatko minev and Zaki Leghtas
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the pyEPR nor the names
#       of its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

### Compatibility with python 2.7 and 3
from __future__ import division, print_function, absolute_import



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Configure logging 
import logging
logger = logging.getLogger('pyEPR') # singleton
if not len(logger.handlers):
    c_handler = logging.StreamHandler()
    logger.propagate = False
    # Jupyter notebooks already has a stream handler on the default log,
    # Do not propage upstream to the root logger.  https://stackoverflow.com/questions/31403679/python-logging-module-duplicated-console-output-ipython-notebook-qtconsole
        
    # Format 
    c_handler.setLevel(logging.WARNING)
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s\n   ::%(pathname)s:%(lineno)d: %(funcName)s\n')  #  unlike the root logger, a custom logger can’t be configured using basicConfig(). 
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)
    
    

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# Import Checks Matplotlib & core packages
__STD_END_MSG = """\n   Please install it and provide the system.PATH reference. 
   See online setup instructions at 
   https://github.com/zlatko-minev/pyEPR"""
   
try:
    import matplotlib as mpl
except (ImportError, ModuleNotFoundError):
    logger.warning("""IMPORT WARNING:
   Could not find package `matplotlib`. 
   Plotting will not work unless you install it. """ + __STD_END_MSG)
    
    
try:
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)
except (ImportError, ModuleNotFoundError):    
    logger.warning("""IMPORT WARNING:
   `pandas` python package not found.""" + __STD_END_MSG)

# Check for qutip
try:
    import qutip
except (ImportError, ModuleNotFoundError):
    logger.warning("""IMPORT WARNING:
   `qutip` package not found. 
   Numerical diagonalization will not work.
 
   You could try `conda install -c conda-forge qutip`
                   """ + __STD_END_MSG)
else:
    del qutip, warnings


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# pyEPR Specific 
    
### Config setup
from . import config
try:  # Check if we're in IPython.
    __IPYTHON__
    config.ipython = True
except:
    config.ipython = False
config.__STD_END_MSG = __STD_END_MSG
    

### Convenience variable and function imports
from collections import OrderedDict
from .toolbox import *
from .toolbox_plotting import *
from .hfss import load_HFSS_project, get_active_design, get_active_project,\
                  HfssProject
from .hfss import release as hfss_release
from .core import Project_Info, pyEPR_HFSS, pyEPR_Analysis