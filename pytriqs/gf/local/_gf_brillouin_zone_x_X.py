from select_indices import *
from scipy.interpolate import griddata
import numpy as np

def plottable_slice_along_path(self,path, method="cubic"):

     indices,high_sym=select_path_indices(path,self.mesh.components[0],True)

     d=np.zeros((len(indices)*len(self.mesh.components[1]),3), np.complex64)
     i=0
     for i_k in range(len(indices)):
         i_om=0
         for w in self.mesh.components[1]:
            d[i,0] = i_k
            d[i,1] = w
            d[i,2] = self.data[indices[i_k],i_om, 0, 0]
            #print d[i,1].real,d[i,2].imag
            i+=1
            i_om+=1
 
     x = d[:,0]
     y = d[:,1]
     z = d[:,2]
     zmin=np.amin(z.real)+1j*np.amin(z.imag)
     zmax=np.amax(z.real)+1j*np.amax(z.imag)
     xi = np.linspace(min(x), max(x),50)
     yi = np.linspace(min(y), max(y),50)
     zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method=method)
 
     return xi,yi,zi,zmin,zmax,high_sym

def plot(self, opt_dict):
    r"""
    Plot protocol for GfBrillouinZone objects.
    """

    plot_type = opt_dict.pop('type','contourf')
    method = opt_dict.pop('method', 'nearest')
    comp = opt_dict.pop('mode', 'R')
    component=  lambda x : x.real if comp=="R" else x.imag

    if plot_type=="contourf":
     path=opt_dict.pop("path")
     x,y,z,zmin, zmax, high_sym = plottable_slice_along_path(self,path=path, method=method)

     xticks_args=([i for i,j in high_sym], ["%1.3f,%1.3f"%(i,j) for i,j in path],)
     default_dict = {'xdata': x, 
                     'ydata': y, 
                     'label': r'$G_\mathbf{k}$', 
                     'xlabel': r'$\mathbf{k}$',
                     'zdata' : component(z),
                     'levels':np.linspace(component(zmin),component(zmax),50), 
                     'plot_function': 'contourf',
                     'xticks' : xticks_args,
                     'title': r'$\mathrm{%s}G(\mathbf{k},\omega)$'%('Re' if comp=='R' else 'Im'), 
                    }
    else: raise Exception("Unknown plot type %s. Can only be 'contourf' (default)."%plot_type)

    default_dict.update(opt_dict)

    return [default_dict]

