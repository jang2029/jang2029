import maya.cmds as cmds
import json








shadingGroups = cmds.ls( selection=True )
print (shadingGroups)
for s in shadingGroups:
    cmds.hyperShade (s, objects = "")




shadingGroups = cmds.ls( selection=True )
print (shadingGroups)
cmds.hyperShade (s, smn =True)


















cmds.listConnections( 'beige_vp',type = 'shadingEngine')


SG = cmds.listConnections( 'beige_vp',type = 'shadingEngine')
select SG

select -r Rt_Shoulderpad_GeoShape zipper_GeoShape Top_Legs_Geo.f[0:1961] Top_Legs_Geo.f[3338:5777] Lf_UpperArm_GeoShape Lf_Forearm_Geo.f[0:2264] Bot_Legs_Geo.f[2496:3639] Bot_Legs_Geo.f[5846:6513] Bot_Legs_Geo.f[9466:10037] Rt_UpperArm_GeoShape Rt_Forearm_Geo.f[0:1516] Rt_Forearm_Geo.f[2129:2876] Rt_shoulder_circle_Geo.f[1584:2223] Lf_shoulderpad_GeoShape Lf_shoulder_circle_Geo.f[1564:2203] eyes_Geo_oldShape chest_GeoShape chestdetail3_GeoShape chestrim_GeoShape;
