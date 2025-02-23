import bpy
import csv
import mathutils
from math import radians

# Any prefixes in the exclude list will automatically be checked against every object loaded in. If they match, that object is skipped. (Useful for removing clutter from engine markers like NPC idles)
EXCLUDE = ["marker", "fx"]
# Normalize_loc will find the average of all objects and automatically move the scene so it is centered in blender
NORMALIZE_LOC = True
# Rescales the scene to real world units after importing. Conversion factors were taken from UESP https://ck.uesp.net/w/index.php?title=Unit
RESCALE = True
CONVERSION_SCALE = 0.01428750 if RESCALE else 1.0
# Path to xedit script output
xedit_output = 'C:\\xEdit\\output.txt'

# Path to extracted meshes
# The directory should also contain extracted textures.
# D:\ExtractedData\
#          |-\meshes\
#          |-\textures\

mesh_loc="D:\\ExtractedData\\meshes\\"

def import_nif(object, mesh_folder, average_offset):
    if (object == [] or object[0]==""):
        return False
    
    for exclusion in EXCLUDE:
        if exclusion in object[0].lower():
            return False
        
    file_loc = mesh_folder+object[0]
    try:
        before_import = set(bpy.context.scene.objects.keys())
        bpy.ops.import_scene.pynifly(filepath=file_loc)
        after_import = set(bpy.context.scene.objects.keys())
        import_objects = [bpy.data.objects[x] for x in list(after_import - before_import)]
        for i in import_objects:
            if i.parent == None:
                scale = CONVERSION_SCALE
                if object[7] != '':
                    scale *= float(object[7])
                    
                i.location= (float(object[1])*CONVERSION_SCALE-average_offset[0], float(object[2])*CONVERSION_SCALE-average_offset[1], float(object[3])*CONVERSION_SCALE-average_offset[2])
                i.scale = (scale, scale, scale)
                eul = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
                eul.rotate_axis("X", radians(360-float(object[4])))
                eul.rotate_axis("Y", radians(360-float(object[5])))
                eul.rotate_axis("Z", radians(360-float(object[6])))
                i.rotation_euler = eul
                
        
    except Exception as e:
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(e)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        pass
    
    return False

cell = []
with open(xedit_output, newline='') as csvfile:
    cellreader = csv.reader(csvfile, delimiter=',')
    for row in cellreader:
        cell.append(row)

if NORMALIZE_LOC:
    ax=0
    ay=0
    az=0
    count=0
    for object in cell:
        if object != []:
            ax+=float(object[1])
            ay+=float(object[2])
            az+=float(object[3])
            count+=1
            
    offset = (int(ax/count)*CONVERSION_SCALE, int(ay/count)*CONVERSION_SCALE, int(az/count)*CONVERSION_SCALE)

else:
    offset = (0, 0, 0)

total = 0
for object in cell:
    import_nif(object, mesh_loc, offset)
    print(f"Import Progress: {100*total/len(cell)}%")
    total+=1
    bpy.ops.object.select_all(action='DESELECT')