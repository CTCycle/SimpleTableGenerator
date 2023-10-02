from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ks_2samp


# define class for trained model validation and data comparison
#============================================================================== 
#==============================================================================
#==============================================================================
class DataValidator:
    
    """ 
    DataValidator(dataframe1, dataframe2)
    
    Defines the functions to compare real and synthetic dataframes and evalutate the
    overall quality of the generation process. 
    
    Keyword arguments:    
    dataframe1:  dataframe of real numbers (original dataframe)
    dataframe2:  dataframe of fake numbers (synthetic dataframe)
    
    """    
    
    # comparison of histograms (distributions) by superimposing plots
    #-------------------------------------------------------------------------- 
    def hist_comparison(self, dataframe1, dataframe2, bins):
        
        """ 
        hist_comparison(dataframe1, dataframe2, bins, path)
        
        Plots the histograms of both the real and fake dataframe, column by column,
        using a mild transparency to superimpose them in a clear fashion. Standard
        deviation and mean differences are printed into a text box inside the plot 
        
        Keyword arguments:    
        dataframe1 (pd.dataframe):  dataframe of real numbers (original dataframe)
        dataframe2 (pd.dataframe):  dataframe of fake numbers (synthetic dataframe)
        bins (int):                 number of histogram bins (int)
        path (str):                 figures (.jpeg) folder path
        
        Returns:
        
        None
        
        """
        for (r, f) in tqdm(zip(dataframe1.columns, dataframe2.columns)):
            r_arr = dataframe1[r].values
            f_arr = dataframe2[f].values
            r_mu = r_arr.mean()
            f_mu = f_arr.mean()
            r_sigma = r_arr.std()
            f_sigma = f_arr.std()
            std_check = (abs(r_sigma - f_sigma)/r_sigma)*100
            mean_check = (abs(r_mu - f_mu)/r_mu)*100
            std_check = round(std_check, 2)
            mean_check = round(mean_check, 2)
            text = '''STD diff = {0}%
                      Mean diff = {1}%'''.format(std_check, mean_check) 
            fig, ax = plt.subplots()
            plt.hist(r_arr, bins = bins, alpha=0.5, density = True, label='real data')
            plt.hist(f_arr, bins = bins, alpha=0.5, density = True, label='synthetic data')
            plt.legend(loc='upper right')
            plt.title('Histogram of {}'.format(r))
            plt.xlabel(r, fontsize = 8)
            plt.ylabel('Norm frequency', fontsize = 8) 
            plt.xticks(fontsize = 8)
            plt.yticks(fontsize = 8)
            plt.figtext(0.33, -0.02, text, ha = 'right') 
            plt.tight_layout()           
            
            return fig
    
    # comparison of data distribution using statistical methods 
    #-------------------------------------------------------------------------- 
    def KS_test(self, dataframe1, dataframe2):
        
        """ 
        data_check(dataframe1, dataframe2, path)
        
        Check the similarity beteween the real and synthetic data using the 
        Kolmogorov-Smirnoff test to compare the cumulative distribution functions 
        of the dataseries. The P value list for all dataframe columns is generated 
        and called as self.pv_list.  
        
        Keyword arguments:  
            
        dataframe1 (pd.dataframe):  dataframe of real numbers (original dataframe)
        dataframe2 (pd.dataframe):  dataframe of fake numbers (synthetic dataframe)
        path (str):                 figures (.jpeg) folder path
        
        Returns:
            
        None
        
        """
        self.pv_list = []
        self.real_list = []
        self.fake_list = [] 
        for col1, col2 in zip(dataframe1.columns, dataframe2.columns):
            array = dataframe1[col1].values
            self.real_list.append(array)
            array = dataframe2[col2].values        
            self.fake_list.append(array)
        for (r, f, t) in tqdm(zip(self.real_list, self.fake_list, dataframe1.columns)):
            ry, rx = np.histogram(r, bins = 'auto')
            sy, sx = np.histogram(f, bins = 'auto')
            real_cumsum = np.cumsum(ry)
            fake_cumsum = np.cumsum(sy)
            norm_real_cumsum = [x/real_cumsum[-1] for x in real_cumsum]
            norm_fake_cumsum = [x/fake_cumsum[-1] for x in fake_cumsum]
            statistic, p_value = ks_2samp(real_cumsum, fake_cumsum, 
                                          alternative = 'two-sided')
            statistic = round(statistic, 2)
            p_value = round(p_value, 3)
            self.pv_list.append(p_value)
            text = '''Statistics = {0}%
                      P value = {1}'''.format(statistic, p_value)
            fig, ax = plt.subplots()   
            plt.plot(rx[:-1], norm_real_cumsum, c = 'blue', label = 'real data')
            plt.plot(sx[:-1], norm_fake_cumsum, c = 'orange', label = 'synthetic data')
            plt.xlabel(t, fontsize = 8)
            plt.ylabel('Cumulative norm frequency', fontsize = 8) 
            plt.xticks(fontsize = 8)
            plt.yticks(fontsize = 8)
            plt.legend(loc='upper left')
            plt.title('CDF of {}'.format(t))
            plt.figtext(0.33, -0.02, text, ha = 'right')
            plt.tight_layout()                        
        self.desc_list = []        
        for f in self.pv_list:
            if f >= 0.05:
                desc = 'Generated distribution is not equal'
            else:
                desc = 'Generated distribution is equal'
            self.desc_list.append(desc)

            return fig
            
