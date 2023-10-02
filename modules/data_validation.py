import os
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import warnings
warnings.simplefilter(action='ignore', category = DeprecationWarning)
warnings.simplefilter(action='ignore', category = FutureWarning)

# [IMPORT MODULES AND CLASSES]
#==============================================================================
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.components.validation_classes import DataValidator, MultiCorrelator
import modules.global_variables as GlobVar

# [GLOBAL VARIABLES]
#==============================================================================
file_name = GlobVar.file_name
df = GlobVar.dataframe
df_synthetic = GlobVar.synthetic_dataframe
canvas_draw = False 

# [WINDOW THEME AND OPTIONS]
#==============================================================================
sg.theme('LightGrey1')
sg.set_options(font = ('Arial', 11), element_padding = (6,6))

# [LAYOUT OF FILE SAVING FRAME]
#==============================================================================
save_button = sg.Button('Save', key = '-SAVE-', disabled=True)
path_input = sg.Input(key = '-SAVEPATH-', expand_x = True, enable_events=True)
folder_browse = sg.FolderBrowse()
save_frame = sg.Frame('Save file', layout = [[path_input, folder_browse, save_button]],
                      expand_x=True)

# [LAYOUT OF THE ANALYSIS FRAME]
#==============================================================================
hist_button = sg.Button('Histogram analysis', key = '-HISTOGRAM-', expand_x= True)
KS_button = sg.Button('Kolmogorov-Smirnoff Test', key = '-KSTEST-', expand_x= True)
corr_button = sg.Button('Correlations analysis', key = '-CORRELATIONS-', expand_x= True)
analysis_frame = sg.Frame('Set of analytical tecnhiques', layout = [[hist_button], [KS_button], [corr_button]],
                           expand_x=True)

# [LAYOUT OF THE WINDOW]
#==============================================================================
main_text = sg.Text('Placeholder text', font = ('Arial', 12), size = (50,1))
canvas = sg.Canvas(key='-CANVAS-', size = (700, 600), expand_x=True)
left_column = sg.Column([[analysis_frame]])
right_column = sg.Column([[canvas]])
main_layout = [[main_text],
               [sg.HSeparator()],
               [left_column, sg.VSeparator(), right_column],
               [sg.HSeparator()],
               [save_frame]]              

# [WINDOW LOOP]
#==============================================================================
validation_window = sg.Window('Simple table generator V1.0', main_layout, 
                               grab_anywhere = True, finalize = True)
while True:
    event, values = validation_window.read()
    if event == sg.WIN_CLOSED:
        break   

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-HISTOGRAM-': 
        if canvas_draw == True:
            fig_canvas.get_tk_widget().pack_forget()
            canvas_draw = False
        validation = DataValidator()
        figure = validation.hist_comparison(df, df_synthetic, 'auto')           
        fig_canvas = FigureCanvasTkAgg(figure, master = validation_window['-CANVAS-'].TKCanvas)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side='top', fill='none', expand=False)
        canvas_draw = True 

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-KSTEST-':         
        if canvas_draw == True:
            fig_canvas.get_tk_widget().pack_forget()
            canvas_draw = False 
        figure = validation.KS_test(df, df_synthetic)
        pv_list = validation.pv_list
        real_list = validation.real_list
        fake_list = validation.fake_list  
        desc_list = validation.desc_list 
        fig_canvas = FigureCanvasTkAgg(figure, master = validation_window['-CANVAS-'].TKCanvas)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side='top', fill='none', expand=False)
        canvas_draw = True 

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-CORRELATIONS-':
        validation_window['-CANVAS-'].update(visible=True)
        if canvas_draw == True:
            fig_canvas.get_tk_widget().pack_forget()
            canvas_draw = False 
        regressor = MultiCorrelator()        
        df_corr_real = regressor.Spearman_corr(df, 2)
        df_corr_synth = regressor.Spearman_corr(df_synthetic, 2)
        figure = regressor.double_corr_heatmap(df_corr_real, df_corr_synth) 
        fig_canvas = FigureCanvasTkAgg(figure, master = validation_window['-CANVAS-'].TKCanvas)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side='top', fill='both', expand=True) 
        canvas_draw = True
        
validation_window.close()


