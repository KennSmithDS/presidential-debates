import re
import nltk
import pandas as pd
import numpy as np

# noise to remove
# <p>(APPLAUSE)</p>
# <p>(CROSSTALK)</p>
# <p>(LAUGHTER)</p>
# [*]

# indicator of speech ending
# <p>END</p>

"""
Create container list for each sentence for active speakers
Create active speaker flag to append new sentences to active speaker
For each <P> tag contents
    If first word all CAPS and ends with ':' e.g. 'OBAMA:'
        Change active speaker flag
        Remove <p>...</p> tags
        Append sentence as dictionary to speaker container list
            {'speaker': 'sentence'}
    Else
        Remove <p>...</p> tags
        Append sentence as dictionary to speaker container list
            {'speaker': 'sentence'}
Convert speaker dictionary container to pandas dataframe
"""

