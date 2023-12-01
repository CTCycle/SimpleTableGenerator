import os
import sys
import random
import numpy as np
import pandas as pd
import PySimpleGUI as sg

# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# import modules and classes
#------------------------------------------------------------------------------ 
from modules.components.data_classes import DataSetFinder, DataGenerator
import modules.global_variables as GlobVar

# [WINDOW THEME AND OPTIONS]
#==============================================================================
initial_folder = os.path.dirname(os.path.realpath(__file__))
sg.theme('LightGrey1')
sg.set_options(font = ('Arial', 11), element_padding = (6,6))

# [LAYOUT OF THE FILE SELECTION FRAME]
#==============================================================================
list_of_files = GlobVar.list_of_files
input_text = sg.Text('Input folder', font = ('Arial', 12), size = (10,1))
dd_text = sg.Text('List of files', font = ('Arial', 12), size = (10,1))
input_path = sg.Input(enable_events=True, key= '-PATHINPUT-', size = (70,1))
input_browser = sg.FolderBrowse(initial_folder = initial_folder, key = '-INBROWSER-')
dropdown = sg.DropDown(list_of_files, size = (20, 1), key = '-DROPDOWN-', expand_x = True, enable_events=True)
path_frame = sg.Frame('Select folder path', layout = [[input_text, input_path, input_browser], [dd_text, dropdown]],
                                                       expand_x=True)

# [LAYOUT OF FILE SAVING FRAME]
#==============================================================================
save_button = sg.Button('Save', key = '-SAVE-', disabled=True)
path_input = sg.Input(key = '-SAVEPATH-', expand_x = True, enable_events=True)
folder_browse = sg.FolderBrowse(initial_folder = initial_folder)
save_frame = sg.Frame('Save file', layout = [[path_input, folder_browse, save_button]], expand_x=True)

# [LAYOUT OF THE WINDOW]
#==============================================================================
main_text = sg.Text('Placeholder text', font = ('Arial', 12), size = (50,1))
CDF_button = sg.Button('Cumulative Distribution Function (CDF)', expand_x=True, key = '-CDF-', disabled=True)
kernel_button = sg.Button('Kernel Sampling (KS)', expand_x=True, key = '-KERNEL-', disabled=True)
dist_button = sg.Button('Theoretical Distribution Fitting (TDF)', expand_x=True, key = '-TDF-', disabled=True)
validate_button = sg.Button('Data Validation', expand_x=True, key = '-VALID-', disabled=True)
input_text = sg.Text('Number of synthetic values to generate', font = ('Arial', 12), size = (30,1))
num_input = sg.Input(key = '-NUMVAL-', size = (30,1), enable_events=True)
left_column = sg.Column([[input_text], [num_input]])
right_column = sg.Column([[CDF_button], [kernel_button], [dist_button], [validate_button]], expand_x=True)
progress_bar = sg.ProgressBar(100, orientation = 'horizontal', size = (50, 20), key = '-PBAR-', expand_x=True)
main_layout = [[main_text],
               [path_frame],
               [sg.HSeparator()],
               [left_column, right_column],
               [sg.HSeparator()],               
               [save_frame],
               [progress_bar]]              

# [WINDOW LOOP]
#==============================================================================
main_window = sg.Window('Simple table generator V1.0', main_layout, 
                        grab_anywhere = True, resizable = True, finalize = True)
while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED:
        break 

    # [SELECT FILES USING DROPDOWN MENU]
    #==========================================================================
    if event == '-DROPDOWN-':
        target_file = values['-DROPDOWN-'] 
        file_name = target_file.split('.')[0]
        GlobVar.file_name = file_name
        folder_path = values['-PATHINPUT-']     
        filepath = os.path.join(folder_path, target_file)        
        df = pd.read_csv(filepath, sep= ';', encoding='utf-8')
        GlobVar.dataframe = df        
        if values['-NUMVAL-'].isdigit():
            main_window['-CDF-'].update(disabled = False)  
            main_window['-KERNEL-'].update(disabled = False) 
            main_window['-TDF-'].update(disabled = False)         

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-PATHINPUT-':
        path = values['-PATHINPUT-']
        dataset_inspector = DataSetFinder(path)
        list_of_files = dataset_inspector.target_files
        GlobVar.list_of_files = list_of_files
        main_window['-DROPDOWN-'].update(values = list_of_files)

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-NUMVAL-':
        if values['-NUMVAL-'].isdigit() and values['-PATHINPUT-']:
            main_window['-CDF-'].update(disabled = False)  
            main_window['-KERNEL-'].update(disabled = False) 
            main_window['-TDF-'].update(disabled = False) 
        else: 
            main_window['-CDF-'].update(disabled = True)  
            main_window['-KERNEL-'].update(disabled = True) 
            main_window['-TDF-'].update(disabled = True)     

    # [CUMULATIVE DISTRIBUTION FUNCTION]
    #==========================================================================
    if event == '-CDF-':                
        num_values = int(values['-NUMVAL-'])
        generator = DataGenerator()
        df = GlobVar.dataframe
        df_synthetic = generator.CDF_generator(df, num_values, progress_bar)          
        GlobVar.synthetic_dataframe = df_synthetic
        folder_path = values['-SAVEPATH-']
        save_path = os.path.join(folder_path, 'CDF_synthetic_{}.csv'.format(file_name))
        df_synthetic.to_csv(save_path, index = False, sep = ';', encoding = 'utf-8') 
        main_window['-VALID-'].update(disabled = False)           

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-KERNEL-':        
        num_entries = int(values['-NUMVAL-'])        
        rand = np.random.RandomState(42)
        dist_list = ['uniform','normal','exponential','lognormal','chisquare','beta']
        KDE_sampling = DataGenerator() 
        synthetic_data = KDE_sampling.KDE_generator(df, num_entries, 42)
        synthetic_df = pd.DataFrame(synthetic_data).T
        GlobVar.synthetic_dataframe = df_synthetic
        folder_path = values['-SAVEPATH-']
        save_path = os.path.join(folder_path, 'KDE_synthetic__{}.csv'.format(file_name))
        df_synthetic.to_csv(save_path, index = False, sep = ';', encoding = 'utf-8')  
        main_window['-VALID-'].update(disabled = False) 

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-TDF-':
        random.seed(42) 
        num_entries = int(values['-NUMVAL-'])
        distfit_sampling = DataGenerator() 
        synthetic_data = distfit_sampling.dist_fitter(df, num_entries, progress_bar)
        synthetic_df = pd.DataFrame(synthetic_data).T
        GlobVar.synthetic_dataframe = synthetic_df
        folder_path = values['-SAVEPATH-']
        save_path = os.path.join(folder_path, 'TDF_synthetic_{}.csv'.format(file_name))
        df_synthetic.to_csv(save_path, index = False, sep = ';', encoding = 'utf-8')
        main_window['-VALID-'].update(disabled = False)

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-VALID-':
        import modules.data_validation
        del sys.modules['modules.data_validation']   

main_window.close()
    

