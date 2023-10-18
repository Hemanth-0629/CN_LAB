import numpy as np
import pandas as pd
from math import sqrt

hq_ht_t = np.array([0.5,0.5,-0.5,-0.25,-0.25])

A=[[1,0.135,0.195,0.137,0.157],
 [0.135,1,0.2,0.309,0.143],
  [0.195,0.2,1,0.157,0.122],
   [0.137,0.309,0.157,1,0.195],
   [0.157,0.143,0.122,0.195,1]]

A = np.array(A)
A

hq_ht = hq_ht_t.T
Quad_form_distance = sqrt(np.dot(np.dot(hq_ht,A),hq_ht_t))
print(Quad_form_distance)