#!/usr/bin/env python
import ROOT
import argparse
import os
import glob
import errno
import itertools
from Utilities import OutputTools, IVCurve
from IPython import embed

config_info = {}
def getComLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", required=True,
            type=lambda x : itertools.chain(
                *[glob.glob(i.strip()) for i in x.split(",")]
            ),
            help="List of files of data files to plot, separated "
            "commas. Unix wildcards will be expanded"
    )
    parser.add_argument("--discard_fits", action='store_true',
            help="Don't store plots for fits to exponential "
                "fits (for pA points)"
    )
    parser.add_argument("--logy", action='store_true',
            help="Use log scale for y-axis"
    )
    parser.add_argument("--legend_right", action='store_true',
            help="Position legend to the right"
    )
    parser.add_argument("-o", "--output_folder", type=str,
            default="/afs/cern.ch/user/k/kelong/www/GIFstuff",
            help="Name of folder to store plots"
    )
    parser.add_argument("--scaley", type=float, default=1.2,
            help="Set y-axis max to y_max*args.scaley"
    )
    parser.add_argument("--xmax", type=float, default=-1,
            help="Set x_max to args.xmax if specfied, otherwise"
                 " xmax is taken from the xrange of the graphs"
    )
    parser.add_argument("--ymin", type=float, default=0.1,
            help="Minimum value for y-axis range. Default 0.1"
    )
    parser.add_argument("--scaleleg", type=float,
            default=1.,
            help="Scale legend entries (nominal size 0.06)"
    )
    return parser.parse_args()
def getPrettyLegend(graphs, entry_size, right):
    offset = ROOT.gPad.GetRightMargin() - 0.04
    xcoords = [.15, .5] if not right else [.55-offset, .90-offset]
    unique_entries = len(graphs)
    ycoords = [.9, .9 - entry_size*unique_entries]
    legend = ROOT.TLegend(xcoords[0], ycoords[0], xcoords[1], ycoords[1])
    legend.SetFillColor(0)
    for graph in graphs:
        legend.AddEntry(graph, graph.GetTitle(), "PE")
    return legend
def main():
    ROOT.gROOT.SetBatch(True)
    final_canvas = ROOT.TCanvas("final", "final")
    ROOT.gStyle.SetOptStat(1)
    args = getComLineArgs()
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kGreen, ROOT.kGray, ROOT.kCyan,
                ROOT.kYellow, ROOT.kGreen + 4, ROOT.kOrange, ROOT.kPink]
    OutputTools.makeDirectory(args.output_folder)
    curves = []
    graphs = []
    for i, data_file in enumerate(args.files):
        curve = IVCurve.IVCurve(data_file)
        curves.append(curve)
        graphs.append(curve.getCurve(args.output_folder))
    ymax = max([x.GetMaximum() for x in graphs])
    xmax = args.xmax if args.xmax > 0 else max([x.GetXaxis().GetXmax() for x in graphs])
    for i, (graph, curve) in enumerate(zip(graphs, curves)):
        if i == 0:
            graph.GetXaxis().SetLimits(0, xmax)
            graph.SetMaximum(ymax*args.scaley)
            graph.SetMinimum(args.ymin)
            graph.Draw("AP")
        else:
            graph.Draw("Psames")
        graph.SetMarkerColor(colors[i])
        stat_box = curve.getStatBox()
        if stat_box:
            stat_box.SetX1NDC(0.7)
            stat_box.SetX2NDC(0.9)
            stat_box.SetY1NDC(0.4)
            stat_box.SetY2NDC(0.5)
            final_canvas.Update()
        fit_text = curve.getFitText()
        if fit_text:
            fit_text.Draw()
    if args.logy:
        final_canvas.SetLogy()
    legend = getPrettyLegend(graphs, 0.06*args.scaleleg, args.legend_right)
    #embed()
    legend.Draw()
    final_canvas.Print("/".join([args.output_folder, "final.pdf"]))

if __name__ == "__main__":
        main()
