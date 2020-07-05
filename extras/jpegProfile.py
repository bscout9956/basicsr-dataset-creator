from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import jpegPrepare

with PyCallGraph(output=GraphvizOutput()):
    jpegPrepare.main()