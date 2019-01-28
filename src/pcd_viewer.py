# -*- coding: utf-8 -*-
'''
Created on 2019-01-25
@summary: pcd_viewer
@author: fiefdx
'''

import os
import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomNode, NodePath

from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexArrayData, GeomVertexArrayFormat
from panda3d.core import Geom, GeomPoints, InternalName, GeomEnums
from panda3d.core import loadPrcFileData

import pypcd
import numpy

from pcd_viewer import arrayfilter


loadPrcFileData('', 'win-size 1280 720')


def load_pcd_content(content, w = 2, color_mode = "intensity", intensity_filter = 50):
    pc = pypcd.PointCloud.from_buffer(content)
    fmt = GeomVertexFormat() #3 component vertex, w/ 4 comp color
    fmt_arr = GeomVertexArrayFormat()
    fmt_arr.addColumn(InternalName.make('vertex'), 3, Geom.NTFloat32, Geom.CPoint)
    fmt_color_arr = GeomVertexArrayFormat()
    fmt_color_arr.addColumn(InternalName.make('color'), 4, Geom.NTUint8, Geom.CColor)
    fmt.addArray(fmt_arr)
    fmt.addArray(fmt_color_arr)
    fmt = GeomVertexFormat.registerFormat(fmt)

    vertexData = GeomVertexData('points', fmt, Geom.UHStatic)
    pointCloud = GeomPoints(Geom.UHStatic)

    pc.pc_data.dtype = numpy.dtype("<f4")
    v, c = arrayfilter.vertices_filter(pc.pc_data.reshape((pc.points, 4)))
    for i in xrange(len(v)):
        pointCloud.addVertex(i)
        pointCloud.closePrimitive()

    arr = GeomVertexArrayData(fmt.getArray(0), GeomEnums.UHStream)
    datahandle = arr.modifyHandle()
    datahandle.copyDataFrom(v)
    vertexData.setArray(0, arr)

    arr = GeomVertexArrayData(fmt.getArray(1), GeomEnums.UHStream)
    datahandle = arr.modifyHandle()
    datahandle.copyDataFrom(c)
    vertexData.setArray(1, arr)

    cloud = Geom(vertexData)
    cloud.addPrimitive(pointCloud)
    cloudNode = GeomNode('points')
    cloudNode.addGeom(cloud)
    cloudNodePath = NodePath(cloudNode)
    cloudNodePath.setRenderModeThickness(w)
    cloudNodePath.setRenderModePerspective(True)
    return cloudNode


class ViewerApp(ShowBase):
    def __init__(self, pcd_path = ""):
        ShowBase.__init__(self)

        self.setBackgroundColor(0, 0, 0)
        if pcd_path is not "":
            pcd = open(pcd_path, "rb").read()
            p = load_pcd_content(pcd, w = 0.03, color_mode = "intensity", intensity_filter = 0)
            np = NodePath(p)
            np.reparentTo(self.render)


def main():
    try:
        argv_n = len(sys.argv)
        LOG.debug("argv_n: %s", argv_n)
        if argv_n < 1:
            print "missing parameter! So, exit the program now."
            sys.exit()
        pcd_path = ""
        if argv_n == 2:
            pcd_path = sys.argv[1]
        app = ViewerApp(pcd_path)
        app.run()
    except Exception, e:
        LOG.exception(e)


if __name__ == "__main__":
    main()