# define class for correlations calculations
#==============================================================================
#==============================================================================
#==============================================================================
class MultiCorrelator:
    
    """ 
    MultiCorrelator(dataframe)
    
    Calculates the correlation matrix of a given dataframe using specific methods.
    The internal functions retrieves correlations based on Pearson, Spearman and Kendall
    methods. This class is also used to plot the correlation heatmap and filter correlations
    from the original matrix based on given thresholds. Returns the correlation matrix
    
    Keyword arguments: 
        
    dataframe (pd.dataframe): target dataframe
    
    Returns:
        
    df_corr (pd.dataframe): correlation matrix in dataframe form
                
    """
   
    # Spearman correlation calculation
    #--------------------------------------------------------------------------
    def Spearman_corr(self, dataframe, decimals):
        df_corr = dataframe.corr(method = 'spearman').round(decimals)
        return df_corr
    
    # Kendall correlation calculation
    #--------------------------------------------------------------------------    
    def Kendall_corr(self, dataframe, decimals):
        df_corr = dataframe.corr(method = 'kendall').round(decimals)
        return df_corr
    
    # Pearson correlation calculation
    #--------------------------------------------------------------------------    
    def Pearson_corr(self, dataframe, decimals):
        df_corr = dataframe.corr(method = 'pearson').round(decimals)
        return df_corr
    
    # plotting correlation heatmap using seaborn package
    #--------------------------------------------------------------------------
    def corr_heatmap(self, matrix, name):
        
        """ 
        corr_heatmap(matrix, path, dpi, name)
        
        Plot the correlation heatmap using the seaborn package. The plot is saved 
        in .jpeg format in the folder that is specified through the path argument. 
        Output quality can be tuned with the dpi argument.
        
        Keyword arguments:    
            
        matrix (pd.dataframe): target correlation matrix
        path (str):            picture save path for the .jpeg file
        dpi (int):             value to set picture quality when saved (int)
        name (str):            name to be added in title and filename
        
        Returns:
            
        None
            
        """
        cmap = 'YlGnBu'
        fig = sns.heatmap(matrix, square = True, annot = False, 
                          mask = False, cmap = cmap, yticklabels = False, 
                          xticklabels = False)
        plt.title('{}_correlation_heatmap'.format(name))
        plt.tight_layout()        
                
        return fig
        
    # plotting correlation heatmap of two dataframes
    #--------------------------------------------------------------------------
    def double_corr_heatmap(self, matrix_real, matrix_fake):        
        
        """ 
        double_corr_heatmap(matrix_real, matrix_fake, path, dpi)
        
        Plot the correlation heatmap of two dataframes using the seaborn package. 
        The plot is saved in .jpeg format in the folder specified through the path argument. 
        Output quality can be tuned with the dpi argument.
        
        Keyword arguments:
            
        matrix_real (pd.dataframe): real data correlation matrix
        matrix_fake (pd.dataframe): fake data correlation matrix
        path (str):                 picture save path for the .jpeg file
        dpi (int):                  value to set picture quality when saved (int)
        
        Returns:
            
        None
        
        """ 
        plt.subplot(2, 1, 1)
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(matrix_real, square=True, annot=False, mask = False, 
                    cmap=cmap, yticklabels=False, xticklabels=False)
        plt.title('Real data')
        plt.subplot(2, 1, 2)
        sns.heatmap(matrix_fake, square=True, annot=False, mask = False, 
                    cmap=cmap, yticklabels=False, xticklabels=False)
        plt.title('Synthetic data')
        plt.tight_layout()

        fig = plt.gcf()

        return fig        
        
     
    # filtering of correlation pairs based on threshold value. Strong, weak and null
    # pairs are isolated and embedded into output lists
    #--------------------------------------------------------------------------    
    def corr_filter(self, matrix, threshold): 
        
        """
        corr_filter(matrix, path, dpi)
        
        Generates filtered lists of correlation pairs, based on the given threshold.
        Weak correlations are those below the threshold, strong correlations are those
        above the value and zero correlations identifies all those correlation
        with coefficient equal to zero. Returns the strong, weak and zero pairs lists
        respectively.
        
        Keyword arguments:    
        matrix (pd.dataframe): target correlation matrix
        threshold (float):     threshold value to filter correlations coefficients
        
        Returns:
            
        strong_pairs (list): filtered strong pairs
        weak_pairs (list):   filtered weak pairs
        zero_pairs (list):   filtered zero pairs
                       
        """        
        self.corr_pairs = matrix.unstack()
        self.sorted_pairs = self.corr_pairs.sort_values(kind="quicksort")
        self.strong_pairs = self.sorted_pairs[(self.sorted_pairs) >= threshold]
        self.strong_pairs = self.strong_pairs.reset_index(level = [0,1])
        mask = (self.strong_pairs.level_0 != self.strong_pairs.level_1) 
        self.strong_pairs = self.strong_pairs[mask]        
        self.weak_pairs = self.sorted_pairs[(self.sorted_pairs) >= -threshold]
        self.weak_pairs = self.weak_pairs.reset_index(level = [0,1])
        mask = (self.weak_pairs.level_0 != self.weak_pairs.level_1) 
        self.weak_pairs = self.weak_pairs[mask]        
        self.zero_pairs = self.sorted_pairs[(self.sorted_pairs) == 0]
        self.zero_pairs = self.zero_pairs.reset_index(level = [0,1])
        mask = (self.zero_pairs.level_0 != self.zero_pairs.level_1) 
        self.zero_pairs_P = self.zero_pairs[mask]
        
        return self.strong_pairs, self.weak_pairs, self.zero_pairs
