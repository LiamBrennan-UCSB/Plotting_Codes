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
def draw2DHistNoLegend(hist1, title): #x1,x2,y1,y2):

    can = r.TCanvas()
    can.Draw()
    hist1.SetLineColor(r.kRed)
    hist1.SetTitle(title)
    #hist1.SetStats(0);
    hist1.Draw("COLZ")


    # can.SaveAs(f"plots/2DHistTest1/{title}_both.pdf")
    can.SaveAs(f"plots/{title}_both.png")

    return can

def draw2DHistToRootFile(hist1, title, root_file):
    # Create a TCanvas
    can = r.TCanvas()
    can.Draw()

    # Set properties of the histogram
    hist1.SetLineColor(r.kRed)
    hist1.SetTitle(title)

    # Draw the 2D histogram
    hist1.Draw("COLZ")

    # Save the canvas as a TImage object in the ROOT file
    can.Write(title)  # Use the title as the object name in the ROOT file

def combine2DHistograms(hist_list):
    # Initialize a histogram with the same binning as the first input histogram
    merged_hist = hist_list[0].Clone("Merged2DHist")

    # Loop over the remaining histograms and add their contents to the merged histogram
    for hist in hist_list[1:]:
        merged_hist.Add(hist)

    return merged_hist



def main():
    ####Background
    # path = f"/Users/lbrennan/Documents/Research/CMS/Coding/11-Debugging/RootFiles_1/0to75Theta_3to4000GeV_v1_10.root"
    # path = f"/Users/lbrennan/Documents/Research/CMS/Coding/11-Debugging/RootFiles_1/0to75Theta_3to4000GeV_v1_Total.root"



    #####Signal
    # path = f"/Users/lbrennan/Documents/Research/CMS/Coding/11-Debugging/RootFiles_1/test_10.root"
    # path = f"/Users/lbrennan/Documents/Research/CMS/Coding/11-Debugging/RootFiles_1/Signal_Total_v1.root"


    # # path = f"/Users/lbrennan/Documents/Research/CMS/Coding/11-Debugging/RootFiles_1/Cosmics_Total_Background_v1.root"
    # tree1 = loadTree(path, "muonPhiAnalyzer/tree")
    # print(tree1)

    # nevents1 = tree1.GetEntries()
    # print("nentries1 = ", nevents1)

    if len(sys.argv) != 2:
        print("Usage: python3 drawhist_CorrelationFactorStudy_v2.py <file_path>")
        sys.exit(1)

    path = sys.argv[1]

    # Rest of your code
    tree1 = loadTree(os.path.abspath(path), "muonPhiAnalyzer/tree")

    nevents1 = tree1.GetEntries()
    print("nentries1 = ", nevents1)



    # for event in tree1:
    #     print(event.muon_pt)
    #     print("This is pt length:",len(event.muon_pt))
    #     pt_length_1 = len(event.muon_pt)
    #     pt_length =+ pt_length_1 + pt_length
    #     print("This is pt_length", pt_length)
    #     print("This is phi length:",len(event.muon_phi))
    #     print("This is eta length:",len(event.muon_eta))
    #     print("This is dtSeg_globZ length:",len(event.muon_dtSeg_globZ))
    #     print("This is dtSeg_globY length:",len(event.muon_dtSeg_globY))
    #     print("This is comb_timeAtIpInOut length:",len(event.muon_comb_timeAtIpInOut))
    #     # print("This is total_events:",total_events)
    #     event_number_0 += 1
    #     print("This is event_number_0:", event_number_0)




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
    variables = ["pt", "phi", "energy", "eta", "n"] #, "dtSeg_n", "phi"] #, "n" # Add more variables as needed
    correlation_factors = ["Positive", "Negative"]  # Add more correlation factors as needed
    chi2_vs_ndof_values = [15]  # Add more cut values as needed
    ndof_values = [15]

    # Create histograms for each combination of variable, correlation factor, and cut

    histograms = {}
    for variable in variables:
        for correlation_factor in correlation_factors:
            # Define the histogram name based on all four components
            # histogram_name = f"h_{variable}_CorrelationFactor_{correlation_factor}_With_cut_on_Chi2/ndof<={cut_value}_and_ndof>{ndof_value}"
            histogram_name = f"No_cuts_{variable}_CorrelationFactor_{correlation_factor}"
            # print(histogram_name)
            # Define the axis limits based on the variable
            if variable == "phi":
                axis_limits = (-4, 4)
            elif variable == "eta":
                axis_limits = (-2.5, 2.5)
            elif variable == "pt":
                axis_limits = (0, 300)
            # elif variable == "pt_extended":
            #     axis_limits = (0, 4000)
            elif variable == "energy":
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
            elif variable == "n":
                axis_limits = (0, 50)
            elif variable == "tuneP_PtErr":
                axis_limits = (0, 50)
            elif variable == "dtSeg_n":
                axis_limits = (0, 50)
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
                    if variable == "phi":
                        axis_limits = (-4, 4)
                    elif variable == "eta":
                        axis_limits = (-2.5, 2.5)
                    elif variable == "pt":
                        axis_limits = (0, 300)
                    # elif variable == "pt_extended":
                    #     axis_limits = (0, 4000)
                    elif variable == "energy":
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
                    elif variable == "n":
                        axis_limits = (0, 50)
                    elif variable == "tuneP_PtErr":
                        axis_limits = (0, 50)
                    elif variable == "dtSeg_n":
                        axis_limits = (0, 50)
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
    #print("Number of entries in tree1.muon_phi:", len(tree1.muon_pt))
    # for event in tree1:
    for variable in variables:
        # variable_value_1 = getattr(tree1, f"muon_{variable}")
        # print("This is first event.muon_pt:",variable_value_1)
        #print("This is step 1")
        total_events += 1  # Increment total_events for each event
        Event_Number.append(total_events)
        #print('total_events', total_events)
        # for variable in variables:
        #     variable_value = getattr(event, f"muon_{variable}")
        for event in tree1:
            correlation_found = False
            variable_value = getattr(event, f"muon_{variable}")
            for (dtSeg_t0timing, dtSeg_globY, dtSeg_found, Chi2, ndof) in zip(
            tree1.muon_dtSeg_t0timing, tree1.muon_dtSeg_globY, tree1.muon_dtSeg_found,
            tree1.muon_Chi2, tree1.muon_comb_ndof
        ):

                #print("This is step 2")
                # print("This is dtSeg_t0timing, dtSeg_globY, dtSeg_found, Chi2, ndof", dtSeg_t0timing, dtSeg_globY, dtSeg_found, Chi2, ndof)

                if dtSeg_t0timing != 0 and dtSeg_found == 1:
                    # print("This is dtSeg_t0timing, dtSeg_found:", dtSeg_t0timing, dtSeg_found)
                    total_events_1 += 1  # Increment total_events_1 for each valid event

                    h_muonGlobalYvsTime1.Fill(dtSeg_t0timing, dtSeg_globY)
                    correlationFactor = h_muonGlobalYvsTime1.GetCorrelationFactor()
                    h_muonGlobalYvsTime1CorrelationFactor.Fill(correlationFactor)

                    #print(variables)
                    #print(variable)
                    #print("Segment was found")
                    segment_counting =+ segment_counting + 1
                    #print(segment_counting)
                    correlation_found = True
            if correlation_found:
                base_histogram_key_no_cuts = f"No_cuts_{variable}_CorrelationFactor"
                histogram_key_positive_no_cuts = f"{base_histogram_key_no_cuts}_Positive"
                histogram_key_negative_no_cuts = f"{base_histogram_key_no_cuts}_Negative"
                # variable_value = getattr(event, f"muon_{variable}")
                if variable == "n":
                    variable_value = [event.muon_n]
                # for value in variable_value:
                value_counting =+ value_counting + 1
                #print("This is value_counting", value_counting)
                # variable_value = getattr(event, f"muon_{variable}")
                for value in variable_value:
                    if correlationFactor > 0:
                        histograms[histogram_key_positive_no_cuts].Fill(value)
                    elif correlationFactor <= 0:
                        histograms[histogram_key_negative_no_cuts].Fill(value)

                for (cut_value, ndof_value) in zip(chi2_vs_ndof_values_1,ndof_values_1):
                    #print("This is cut_value, ndof_value:", cut_value, ndof_value)
                    #print("This is Chi2,ndof:",Chi2,ndof)
                    #print("This is step 4")
                    if ndof != 0 and Chi2 / ndof <= cut_value and ndof >= ndof_value: #and dtSeg_found == 1:
                        # for value in variable_value:
                        # print(cut_value, ndof_value)
                        # print(tree1.muon_Chi2, tree1.muon_comb_ndof)
                            ndof_counting = ndof_counting + 1
                            #print("This is ndof_counting:",ndof_counting)
                            # variable_value = getattr(event, f"muon_{variable}")

                            # if variable == "n":
                            #     variable_value = [event.muon_n]

                            # base_histogram_key = f"{variable}_CorrelationFactor_cut{cut_value}_ndof{ndof_value}"
                            base_histogram_key = f"{variable}_CorrelationFactor_cut{cut_value}_ndof{ndof_value}"
                            histogram_key_positive = f"{base_histogram_key}_Positive"
                            histogram_key_negative = f"{base_histogram_key}_Negative"

                            # for value in variable_value:
                                # print(value)
                            # value_counting_1 =+ value_counting_1 + 1
                            # print("This is value_counting_1:",value_counting_1)

                            if correlationFactor > 0:
                                histograms[histogram_key_positive].Fill(value)
                               # print("This is deep value:",value)
                                histograms[histogram_key_positive].GetXaxis().SetRange(1, histograms[histogram_key_positive].GetNbinsX() + 2)  # Include overflow bin
                            elif correlationFactor <= 0:
                                histograms[histogram_key_negative].Fill(value)
                                histograms[histogram_key_negative].GetXaxis().SetRange(1, histograms[histogram_key_negative].GetNbinsX() + 2)




            #print("This is variable", variable)


    # draw2DHistNoLegend(h_muonGlobalYvsTime1, '2Dhist_SplitMuons_0to75_Background_Total_NoTrigger') #r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', '2Dhisttest') #0.75, 0.4, 0.95, 0.55)
    # draw2DHistNoLegend(h_muonGlobalYvsTime1, '2Dhist_SplitMuons_91to180_Signal_NoTrigger')
            base_histogram_key_no_cuts = f"No_cuts_{variable}_CorrelationFactor"
            histogram_key_positive_no_cuts = f"{base_histogram_key_no_cuts}_Positive"
            histogram_key_negative_no_cuts = f"{base_histogram_key_no_cuts}_Negative"
            # variable_value = getattr(event, f"muon_{variable}")
            if variable == "n":
                variable_value = [event.muon_n]
            # for value in variable_value:
            value_counting =+ value_counting + 1
            #print("This is value_counting", value_counting)
            # variable_value = getattr(event, f"muon_{variable}")
            for value in variable_value:
                if correlationFactor > 0:
                    histograms[histogram_key_positive_no_cuts].Fill(value)
                elif correlationFactor <= 0:
                    histograms[histogram_key_negative_no_cuts].Fill(value)

            for (cut_value, ndof_value) in zip(chi2_vs_ndof_values_1,ndof_values_1):
                    #print(cut_value, ndof_value)
                    #print(tree1.muon_Chi2, tree1.muon_comb_ndof)
                    if ndof != 0 and Chi2 / ndof <= cut_value and ndof >= ndof_value: #and dtSeg_found == 1:
                        ndof_counting = ndof_counting + 1
                        #print("This is ndof_counting:",ndof_counting)
                        # variable_value = getattr(event, f"muon_{variable}")

                        # if variable == "n":
                        #     variable_value = [event.muon_n]

                        # base_histogram_key = f"{variable}_CorrelationFactor_cut{cut_value}_ndof{ndof_value}"
                        base_histogram_key = f"pt_CorrelationFactor_cut{cut_value}_ndof{ndof_value}"
                        histogram_key_positive = f"{base_histogram_key}_Positive"
                        histogram_key_negative = f"{base_histogram_key}_Negative"

                        # for value in variable_value:
                            # print(value)
                        value_counting_1 =+ value_counting_1 + 1
                        #print("This is value_counting_1:",value_counting_1)

                        if correlationFactor > 0:
                            histograms[histogram_key_positive].Fill(value)
                            #print("This is deep value:",value)
                            histograms[histogram_key_positive].GetXaxis().SetRange(1, histograms[histogram_key_positive].GetNbinsX() + 2)  # Include overflow bin
                        elif correlationFactor <= 0:
                            histograms[histogram_key_negative].Fill(value)
                            histograms[histogram_key_negative].GetXaxis().SetRange(1, histograms[histogram_key_negative].GetNbinsX() + 2)







