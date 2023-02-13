
import numpy as np 
import scipy
import matplotlib.pyplot as plt
from io import StringIO, BytesIO

class elements:
    def __init__(self,ax,x,y,lw):
        self.x = x
        self.y = y
        self.lw = lw
        self.ax = ax

    def R(self):
        x0 = np.linspace(0,7,15)
        y0 = np.array([0,0,0.3,0,-0.3,0,0.3,0,-0.3,0,0.3,0,-0.3,0,0])
        self.ax.plot(self.x+x0, self.y+y0, color='black',lw=self.lw)

        self.x += x0[-1]
        self.y += y0[-1]
    def W(self):
        x0 = np.linspace(1,6,9)
        y0 = np.array([0.3,0,-0.3,0,0.3,0,-0.3,0,0.3])
        self.ax.plot(self.x+x0, self.y+y0, color='black',lw=self.lw)
        self.ax.plot(self.x+np.array([0,1.625]), self.y+np.array([0,0]), color='black',lw=self.lw)
        self.ax.plot(self.x+np.array([5.375,7]), self.y+np.array([0,0]), color='black',lw=self.lw)
        self.x += 7
        self.y += 0

    def C(self):
        lm = 2
        rm = 5
        self.ax.plot(self.x+np.array([lm,lm]), self.y+np.array([-0.3,0.3]), color='black',lw=self.lw)
        self.ax.plot(self.x+np.array([rm,rm]), self.y+np.array([-0.3,0.3]), color='black',lw=self.lw)
        self.ax.plot(self.x+np.array([0,lm]), self.y+np.array([0,0]), color='black',lw=self.lw)
        self.ax.plot(self.x+np.array([rm,7]), self.y+np.array([0,0]), color='black',lw=self.lw)
        self.x += 7
        self.y += 0
    def line(self):
        length = 7
        self.ax.plot(self.x+np.array([0,length]), self.y+np.array([0,0]), color='black',lw=self.lw)
        self.x += length
        self.y += 0
    def long_line(self):
        length = 14
        self.ax.plot(self.x+np.array([0,length]), self.y+np.array([0,0]), color='black',lw=self.lw)
        self.x += length
        self.y += 0
        
    def p(self,upper_elm,lower_elm):
        height = 0.5
        x_p = self.x
        y_p = self.y 
        self.ax.plot(self.x+np.array([0,0]), self.y+np.array([-height,height]), color='black',lw=self.lw)
        self.x += 0 
        self.y += height
        up_len = len(upper_elm)
        low_len = len(lower_elm)
        if up_len >= low_len:
            self.line()
        else:
            for i in range (0,low_len-up_len+1):
                self.line()
        for i in range (0,up_len):
                    upper_elm[i]()
                    self.line()
        if up_len < low_len:
            for i in range (0,low_len-up_len):
                self.line()
        self.x = x_p
        self.y = y_p-height
        if up_len <= low_len:
            self.line()
        else:
            for i in range (0,up_len-low_len+1):
                self.line()
        for i in range(0,low_len):
            lower_elm[i]()
            self.line()
        if low_len < up_len:
            for i in range (0,up_len-low_len):
                self.line()

        self.y = y_p
        self.ax.plot(self.x+np.array([0,0]), self.y+np.array([-height,height]), color='black',lw=self.lw)
    def save(self,name,dpi,w,h,transparent=True):

        fig =self.get_fig(w, h)
        fig.savefig(name, bbox_inches='tight', transparent=transparent, dpi=dpi)
        
    def get_fig(self,w,h):
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.ax.set_frame_on(False)
        fig = self.ax.get_figure().set_size_inches(w,h)
        return(fig)
        
    def getimage(self, w,h,fmt='png'):

        fig = self.get_fig(w,h)
        output = BytesIO()
        plt.savefig(output, format=fmt, bbox_inches='tight')
        image = output.getvalue()
        return(image)

def impedance_data_processing(text_file,option):
    '''
    
    Parameters
    ----------
    text_file : str
        file name of the impedance data.
    Returns
    -------
    the dataframe with column 'Z1', 'Z2', and 'frequency'.
    '''
    data=np.loadtxt(text_file,delimiter=",",skiprows=11)
    f=data[:,0]
    Z1=data[:,4]
    Z2=data[:,5]
    if option == 'No':
        
        mask = np.array(Z2)<0
        f = f[mask]
        Z1 = Z1[mask]
        Z2 = Z2[mask]
    Z=np.array(Z1) +1j*np.array(Z2)
    return(f,Z)

    
    
    
    
    
    