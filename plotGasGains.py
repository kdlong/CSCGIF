#!/usr/bin/env python
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import errno
from Utilities import OutputTools, InputTools
from DataTools import IVCurve, IVData
from IPython import embed
import os
import sys
import datetime

config_info = {}
def getComLineArgs():
    parser = InputTools.getDefaultParser()
    parser.add_argument("--discard_fits", action='store_true',
            help="Don't store plots for fits to exponential "
                "fits (for pA points)"
    )
    parser.add_argument("--logy", action='store_true',
            help="Use log scale for y-axis"
    )
    parser.add_argument("--show_stats", action='store_true',
            help="Print stat box"
    )
    parser.add_argument("--saveroot", action='store_true',
            help="Save canvas to root file"
    )
    parser.add_argument("--legend_right", action='store_true',
            help="Position legend to the right"
    )
    parser.add_argument("-o", "--output_folder", type=str,
            default="/afs/cern.ch/user/k/kelong/www/GIFstuff",
            help="Name of folder to store plots"
    )
    parser.add_argument("-e", "--extra_text", type=str,
            default="",
            help="Extra text to be added to plot"
    )
    parser.add_argument("-t", "--extra_text_left", type=str,
            default="",
            help="Extra text to be added to plot in top left corner"
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
    parser.add_argument("-n", "--norm_factor", type=float, default=1,
            help="Multiplicative factor applied to all data. Default 1"
    )
    parser.add_argument("--scaleleg", type=float,
            default=1.,
            help="Scale legend entries (nominal size 0.06)"
    )
    return parser.parse_args()
def addExtraText(text, size, left=False):
    lines = [x.strip() for x in text.split(";")]
    xvals = [0.6, 0.9] if not left else [.175, .575]
    box_size = size*len(lines)
#    if args.extra_text_above:
#        ymax = coords[1] 
#        coords[1] -= box_size
#        coords[3] -= box_size
    ymax = 0.4 if not left else 0.9
    ymin = ymax - box_size
#    text_box = ROOT.TPaveText(coords[0], ymin, coords[2], ymax, "NDCnb")
    text_box = ROOT.TPaveText(xvals[0], ymin, xvals[1], ymax, "NDCnb")
    text_box.SetFillColor(0)
    text_box.SetTextFont(42)
    for i, line in enumerate(lines):
        text_box.AddText(line)
    text_box.Draw()
    ROOT.SetOwnership(text_box, False)
def getPrettyLegend(graphs, entry_size, right):
    offset = ROOT.gPad.GetRightMargin() - 0.04
    xcoords = [.15, .5] if not right else [.55-offset, .90-offset]
    unique_entries = len(graphs)
    ycoords = [.85, .85 - entry_size*unique_entries]
    legend = ROOT.TLegend(xcoords[0], ycoords[0], xcoords[1], ycoords[1])
    legend.SetFillColor(0)
    for graph in graphs:
        legend.AddEntry(graph, graph.GetTitle(), "PE")
    return legend
def main():
    ROOT.gROOT.SetBatch(True)
    final_canvas = ROOT.TCanvas("final", "final")
    args = getComLineArgs()
    if not args.show_stats:
        ROOT.gStyle.SetOptFit(0000)
    output_folder = os.path.expanduser(args.output_folder)
    OutputTools.makeDirectory(output_folder)
    curves = []
    graphs = []
    with open("/".join([output_folder, "meta_info.log"]), "w") as log:
        log.write('-'*80 + '\n' + 
            'Script completed at %s\n' % datetime.datetime.now() +
            'The command was: %s\n' % ' '.join(sys.argv) +
            '-'*80 + '\n'
        )
        log.write("\n{0:<15} {1:<15} {2:<15}".format("Voltage (V)", "Current (nA)", "Unc (nA"))
    
        for data_file in InputTools.getFileList(args.files, args.data_path):
            data = IVData.IVData(data_file)
            curve = IVCurve.IVCurve(data, args.norm_factor)
            curves.append(curve)
            graphs.append(curve.getCurve(output_folder))
            for point in data.getRawData(""):
                log.write("\n{0:<15.1f} {1:<15.3f} {2:<15.3f}".format(*point))
    if args.subtract_files != []:
        subtract_files = InputTools.getFileList(args.subtract_files, args.data_path)
        filedata = IVData.IVData(next(subtract_files))
        filedata.loadRawData()
        subtract_data = IVData.IVData(next(subtract_files))
        subtract_data.loadRawData()
        filedata.subtractData(subtract_data)
        curve = IVCurve.IVCurve(filedata)
        curves.append(curve)
        graph = curve.getCurve(output_folder)
        graph.SetLineColor(ROOT.kGray)
        graph.SetMarkerColor(ROOT.kGray)
        graph.SetLineColor(ROOT.kGray+2)
        graph.SetMarkerColor(ROOT.kGray+2)
        graphs.append(graph)
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
        stat_box = curve.getStatBox()
        #if stat_box:
        #    stat_box.SetX1NDC(0.7)
        #    stat_box.SetX2NDC(0.9)
        #    stat_box.SetY1NDC(0.4)
        #    stat_box.SetY2NDC(0.5)
        #    final_canvas.Update()
        fit_text = curve.getFitText()
        if fit_text:
            fit_text.Draw()
    if args.logy:
        final_canvas.SetLogy()
    if args.extra_text != "":
        addExtraText(args.extra_text, 0.03)
    if args.extra_text_left != "":
        addExtraText(args.extra_text_left, 0.04, True)
    ROOT.gROOT.ForceStyle()
    final_canvas.Update()
    legend = getPrettyLegend(graphs, 0.06*args.scaleleg, args.legend_right)
    legend.Draw()
    final_canvas.Print("/".join([output_folder, "final.pdf"]))
    if args.saveroot:
        final_canvas.Print("/".join([output_folder, "final.root"]))

if __name__ == "__main__":
        main()