###############Need to fix#################


                # if ndof != 0 and cut_value == 0:
                #     chi2_ndof = Chi2 / ndof
                #     histogram_key_chi2_ndof_positive = f"Positive_Chi2_ndof_cut{cut_value}"
                #     histogram_key_chi2_ndof_negative = f"Negative_Chi2_ndof_cut{cut_value}"

                #     if correlationFactor > 0:
                #         histograms[histogram_key_chi2_ndof_positive].Fill(chi2_ndof)
                #         histograms[histogram_key_chi2_ndof_positive].GetXaxis().SetRange(1, histograms[histogram_key_chi2_ndof_positive].GetNbinsX() + 2)
                #     elif correlationFactor <= 0:
                #         histograms[histogram_key_chi2_ndof_negative].Fill(chi2_ndof)
                #         histograms[histogram_key_chi2_ndof_negative].GetXaxis().SetRange(1, histograms[histogram_key_chi2_ndof_negative].GetNbinsX() + 2)


    # graph_corr_factor_vs_event = r.TGraph()
    # event_number = 0  # Initialize event number

    # # # Your existing code for looping through events
    # for tree in [tree1]:
    #     for event in tree:
    #         total_events += 1
    #         Event_Number.append(total_events)
    #         muon_n.append(event.muon_n)
    #         for (dtSeg_t0timing, dtSeg_globY, dtSeg_found) in zip(event.muon_dtSeg_t0timing, event.muon_dtSeg_globY, event.muon_dtSeg_found):
    #             if dtSeg_t0timing != 0 and dtSeg_found == 1:

    #                 h_muonGlobalYvsTime1.Fill(dtSeg_t0timing, dtSeg_globY)
    #                 correlationFactor = h_muonGlobalYvsTime1.GetCorrelationFactor()
    #                 # Add data points to the TGraph
    #                 graph_corr_factor_vs_event.SetPoint(event_number, event_number, correlationFactor)
    #                 event_number += 1
    # for variable in variables:
    #     for cut_value in chi2_vs_ndof_values:
    #         for ndof_value in ndof_values:
    #             trigger_variable_hist_ndof_cut = r.TH2D(f"Trigger_vs_{variable}_Chi2vsNdof{cut_value}_ndof{ndof_value}", f"Trigger_vs_{variable}_Chi2{cut_value}_ndof{ndof_value}", 2, -0.5, 1.5, 100, -1000, 1000)
  


