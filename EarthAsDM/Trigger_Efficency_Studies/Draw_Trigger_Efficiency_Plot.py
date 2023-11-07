import ROOT as r
import os
import array
import numpy as np
import argparse
import os.path
import matplotlib.pyplot as plt
# from Plotting_onTop_Functions import overlay_histograms, find_largest_bin_size

def generate_histogram_names(variables, ndof_cuts, chi2_cuts, correlation_factors):
    histogram_names = []

    for variable in variables:
        for ndof_cut in ndof_cuts:
            for chi2_cut in chi2_cuts:
                for correlation_factor in correlation_factors:
                    histogram_name = f'{variable}_CorrelationFactor_cut{chi2_cut}_ndof{ndof_cut}_{correlation_factor}'
                    histogram_names.append(histogram_name)
    for variable in variables:
        for correlation_factor in correlation_factors:
            histogram_name = f'No_cuts_{variable}_CorrelationFactor_{correlation_factor}'
            histogram_names.append(histogram_name)

    return histogram_names

def generate_histogram_names_2(variables, ndof_cuts, chi2_cuts):
    histogram_names = []
    for variable in variables:
        # histogram_name = f'Trigger_vs_{variable}_pfy_px'
        histogram_name = f'Trigger_vs_{variable}'
        histogram_names.append(histogram_name)

    for variable in variables:
        for ndof_cut in ndof_cuts:
            for chi2_cut in chi2_cuts:
                histogram_name = f'Trigger_vs_{variable}_Chi2_{chi2_cut}_ndof_{ndof_cut}_pfy_px'
                histogram_names.append(histogram_name)

    return histogram_names

def generate_histogram_names_3(variables):
    histogram_names = []
    for variable in variables:
        # histogram_name = f'Trigger_vs_{variable}_pfy_px'
        histogram_name = f'Trigger_vs_{variable}'
        histogram_names.append(histogram_name)

    return histogram_names

# Example usage:
# create_trigger_vs_energy_plot("your_root_file.root", "plots/test4/Background_TriggerEfficency_Energy.png")
def create_trigger_vs_Variable_TProfile(root_file_path, output_folder, histogram_names, output_file_name, Title):
    # Open the ROOT file
    root_file = r.TFile.Open(root_file_path, "READ")
    print("This is root_file", root_file)

    print(f"Contents of the ROOT file: {root_file_path}")
    root_file.ls()
    if not root_file or root_file.IsZombie():
        print(f"Error: Unable to open or invalid ROOT file {root_file_path}")
        return
    output_file_name = f"Total3.root"
    output_file_path = os.path.join(output_folder, output_file_name)
    output_file = r.TFile.Open(output_file_path, "UPDATE")
    for hist_name in histogram_names:
        # Check if the histogram exists in the ROOT file
        if not root_file.Get(hist_name):
            print(f"Error: Histogram '{hist_name}' not found in the ROOT file.")
            continue

        # Get the histogram from the ROOT file
        histogram = root_file.Get(hist_name)
        print("This is GetEntries1:",histogram.GetEntries())

        # Rebin the histogram
        histogram.RebinY(10)
        print("This is GetEntries2:",histogram.GetEntries())

        numXbins = histogram.GetNbinsY()
        print(f"Number of X bins: {numXbins}")

        # Create a profile histogram
        profile = histogram.ProfileY()
        print("This is GetEntries3:",profile.GetEntries())

        # Project the X-axis
        profile = profile.ProjectionX()

        # Set X-axis range and Y-axis range
        profile.GetXaxis().SetRange(1, profile.GetNbinsX() + 1)
        profile.GetYaxis().SetRangeUser(0., 1.)
        profile.Write(f"{Title}_{hist_name}")

        # # Save the plot as an image file
        # output_file_name = f"{Title}_{hist_name}.root"
        # output_file_path = os.path.join(output_folder, output_file_name)

        # # Save the profile histogram to the ROOT file
        # output_file = r.TFile.Open(output_file_path, "RECREATE")
        # profile.Write()
    output_file.Close()

    # Close the ROOT file
    root_file.Close()




