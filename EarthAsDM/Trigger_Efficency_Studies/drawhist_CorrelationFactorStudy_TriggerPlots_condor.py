import ROOT as r
import sys
import re
import os
import array
import numpy as np
import argparse
import os.path
import matplotlib.pyplot as plt
import argparse

def loadTree(file_path, tree_name):
    tree = r.TChain(tree_name)
    tree.Add(file_path)
    return tree


def main():


    if len(sys.argv) != 2:
        print("Usage: python3 drawhist_CorrelationFactorStudy_v2.py <file_path>")
        sys.exit(1)

    path = sys.argv[1]

    # Rest of your code
    tree1 = loadTree(os.path.abspath(path), "muonPhiAnalyzer/tree")

    nevents1 = tree1.GetEntries()
    print("nentries1 = ", nevents1)



#########_____________MAKING CUTS PLOTS________________########

    event_count = 0
    pfreq = 1000
    accepted_printed = False
    rejected_printed = False
    correlation_factors = []
    Event_Number = []
    total_events = 0
    # graph = r.TGraph()
    muon_n = []
    muon_phi_test = []
    muon_dtSeg_globY = []
    muon_dtSeg_n =[]


    muon_phi_average =0
    muon_dtSeg_globY_average = 0
    muon_dtSeg_n_average = 0
    DataType = 'test'


    h_muonGlobalYvsTime1 = r.TH2D("h_muonGlobalYvsTime1", "Background MC GlobalY vs time;time[ns];GlobalY", 100, -100, 100, 50, -800, 800)

    # Define variables and correlation factors
    # variables = ["phi", "n", "eta", "pt", "energy", "Chi2", "dtSeg_globZ", "dtSeg_globY", "comb_freeInvBeta", "comb_timeAtIpInOut", "comb_timeAtIpOutIn", "comb_ndof", "tuneP_PtErr", "dtSeg_n"] #, "n" # Add more variables as needed
    # variables = ["muon_pt", "muon_phi", "muon_energy", "muon_eta", "track_pt", "track_eta", "track_phi"] #, "muon_n""dtSeg_n", "phi"] #, "n" # Add more variables as needed
    variables = ["muon_fromGenTrack_Pt", "muon_fromGenTrack_Phi","muon_fromGenTrack_Eta"]
    correlation_factors = ["Positive", "Negative"]  # Add more correlation factors as needed
    chi2_vs_ndof_values = [1]  # Add more cut values as needed
    ndof_values = [1]

    # Create histograms for each combination of variable, correlation factor, and cut

    histograms = {}
    for variable in variables:
        for correlation_factor in correlation_factors:
            # Define the histogram name based on all four components
            # histogram_name = f"h_{variable}_CorrelationFactor_{correlation_factor}_With_cut_on_Chi2/ndof<={cut_value}_and_ndof>{ndof_value}"
            histogram_name = f"No_cuts_{variable}_CorrelationFactor_{correlation_factor}"
            # print(histogram_name)
            # Define the axis limits based on the variable
            if variable == "muon_phi":
                axis_limits = (-4, 4)
            elif variable == "muon_eta":
                axis_limits = (-2.5, 2.5)
            elif variable == "muon_pt":
                axis_limits = (0, 300)
            # elif variable == "pt_extended":
            #     axis_limits = (0, 4000)
            elif variable == "muon_energy":
                axis_limits = (-100, 1000)
            elif variable == "Chi2":
                axis_limits = (0, 100)
            elif variable == "dtSeg_globZ":
                axis_limits = (-1000, 1000)
            elif variable == "dtSeg_globY":
                axis_limits = (-1000, 1000)
            elif variable == "comb_freeInvBeta":
                axis_limits = (-50, 50)
            elif variable == "comb_timeAtIpInOut":
                axis_limits =  (-500, 500)
            elif variable == "comb_timeAtIpOutIn":
                axis_limits = (-500, 500)
            elif variable == "comb_ndof":
                axis_limits = (0, 50)
            elif variable == "muon_n":
                axis_limits = (0, 50)
            elif variable == "tuneP_PtErr":
                axis_limits = (0, 50)
            elif variable == "dtSeg_n":
                axis_limits = (0, 50)
            elif variable == "track_pt":
                axis_limits = (0, 1000)
            else:
                axis_limits = (-1, 1)  # Define defaults for other variables
            
            # Create the histogram
            histogram = r.TH1F(histogram_name, f"Muon {variable} Comparison, {DataType};{variable};yield", 50, axis_limits[0], axis_limits[1])
            histograms[histogram_name] = histogram


    # histograms = {}
    for variable in variables:
        for correlation_factor in correlation_factors:
            for cut_value in chi2_vs_ndof_values:
                for ndof_value in ndof_values:
                    # Define the histogram name based on all four components
                    # histogram_name = f"h_{variable}_CorrelationFactor_{correlation_factor}_With_cut_on_Chi2/ndof<={cut_value}_and_ndof>{ndof_value}"
                    histogram_name = f"{variable}_CorrelationFactor_cut{cut_value}_ndof{ndof_value}_{correlation_factor}"
                    # print(histogram_name)
                    # Define the axis limits based on the variable
                    if variable == "muon_phi":
                        axis_limits = (-4, 4)
                    elif variable == "muon_eta":
                        axis_limits = (-2.5, 2.5)
                    elif variable == "muon_pt":
                        axis_limits = (0, 300)
                    # elif variable == "pt_extended":
                    #     axis_limits = (0, 4000)
                    elif variable == "muon_energy":
                        axis_limits = (-100, 1000)
                    elif variable == "Chi2":
                        axis_limits = (0, 100)
                    elif variable == "dtSeg_globZ":
                        axis_limits = (-1000, 1000)
                    elif variable == "dtSeg_globY":
                        axis_limits = (-1000, 1000)
                    elif variable == "comb_freeInvBeta":
                        axis_limits = (-50, 50)
                    elif variable == "comb_timeAtIpInOut":
                        axis_limits =  (-500, 500)
                    elif variable == "comb_timeAtIpOutIn":
                        axis_limits = (-500, 500)
                    elif variable == "comb_ndof":
                        axis_limits = (0, 50)
                    elif variable == "muon_n":
                        axis_limits = (0, 50)
                    elif variable == "tuneP_PtErr":
                        axis_limits = (0, 50)
                    elif variable == "dtSeg_n":
                        axis_limits = (0, 50)
                    elif variable == "track_pt":
                        axis_limits = (0, 1000)
                    else:
                        axis_limits = (-1, 1)  # Define defaults for other variables
                    
                    # Create the histogram
                    histogram = r.TH1F(histogram_name, f"Muon {variable} Comparison, {DataType};{variable};yield", 50, axis_limits[0], axis_limits[1])
                    
                    # Store the histogram in a dictionary with a unique key
                    # histograms[f"{variable}_{correlation_factor}_cut{cut_value}"] = histogram
                    histograms[histogram_name] = histogram

    # histograms_chi2_ndof = {}
    for correlation_factor in correlation_factors:
        for cut_value in chi2_vs_ndof_values:
            histogram_name = f"h_{correlation_factor}_Chi2_ndof_cut{cut_value}"
            histogram = r.TH1F(histogram_name, f"Chi2/ndof Comparison, {DataType};Chi2/ndof;yield", 50, 0, 20)  # Adjust the axis limits as needed
            histograms[f"{correlation_factor}_Chi2_ndof_cut{cut_value}"] = histogram

    h_muonGlobalYvsTime1CorrelationFactor = r.TH1F("h_muonGlobalYvsTime1CorrelationFactor", "Muon Correlation Factor;Correlation Factor;Yield", 50, -1, 1)
    # histograms["h_muonGlobalYvsTime1CorrelationFactor"] = h_muonGlobalYvsTime1CorrelationFactor

    graph_corr_factor_vs_event = r.TGraph()
    event_number = 0  # Initialize event number
    # print(histograms)
    Positive_correlation_length = 0
    total_events_1 = 0
    total_events_2 = 0



    segment_counting = 0
    variable_counting = 0
    value_counting = 0
    ndof_counting = 0
    value_counting_1 = 0

    chi2_vs_ndof_values_1 = [15]  # Add more cut values as needed
    ndof_values_1 = [15]



    variable_ranges = {
    "muon_phi": (-0.5, 1.5, -4, 4),  # Define the ranges for each variable here
    "muon_n": (-0.5, 1.5, -500, 500),    # Example ranges for variable2
    "muon_eta": (-0.5, 1.5, -2.5, 2.5),  # Example ranges for variable3
    "muon_pt": (-0.5, 1.5, 0, 10000),  # Define the ranges for each variable here
    # "pt_extended":  (-0.5, 1.5, 0, 1000),
    "muon_energy": (-0.5, 1.5, -100, 7000),    # Example ranges for variable2
    "Chi2": (-0.5, 1.5, 0, 100),  # Example ranges for variable3
    "dtSeg_globZ": (-0.5, 1.5, -1000, 1000),  # Define the ranges for each variable here
    "dtSeg_globY": (-0.5, 1.5, -1000, 1000),    # Example ranges for variable2
    "comb_freeInvBeta": (-0.5, 1.5, -50, 50),  # Example ranges for variable3
    "comb_timeAtIpInOut": (-0.5, 1.5, -500, 500),  # Define the ranges for each variable here
    "comb_timeAtIpOutIn": (-0.5, 1.5, -500, 500),    # Example ranges for variable2
    "comb_ndof": (-0.5, 1.5, 0, 50),  # Example ranges for variable3
    "tuneP_PtErr": (-0.5, 1.5, 0, 50),    # Example ranges for variable2
    "dtSeg_n": (-0.5, 1.5, 0, 50),  # Example ranges for variable3
    "track_pt": (-0.5, 1.5, 0, 10000),  # Example ranges for variable3
    "track_phi": (-0.5, 1.5, -4, 4),  # Example ranges for variable3
    "track_eta": (-0.5, 1.5, -2.5, 2.5),  # Example ranges for variable3
    "track_energy": (-0.5, 1.5, 0, 1000),  # Example ranges for variable3
    "muon_fromGenTrack_Pt":(-0.5, 1.5, 0, 10000),
    "muon_fromGenTrack_Phi":(-0.5, 1.5, -4, 4),
    "muon_fromGenTrack_Eta":(-0.5, 1.5, -2.5, 2.5),
    # Add ranges for other variables as needed
}





    # Initialize histograms outside the loops
    n_events = 0
    double_counting = 0
    x = 0
    GenTrackCounting = 0
    GenTrackCounting2 = 0
    GenTrackCounting3 = 0
    value_sum = 0
    z = 0

    for variable in variables:
        # Get the range for the current variable
        range_values = variable_ranges.get(variable, (-0.5, 1.5, -1000, 1000))
        x_min, x_max, y_min, y_max = range_values

        # Create a plot for Trigger_vs_variable with the specified range
        histogram_name = f"Trigger_vs_{variable}"
        trigger_variable_hist = r.TH2D(histogram_name, f"Trigger vs. {variable}", 2, x_min, x_max, 1000, y_min, y_max)
        for event in tree1:
            for i, j, k, l in zip(event.muon_hasMatchedGenTrack, event.muon_fromGenTrack_Pt,event.muon_fromGenTrack_Phi,event.muon_fromGenTrack_Eta):
                if i == True:
                    if variable == 'muon_fromGenTrack_Pt':
                        if event.HLT_L1SingleMuCosmics == 1:
                            trigger_variable_hist.Fill(1, j)
                        elif event.HLT_L1SingleMuCosmics == 0:
                            trigger_variable_hist.Fill(0, j)
                    if variable == 'muon_fromGenTrack_Phi':
                        if event.HLT_L1SingleMuCosmics == 1:
                            trigger_variable_hist.Fill(1, k)
                        elif event.HLT_L1SingleMuCosmics == 0:
                            trigger_variable_hist.Fill(0, k)
                    if variable == 'muon_fromGenTrack_Eta':
                        if event.HLT_L1SingleMuCosmics == 1:
                            trigger_variable_hist.Fill(1, l)
                        elif event.HLT_L1SingleMuCosmics == 0:
                            trigger_variable_hist.Fill(0, l)
 
    output_file = r.TFile("test2.root", "RECREATE")

    for histogram in histograms.values():
        histogram.Write()



    graph_corr_factor_vs_event.Write("graph_corr_factor_vs_event")
    output_file.Close()

if __name__ == "__main__":
     main()
