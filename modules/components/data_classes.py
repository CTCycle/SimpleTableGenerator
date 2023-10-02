import os
from tqdm import tqdm
import numpy as np
import random
from distfit import distfit
import pandas as pd
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

    
# define the class for inspection of the input folder and generation of files list.
# The extension as argument allows identifying specific files (.csv, .xlsx, .pdf, etc)
# and making a list of those than can be called with the 'target_files' method
#==============================================================================
#==============================================================================
#==============================================================================
class DataSetFinder:
    
    """ 
    DatasetFinder(path, ext)
    
    Creates a list of files with given extension from the argument path, if the
    list is empty because no files were found, then the emtpy_folder variable is
    set to True
    
    Keyword arguments:
        
    path (str): path of the folder that has to be scanned for files    
    ext (str):  the target files extension (.csv, .jpeg, .pdf, etc)
    
    Returns:
        
    None 
    
    """
    def __init__(self, path):        
        self.path = path
        extensions = ('.csv', '.xlsx')
        os.chdir(path)
        self.all_files = os.listdir(path)
        self.target_files = [f for f in self.all_files if f.endswith(extensions)]   
    
    
# define class for generation of synthetic values
#==============================================================================
#==============================================================================
#==============================================================================
class DataGenerator:
    
    """ 
    DataGenerator()
    
    Defines the ensembles of generator methods to produce syntethic dataframes,
    based on the original set of data. Different methodologies include CDF sampling,
    data fitting with standard distribution models and KDE models. Dataseries are
    generated as disjointed distributions.
       
    """      
        
    # generator of synthetic numbers based on CDF sampling
    #==========================================================================
    def CDF_generator(self, dataframe, num_val, pbar):
        
        """ 
        CDF_generator(dataframe, num_val):
        
        Generates synthetic numbers using the CDF of the original dataframe as input,
        and sampling randomly to reproduce the reference distribution (disjointed).
        
        
        Keyword arguments:  
            
        dataframe (pd.dataframe): dataframe of real numbers (original dataframe)
        num_val (int):            number of synthetic values to be generated (int)
        
        Returns: 
            
        fake_list (list): list of lists with synthetic data
        
        """ 
        dataframe_numeric = dataframe.select_dtypes(include = np.number)
        fake_list = []
        real_list = []
        for id, col in enumerate(dataframe_numeric.columns):            
            array = dataframe_numeric[col].values
            real_list.append(array)
            x = np.sort(array)
            n = x.size
            y = np.arange(1, n+1)/n
            synth_cols = []
            for num in range(num_val):
                randomizer = random.random()
                numy = np.interp(randomizer, y, x)
                synth_cols.append(numy)
            fake_list.append(synth_cols)
            pbar.update(id + 1, max=dataframe_numeric.shape[1])
        fake_df = pd.DataFrame(fake_list).T
        fake_df.columns = dataframe_numeric.columns
            
        return fake_df                
     
    
    # generator of synthetic numbers based on theoretical distribution fitting
    #--------------------------------------------------------------------------
    def dist_fitter(self, dataframe, num_val, pbar):
        
        """ 
        dist_fitter(dataframe, num_val):
        
        Generates synthetic numbers by fitting theoretical models to the original
        dataframe and generating new distribution with the best fitting model, based
        on the distift package. 
        
        Keyword arguments:  
            
        dataframe (pd.dataframe): dataframe of real numbers (original dataframe)
        num_val (int):            number of synthetic values to be generated (int)
        
        Returns: 
            
        fake_list (list): list of lists with synthetic data
        
        """
        dataframe_numeric = dataframe.select_dtypes(include = np.number)
        fake_list = []
        real_list = []
        for id, col in enumerate(dataframe_numeric.columns):            
            array = dataframe_numeric[col].values
            real_list.append(array)
            model= distfit(bound='both')
            model.fit_transform(array, verbose = 0)
            Xgen = model.generate(n = num_val).round(0)
            fake_list.append(Xgen)
            pbar.update(id + 1, max=dataframe_numeric.shape[1])
            
        fake_df = pd.DataFrame(fake_list).T
        fake_df.columns = dataframe_numeric.columns
            
        return fake_df    
    
    # generator of synthetic numbers based on Kernel models (KDE)
    #--------------------------------------------------------------------------
    def KDE_generator(self, dataframe, num_val, seed):
        
        """ 
        KDE_generator(dataframe, num_val, seed):
        
        Generates synthetic numbers using the Kernel methodologies of neighbour
        numbers. The bandwidth is selected through an initialization process (may
        take long time to finish).        
        
        Keyword arguments:    
        dataframe (pd.dataframe): dataframe of real numbers (original dataframe)
        seed (int):               seed for random number generation
        num_val (int):            number of synthetic values to be generated (int)
        
        Returns: 
        fake_list (list): list of lists with synthetic data
        
        """
        self.rand = np.random.RandomState(seed)
        self.dist_list = ['uniform','normal','exponential',
                          'lognormal','chisquare','beta']
        self.kernels = ['cosine', 'epanechnikov', 'exponential', 
                        'gaussian', 'linear', 'tophat'] 
        self.dataframe_numeric = self.dataframe.select_dtypes(include = np.number)
        self.fake_list =  []
        self.real_list = []
        for col in tqdm(self.dataframe_numeric.columns):    
            array = self.dataframe_numeric[col].values    
            self.real_list.append(array)            
            grid = GridSearchCV(KernelDensity(),
                            {'bandwidth': np.linspace(0.1, 1.0, 30)},
                            cv=20) 
            grid.fit(array[:, None])
            kde = grid.best_estimator_
            synth_array = kde.sample(num_val, random_state=seed)
            self.fake_list.append(synth_array)
            
        return self.fake_list 
    
    
