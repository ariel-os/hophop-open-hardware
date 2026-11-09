"""Generate simplified mechanical models; dimensions in mm, PCB top at Z=0.

J202: JMECONN 5001-MX0125A-xxR1-00 manufacturer drawing (local datasheets).
D301: Lumex SML-LX0303SIUPGUSB revision A manufacturer drawing:
https://www.mouser.com/datasheet/2/244/SML-LX0303SIUPGUSB-1509215.pdf
These are nominal body/contact models, not vendor manufacturing CAD.
"""
from pathlib import Path
from OCP.gp import gp_Pnt
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.TDataStd import TDataStd_Name
ROOT=Path(__file__).resolve().parent

def box(x,y,z,dx,dy,dz):
    return BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),dx,dy,dz).Shape()

def export(path, parts):
    doc=TDocStd_Document(TCollection_ExtendedString('BinXCAF'))
    shapes=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    colors=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    for name,shape,rgb in parts:
        label=shapes.AddShape(shape,False)
        TDataStd_Name.Set_s(label,TCollection_ExtendedString(name))
        colors.SetColor(label,Quantity_Color(*rgb,Quantity_TOC_RGB),XCAFDoc_ColorType.XCAFDoc_ColorGen)
    writer=STEPCAFControl_Writer();writer.Transfer(doc,STEPControl_AsIs)
    writer.Write(str(ROOT/path))

# Y is inverted relative to footprint coordinates. Mating mouth faces -Y.
case=box(-3.25,-2.75,.1,6.5,5.5,1.85)
case=BRepAlgoAPI_Cut(case,box(-2.5,-2.76,.3,5,3.51,1.35)).Shape()
parts=[('JMECONN nominal housing, simplified',case,(.9,.88,.79))]
for x in [-.625,.625]:
    parts.append(('signal terminal',box(x-.2,2.1,0,.4,2,.15),(.75,.75,.72)))
    parts.append(('mating contact',box(x-.2,-1.8,.35,.4,3.9,.15),(.8,.72,.4)))
for x in [-3.575,3.575]:
    parts.append(('retention tab',box(x-.175,-2.75,0,.35,2.65,.15),(.75,.75,.72)))
export('HopHop_Connector.3dshapes/JMECONN_5001-MX0125A-02R1-00.step',parts)

parts=[('Lumex nominal 0.8 x 0.8 x 0.65 package',box(-.4,-.4,.08,.8,.8,.27),(.86,.85,.79)),
       ('clear lens, simplified',box(-.4,-.4,.35,.8,.8,.3),(.77,.83,.79))]
for x in [-.25,.25]:
    for y in [-.25,.25]:parts.append(('contact',box(x-.15,y-.15,0,.3,.3,.08),(.8,.73,.43)))
export('HopHop_LED_SMD.3dshapes/LED_Lumex_SML-LX0303SIUPGUSB.step',parts)
