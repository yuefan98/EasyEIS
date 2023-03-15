#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 13:10:00 2023

@author: yuefanji
"""

import streamlit as st
import numpy as np 
import scipy
import matplotlib.pyplot as plt
from impedance.models.circuits import CustomCircuit
from impedance.validation import linKK
from  easy_eis import *
from io import StringIO, BytesIO
from impedance.visualization import plot_nyquist
import time
from PIL import Image


img = Image.open('logo/transparent-logo.png')
st.set_page_config(page_title='Easy EIS', page_icon = img , layout="wide")
# st.set_page_config(layout="centered")

st.markdown("""
<style>
.big-font {
    font-size:300px !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    image = 'logo/logo3.png'
    st.image(image,use_column_width='always')
    st.write('Welcome to Easy EIS, an impedance learning tool built based on impedance.py')
    info = st.selectbox(
        'Please select one to start:',
        ('Information', 'EIS analyzer', 'Nonlinear EIS analyzer'))
    if info == 'EIS analyzer':
        uploaded_file = st.file_uploader("Choose a file")
        option = st.radio(
            "Do you want to show the negative impedance value",
            ('Yes', 'No'),horizontal=True)
        agree = st.checkbox('Fit your model')    
##############################
#EIS Start
###############################
if info == 'EIS analyzer':

    
    circ_str = st.text_input('Circuit Elements (at least 2)', 'p(R,C)')
    

    if len(circ_str) > 0:
        names = circ_str.replace(' ', '').split('-')
        fig, ax = plt.subplots()
        
        EEC=elements(ax,0,0,2)
        EEC.long_line()
        elem_arr =['R','C','W']
        nx=0.5
        ny=1
        if len (names) ==1 and names[0] in elem_arr:
            e = RuntimeError('This is an exception of type RuntimeError')
            st.exception(e)
            st.stop()
        for elem in names:
            if elem in elem_arr:
                getattr(EEC, elem)()
                EEC.line()
            if 'p' == elem[0]:
                elem_name = elem.replace('p', '').replace('(', '').replace(')', '').split(',')
                elem_name_up = elem_name[0].split('*')
                elem_name_low = elem_name[1].split('*')
                elem_up = []
                elem_low = []
                for i in range (0,len(elem_name_up)):
                    if elem_name_up [i] in elem_arr:
                        elem_up.append(getattr(EEC, elem_name_up[i]))
                    else:
                        st.error('This is an error', icon="🚨")
                        plt.clf()
                        break
                        
                for i in range (0,len(elem_name_low)):
                    if elem_name_low [i] in elem_arr:
                        elem_low.append(getattr(EEC, elem_name_low[i]))
                    else:
                        st.error('This is an error', icon="🚨")
                        plt.clf()
                        break
    
                    
                EEC.p(elem_up,elem_low)
                EEC.line()
                ny += 1
        
            nx += 0.5
    
        EEC.line()
        image_bytes = EEC.getimage(w=5*nx,h=1*ny,fmt='jpg')
        st.image(image_bytes)
    else:
        st.error('This is an error', icon="🚨")
    EEC_download = st.download_button(
       label="Download the circuit diagram",
       data=image_bytes,
       file_name='Equivalent Circuit.png',
       mime="image/png"
    )
    
    
#######################
        
    circ_str_0 = circ_str.replace('*', '-')
    elem_dic ={'R':0,'C':0,'W':0}
    p_num = {'R':1,'C':1,'W':1}
    circ_str_1 = '' 
    num_initial_guess = 0
    for i in range (len(circ_str)):
        circ_str_1 += circ_str_0[i]
        if circ_str_0[i] in elem_dic:
            circ_str_1 += str(elem_dic[circ_str_0[i]])
            elem_dic[circ_str_0[i]] +=1
            num_initial_guess += p_num[circ_str_0[i]]
            
    ##
    default_guess = np.ones(num_initial_guess)*0.01
    default_guess = str(default_guess).replace(' ',',').replace('[','').replace(']','')
    initial_guess = st.text_input('Please input the initial guess or use the default value', default_guess)
    list1=list(initial_guess.split(','))
    initial_guess_1 = list(map(float,list1))
    ##
    # agree = st.checkbox('Fit')
    circuit_1 = CustomCircuit(circ_str_1,initial_guess=initial_guess_1)
####################################
    if uploaded_file is not None:
        fig, ax = plt.subplots()
        f, Z = impedance_data_processing(uploaded_file,option)
        plot_nyquist(Z,ax =ax, label='data', fmt = 'o')
        # if st.button('Fit'):
        if agree :
            start = time.time()
            circuit_1.fit(f,Z)
            Z_fit = circuit_1.predict(f)
            plot_nyquist(Z_fit,ax=ax,label = 'fit',fmt = '-o')
            end = time.time()
            
            st.success('Calculation finished in ' + str(round(end-start,3))+' s', icon="✅")
        plt.legend()
        plt.tight_layout()
            
        st.pyplot(fig)
        
        fn = 'impedance.png'
        plt.savefig(fn)
        with open(fn, "rb") as img:
            impedance_download = st.download_button(
                label="Download the Nyquist plot",
                data=img,
                file_name=fn,
                mime="image/png"
            )

#########################################
    with st.expander("Example Code"):
        code = '''import numpy as np 
import pandas as pd
import scipy
import matplotlib.pyplot as plt
from impedance.models.circuits import CustomCircuit
from impedance.visualization import plot_nyquist
circ_str_1 = ''' +circ_str_1 +'''
initial_guess_1 = ''' + str(list1)+'''
circuit_1 = CustomCircuit(circ_str_1,initial_guess=initial_guess_1)
circuit_1.fit(f,Z)
Z_fit = circuit_1.predict(f)
fig, ax = plt.subplots()
plot_nyquist(Z,ax=ax,label='data', fmt='o')
plot_nyquist(Z_fit,ax=ax,label = 'fit', fmt='-o')
plt.legend()
plt.show()
         '''
        st.code(code, language='python')
##############################
#EIS End
###############################