def main():
    # Define your criteria
    variables = ['muon_fromGenTrack_Pt','muon_fromGenTrack_Phi','muon_fromGenTrack_Eta']#"phi", "n", "eta", "pt", "energy", "Chi2", "dtSeg_globZ", "dtSeg_globY", "comb_freeInvBeta", "comb_timeAtIpInOut", "comb_timeAtIpOutIn", "comb_ndof", "tuneP_PtErr", "dtSeg_n"] #"dtSeg_globZ", "dtSeg_globY", "comb_freeInvBeta", "comb_timeAtIpInOut", "comb_timeAtIpOutIn", "comb_ndof", "tuneP_PtErr",]  # Specify the variables you want
    ndof_cuts = ['15']  # Specify the ndof cuts you want
    chi2_cuts = ['15']  # Specify the chi2 cuts you want
    correlation_factors = ['Positive', 'Negative']  # Specify the correlation factors you want

    ###Background Settings
    # root_file_path_background = '/Users/lbrennan/Documents/Research/CMS/Coding/15-Creating_Trigger_Plots_for_AN/RootFiles/Cosmics_Total_Background_trigger_v2.root'
    # output_folder_background = '/Users/lbrennan/Documents/Research/CMS/Coding/15-Creating_Trigger_Plots_for_AN/RootFiles/pngs2'
    # output_file_name_background = 'Background'
    # Background_Title = ''    

    #### High energy signal
    root_file_path_HighEnergySignal = '/Users/lbrennan/Documents/Research/CMS/Coding/17-FixingTriggerPlots/500Gev_Monoenergetic_Signal_total.root'
    output_folder_HighEnergySignal = '/Users/lbrennan/Documents/Research/CMS/Coding/17-FixingTriggerPlots/pngs'
    output_file_name_HighEnergySignal = 'High_Energy_signal'
    HighEnergy_Title = 'High_Energy_signal'

    ###Low Energy signal
    # root_file_path_LowEnergySignal = '/Users/lbrennan/Documents/Research/CMS/Coding/15-Creating_Trigger_Plots_for_AN/RootFiles/Cosmics_Total_LowEnergy_Comparison_v2.root'
    # output_folder_LowEnergySignal = '/Users/lbrennan/Documents/Research/CMS/Coding/15-Creating_Trigger_Plots_for_AN/RootFiles/pngs4'
    # output_file_name_LowEnergySignal = 'Low_Energy_signal'
    # LowEnergy_Title = 'Low_Energy_signal'

    ###Signal 
    # root_file_path_Signal = '/Users/lbrennan/Documents/Research/CMS/Coding/15-Creating_Trigger_Plots_for_AN/RootFiles/Cosmics_Total_signal_Comparison_Trigger_v2.root'
    # output_folder_Signal = '/Users/lbrennan/Documents/Research/CMS/Coding/15-Creating_Trigger_Plots_for_AN/RootFiles/pngs4'
    # output_file_name_Signal = 'Signal'
    # Signal_Title = 'Signal

    ###Create the histograms
    histogram_names_3 = generate_histogram_names_3(variables)

    ###Background
    # create_trigger_vs_Variable_TProfile(root_file_path_background, output_folder_background, histogram_names_3, output_file_name_background, Background_Title)

    ### High Energy Signal
    create_trigger_vs_Variable_TProfile(root_file_path_HighEnergySignal, output_folder_HighEnergySignal,histogram_names_3,output_file_name_HighEnergySignal, HighEnergy_Title)

    ###Low Energy Signal
    # create_trigger_vs_Variable_TProfile(root_file_path_LowEnergySignal, output_folder_LowEnergySignal,histogram_names_3,output_file_name_LowEnergySignal, )

    ###Signal
    # create_trigger_vs_Variable_TProfile(root_file_path_Signal,output_folder_Signal,histogram_names_3,output_file_name_Signal, 100, 'Signal')


if __name__ == "__main__":
    main()


