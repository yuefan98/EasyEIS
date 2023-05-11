#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 13:10:00 2023

@author: yuefanji
"""

import streamlit as st
import numpy as np 
import pandas as pd
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
        ('Information', 'EIS analyzer','EIS Dynamic Visualization', 'Nonlinear EIS analyzer'))

    if info == 'EIS analyzer':
        uploaded_file = st.file_uploader("Choose a file")
        option = st.radio(
            "Do you want to show the negative impedance value",
            ('Yes', 'No'),horizontal=True)
        agree = st.checkbox('Fit your model')    
    if info == 'EIS Dynamic Visualization':
        uploaded_file = st.file_uploader("Choose a file")
        option_neg = st.radio(
            "Do you want to show the negative impedance value",
            ('Yes', 'No'),index =1, horizontal=True)
############################## 
#Information start
##############################

circuit_element = [['Resistor', 'R'], ['Capacitor', 'C'], ['Warburg element', 'W']]
circuit_element_df = pd.DataFrame(circuit_element, columns = ['Circuit Element', 'Symbol'])

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

if info == 'Information':
    st.title('Welcome to Easy EIS !')
    '''Easy EIS provides an open access analysis and visualization tool for beginner to understand the fundamental impedance analysis.
    This program is developed based on the fundation of [impedance.py](https://impedancepy.readthedocs.io/en/latest/). 
    One important aspect of this program is to provide an user interface for impedance.py.
    The author of this program would like to direct the user to use impedance.py to pipeline their analysis  
   Eventually, nonlinear EIS analysis and visualization will be supported to bring in the lastest reasearch result we have found in our lab'''  
    '''Please read through descriptions to learn about the functionality of this program.'''
    '''
    Please visit my [GitHub](https://github.com/yuefan98/EasyEIS) for more information!
    '''
    st.subheader('EIS Analyzer')
    with st.expander(''):
        '''
        Currently, this program supports three fundamental circuit element for impedance analysis as shown in the table below. 
        '''
        colt1, colt2, colt3 = st.columns(3)
        with colt1:
            st.table(circuit_element_df)
        with colt2:
            st.write("")

        with colt3:
            st.write('')
        '''
        Series and parallel circuit are supported follows the convention used by impedance.py. 
        For example, a series of resistor can be represented by 'R-R'. The Randles circuit can be represented by p(R,C).
        The diffusion impedance is introduced through the coupling of charge transfer resistance and Warburg element.
        An Randles circuit with diffusion hinderance can be represented by p(R*W,C)
        '''
    st.subheader('EIS Dynamic Visualization')
    with st.expander(''):
        '''After obtaining best fit parameters from EIS analyzer, this functionality will enable you to explore 
        the sensitivity of the EIS spectrum with respect to the change of physical parameters.
       '''
        '''The main purpose of the dynamic visualization is to enable users to understand fundamentals of physcis based EIS model.
        i.e. in Randles circuit, the charge transfer reistance defines the width of the semi-circle, 
        and RC defines the characteristic time constant.
       '''
    st.subheader('Nonlinear EIS Analyzer')
    with st.expander(''):
         '''
         The nonlinear EIS analyzer will bring in state of art model for NLEIS developed in our lab. This will be supported in the future!
        '''
############################## 
#Information end
##############################

##############################
#EIS Start
###############################

parm = []
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
                # ny += 1
        
            nx += 0.5
    
        EEC.line()
        image_bytes = EEC.getimage(w=5*nx,h=2*ny,fmt='jpg')
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
    st.session_state['circ_str_1']= circ_str_1
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

            st.session_state['parm'] = circuit_1.parameters_
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
#EIS Dynamic visualization 
###############################
if info == 'EIS Dynamic Visualization':
    if uploaded_file is not None:
        parm = st.session_state['parm'] 

        col11, col22 = st.columns(2) 
        with col11:
            for i in range(len(parm)):
                globals()[f'p{i}']=st.slider('p'+str(i), float(parm[i])/2, float(parm[i])*2, float(parm[i]),step=float(parm[i])/10)
    
        with col22:
            
            initial_guess = np.zeros(len(parm))
            for i in range(len(parm)):
                initial_guess[i]= eval('p'+str(i))
            
            fig, ax = plt.subplots()

            f,Z= impedance_data_processing(uploaded_file,option_neg)
            plot_nyquist(Z,ax =ax, label='data', fmt = 'o')
            circuit_2 = CustomCircuit(st.session_state['circ_str_1'],initial_guess=initial_guess)
        
            Z_fit = circuit_2.predict(f)
            plot_nyquist(Z_fit,ax=ax,label = 'fit',fmt = '-o')
            plt.legend()
            plt.tight_layout()
            st.pyplot(fig)
            
###############################
#EIS Dynamic visualization end 
###############################

###############################
#Nonlinear EIS analyzer start
###############################

if info =='Nonlinear EIS analyzer':
    
    st.title('This functionality is currently under construction, and will be supported in the future !')

    