###############Need to fix#################





    variable_ranges = {
    "phi": (-0.5, 1.5, -4, 4),  # Define the ranges for each variable here
    "n": (-0.5, 1.5, -500, 500),    # Example ranges for variable2
    "eta": (-0.5, 1.5, -2.5, 2.5),  # Example ranges for variable3
    "pt": (-0.5, 1.5, 0, 7000),  # Define the ranges for each variable here
    # "pt_extended":  (-0.5, 1.5, 0, 1000),
    "energy": (-0.5, 1.5, -100, 7000),    # Example ranges for variable2
    "Chi2": (-0.5, 1.5, 0, 100),  # Example ranges for variable3
    "dtSeg_globZ": (-0.5, 1.5, -1000, 1000),  # Define the ranges for each variable here
    "dtSeg_globY": (-0.5, 1.5, -1000, 1000),    # Example ranges for variable2
    "comb_freeInvBeta": (-0.5, 1.5, -50, 50),  # Example ranges for variable3
    "comb_timeAtIpInOut": (-0.5, 1.5, -500, 500),  # Define the ranges for each variable here
    "comb_timeAtIpOutIn": (-0.5, 1.5, -500, 500),    # Example ranges for variable2
    "comb_ndof": (-0.5, 1.5, 0, 50),  # Example ranges for variable3
    "tuneP_PtErr": (-0.5, 1.5, 0, 50),    # Example ranges for variable2
    "dtSeg_n": (-0.5, 1.5, 0, 50),  # Example ranges for variable3
    # Add ranges for other variables as needed
}





    # Initialize histograms outside the loops

    # Loop through variables
    for variable in variables:
        # Get the range for the current variable
        range_values = variable_ranges.get(variable, (-0.5, 1.5, -1000, 1000))
        x_min, x_max, y_min, y_max = range_values

        # Create a plot for Trigger_vs_variable with the specified range
        histogram_name = f"Trigger_vs_{variable}"
        trigger_variable_hist = r.TH2D(histogram_name, f"Trigger vs. {variable}", 2, x_min, x_max, 1000, y_min, y_max)

        for event in tree1:
            # if event.trig_HLT_L1SingleMuCosmics_v2 == 1:
            if event.HLT_L1SingleMuCosmics == 1:
                trigger_value = 1
            else:
                trigger_value = 0

            variable_value = getattr(event, f"muon_{variable}")
            if variable == "n":
                variable_value = [event.muon_n]

            for value in variable_value:
                trigger_variable_hist.Fill(trigger_value, value)

            histograms[histogram_name] = trigger_variable_hist

        # for (cut_value, ndof_value) in zip(chi2_vs_ndof_values_1, ndof_values_1):
        #     histogram_name = f"Trigger_vs_{variable}_Chi2_{cut_value}_ndof_{ndof_value}"
        #     trigger_variable_hist_ndof_cut = r.TH2D(histogram_name, f"Trigger vs. {variable} (Chi2/ndof={cut_value}, ndof={ndof_value})", 2, -0.5, 1.5, 1000, -1000, 1000)


        #     # if event.trig_HLT_L1SingleMuCosmics_v2 == 1:
        #     if event.HLT_L1SingleMuCosmics == 1:
        #         trigger_value = 1
        #     else:
        #         trigger_value = 0

        #     variable_value = getattr(event, f"muon_{variable}")
        #     if variable == "n":
        #         variable_value = [event.muon_n]

        #     for (Chi2, ndof) in zip(event.muon_Chi2, event.muon_comb_ndof):
        #         if ndof != 0 and Chi2/ndof <= cut_value and ndof >= ndof_value:
        #             for value in variable_value:
        #                 trigger_variable_hist_ndof_cut.Fill(trigger_value, value)

            # histograms[histogram_name] = trigger_variable_hist_ndof_cut



    output_file = r.TFile("test2.root", "RECREATE")

    # histogram = r.TH2D("hist", "My 2D Histogram", 100, 0, 1, 100, 0, 1)
    # histTest_2D = draw2DHistToRootFile(h_muonGlobalYvsTime1, "2Dhist_SplitMuons_91to180_Signal_NoTrigger", output_file)

    # histograms[histogram_name] = histTest_2Dc

    # merged_2D_hist = combine2DHistograms(list(histograms.values()))
    # merged_2D_hist.Write("Merged2D")

    # Save the histograms to a ROOT file
    # output_file = r.TFile("test2.root", "RECREATE")
    for histogram in histograms.values():
        histogram.Write()



    graph_corr_factor_vs_event.Write("graph_corr_factor_vs_event")
    output_file.Close()

    # draw2DHistNoLegend(h_muonGlobalYvsTime1, 'test2') #r'$0^\circ$ - $75^\circ$', r'$91^\circ$ - $180^\circ$', '2Dhisttest') #0.75, 0.4, 0.95, 0.55))

if __name__ == "__main__":
     main()
