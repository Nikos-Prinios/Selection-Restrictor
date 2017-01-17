# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
	"name": "Selection-Restrictor",
	"author": "Alesis & Nikos",
	"version": (0,0,1,0),
	"blender": (2, 7, 8, 0),
	"api": 44539,
	"category": "3D View",
	"location": "View3D > Header",
	"description": "This addon helps to restrict the selection of objects by type.",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",}
''' version 1.5 '''

import bpy
from bpy.types import Header
from bpy.app.handlers import persistent
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty, StringProperty
from bpy.app.handlers import persistent
global sel_restrictor
global obj_num

obj_num = 1


@persistent
def need_update(dummy):
    global obj_num
    objects = bpy.data.objects
    if objects.is_updated:
        if len(objects) != obj_num:
            obj_num = len(objects)
            update()


def prop_update(self,context):
    update()

def is_emissive(obj):
    for mat in obj.data.materials:
        for n in mat.node_tree.nodes:
            if n.type == "EMISSION":
                return True

def update():
    global sel_restrictor
    emissive_as_light = bpy.context.user_preferences.addons[__name__].preferences.emissive_as_light
    hidden_selectable = bpy.context.user_preferences.addons[__name__].preferences.hidden_selectable
    start_with = bpy.context.user_preferences.addons[__name__].preferences.start_with
    mesh_button = bpy.context.user_preferences.addons[__name__].preferences.mesh_button
    camera_button = bpy.context.user_preferences.addons[__name__].preferences.camera_button
    light_button = bpy.context.user_preferences.addons[__name__].preferences.light_button
    empty_button = bpy.context.user_preferences.addons[__name__].preferences.empty_button
    curve_button = bpy.context.user_preferences.addons[__name__].preferences.curve_button
    armature_button = bpy.context.user_preferences.addons[__name__].preferences.armature_button
    surface_button = bpy.context.user_preferences.addons[__name__].preferences.surface_button
    text_button = bpy.context.user_preferences.addons[__name__].preferences.text_button
    lattice_button = bpy.context.user_preferences.addons[__name__].preferences.lattice_button
    field_button = bpy.context.user_preferences.addons[__name__].preferences.field_button
    metaball_button = bpy.context.user_preferences.addons[__name__].preferences.metaball_button

    context = bpy.context
    if sel_restrictor:
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                if emissive_as_light and is_emissive(obj) and obj.name.startswith(start_with):
                    obj.hide_select = not context.scene.lights  
                    print(obj.name)  
                else:
                    obj.hide_select = not context.scene.meshes
            if obj.type == 'CAMERA':
                obj.hide_select = not context.scene.cameras
            if obj.type == 'LAMP':
                obj.hide_select = not context.scene.lights
            if obj.type == 'EMPTY':
                obj.hide_select = not context.scene.empties
            if obj.type == 'CURVE':
                obj.hide_select = not context.scene.nurbs
            if obj.type == 'ARMATURE' :
                obj.hide_select = not context.scene.bones
            if obj.type == 'SURFACE' :
                obj.hide_select = not context.scene.surfaces
            if obj.type == 'FONT' :
                obj.hide_select = not context.scene.texts
            if obj.type == 'LATTICE' :
                obj.hide_select = not context.scene.lattices
            if obj.field.type != 'NONE' :
                obj.hide_select = not context.scene.fields
            if obj.type == 'META' :
                obj.hide_select = not context.scene.metaballs

        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and not mesh_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'CAMERA' and not camera_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'LAMP' and not light_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'EMPTY' and not empty_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'CURVE' and not curve_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'ARMATURE' and not armature_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'SURFACE' and not surface_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'FONT' and not text_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'LATTICE' and not lattice_button:
                obj.hide_select = hidden_selectable
            if obj.field.type != 'NONE' and not field_button:
                obj.hide_select = hidden_selectable
            if obj.type == 'META' and not metaball_button:
                obj.hide_select = hidden_selectable

        for obj in bpy.context.scene.objects:        
                if obj.select and obj.hide_select :
                    obj.select = False
                
S = bpy.types.Scene        
S.meshes = bpy.props.BoolProperty(name="Meshes", default = False, update = prop_update)
S.nurbs = bpy.props.BoolProperty(name="Nurbs", default = False, update = prop_update)
S.cameras = bpy.props.BoolProperty(name="Cameras", default = False, update = prop_update)
S.lights = bpy.props.BoolProperty(name="Lights", default = False, update = prop_update)
S.empties = bpy.props.BoolProperty(name="Empties", default = False,update = prop_update)
S.bones = bpy.props.BoolProperty(name="Bones", default = False, update = prop_update)
S.surfaces = bpy.props.BoolProperty(name="surfaces", default = False, update = prop_update)
S.texts = bpy.props.BoolProperty(name="texts", default = False, update = prop_update)
S.lattices = bpy.props.BoolProperty(name="lattices", default = False, update = prop_update)
S.fields = bpy.props.BoolProperty(name="fields", default = False, update = prop_update)
S.metaballs = bpy.props.BoolProperty(name="metaballs", default = False, update = prop_update)

bpy.types.Object.init = bpy.props.BoolProperty(name="init",description="Initial state",default = False)

sel_restrictor = False

def initial_read():
    for obj in bpy.context.scene.objects:
        obj.init = obj.hide_select

def initial_write():
    for obj in bpy.context.scene.objects:
        obj.hide_select = obj.init

class selective_panel(Header):
    bl_space_type = 'VIEW_3D'
    bl_label = "Selective"
    bl_idname = "OBJECT_PT_Selective"
    bl_region_type = 'HEADER'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        global sel_restrictor, empties,lights,bones,cameras,meshes,nurbs

        mesh_button = bpy.context.user_preferences.addons[__name__].preferences.mesh_button
        light_button = bpy.context.user_preferences.addons[__name__].preferences.light_button
        camera_button = bpy.context.user_preferences.addons[__name__].preferences.camera_button
        empty_button = bpy.context.user_preferences.addons[__name__].preferences.empty_button
        curve_button = bpy.context.user_preferences.addons[__name__].preferences.curve_button
        armature_button = bpy.context.user_preferences.addons[__name__].preferences.armature_button
        surface_button = bpy.context.user_preferences.addons[__name__].preferences.surface_button
        text_button = bpy.context.user_preferences.addons[__name__].preferences.text_button
        lattice_button = bpy.context.user_preferences.addons[__name__].preferences.lattice_button
        field_button = bpy.context.user_preferences.addons[__name__].preferences.field_button
        metaball_button = bpy.context.user_preferences.addons[__name__].preferences.metaball_button

        if not sel_restrictor :
            row = layout.row()
            row.separator()
            row.operator("objects.activate", icon='UNPINNED', text='Selectivity')
            row.active = False
        else :
            row = layout.row(align=True)
            row.separator()
            row.operator("objects.activate", icon='PINNED', text='') 
             
            row = layout.row(align=True)
            row.active = True
            if mesh_button : row.prop(bpy.context.scene,"meshes", "", icon='MESH_DATA')
            if light_button : row.prop(bpy.context.scene,"lights", "", icon='LAMP')
            if camera_button : row.prop(bpy.context.scene,"cameras", "", icon='OUTLINER_DATA_CAMERA')
            if empty_button : row.prop(bpy.context.scene,"empties", "", icon='OUTLINER_OB_EMPTY')
            if curve_button : row.prop(bpy.context.scene,"nurbs", "", icon='CURVE_DATA')
            if armature_button : row.prop(bpy.context.scene,"bones", "", icon='BONE_DATA')
            if surface_button : row.prop(bpy.context.scene, "surfaces", "", icon="SURFACE_DATA")
            if text_button : row.prop(bpy.context.scene, "texts", "",icon="FONT_DATA")
            if lattice_button : row.prop(bpy.context.scene, "lattices", "", icon="OUTLINER_OB_LATTICE")
            if field_button : row.prop(bpy.context.scene, "fields", "",icon="FORCE_FORCE")
            if metaball_button : row.prop(bpy.context.scene, "metaballs", "",icon="META_BALL")

# Preferences

class OBJECT_OT_activate(bpy.types.Operator):
    bl_idname = "objects.activate"
    bl_label = "Activate Selective"
 
    def execute(self, context):
        global sel_restrictor
        
        sel_restrictor = not sel_restrictor
        if sel_restrictor:
            initial_read()
            prop_update(self, bpy.context)
        else:
            initial_write()
        return{'RUNNING_MODAL'}

class SelectivityPreferences(AddonPreferences):
    bl_idname = __name__

    mesh_button = BoolProperty(
            name="mesh button",
            default=True, 
            )
    light_button = BoolProperty(
            name="light button",
            default=True,
            )
    camera_button = BoolProperty(
            name="camera button",
            default=True,
            )
    empty_button = BoolProperty(
            name="empty button",
            default=True,
            )
    curve_button = BoolProperty(
            name="curve button",
            default=True,
            )
    armature_button = BoolProperty(
            name="armature button",
            default=True,
            )
    surface_button = BoolProperty(
            name="surface button",
            default=True,
            )
    text_button = BoolProperty(
            name="text button",
            default=False,
            )
    lattice_button = BoolProperty(
            name="lattice button",
            default=False,
            )
    field_button = BoolProperty(
            name="field button",
            default=False,
            )
    metaball_button = BoolProperty(
            name="metaball button",
            default=False,
            )

    emissive_as_light = BoolProperty(
            name="other light",
            default=False,
            )
    start_with = StringProperty(
            name="begins with:",
            )
    hidden_selectable = BoolProperty(
            name="hidden selectable",
            default=False,
            )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Display only:")
        row = layout.row(align=True)
        row.prop(self, "mesh_button", icon='MESH_DATA', text='')
        row.prop(self, "light_button", icon='LAMP', text='')
        row.prop(self, "camera_button", icon="OUTLINER_DATA_CAMERA", text='')
        row.prop(self, "empty_button", icon="OUTLINER_OB_EMPTY", text='')
        row.prop(self, "curve_button", icon="CURVE_DATA", text='')
        row.prop(self, "armature_button", icon="BONE_DATA", text='')
        row.prop(self, "surface_button", icon="SURFACE_DATA", text='')
        row.prop(self, "text_button", icon="FONT_DATA", text='')
        row.prop(self, "lattice_button", icon="OUTLINER_OB_LATTICE", text='')
        row.prop(self, "field_button", icon="FORCE_FORCE", text='')
        row.prop(self, "metaball_button", icon="META_BALL", text='')
        row.separator()
        row.separator()
        row.prop(self, "hidden_selectable", icon='FILTER', text='')
        if self.hidden_selectable:
            row.label("Not displayed types are not selectable")
        else:
            row.label("Not displayed types are selectable")
        
        row = layout.row(align=True)
        row.prop(self, "emissive_as_light", icon='LAMP_AREA', text='Emissive objects count as light')
        row.prop(self, "start_with", text='if start with:')
        row = layout.row(align=True)
        

class OBJECT_OT_addon_prefs(Operator):
    bl_idname = "object.selectivity_prefs"
    bl_label = "Selection Restrictor Preferences"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        info = ("Mesh: %r, Light: %r, Camera: %r, Empty: %r, Curve: %r, Armature: %r, Surface: %r, Text: %r, Lattice: %r, Field: %r, Metaball: %r, " %
                (addon_prefs.mesh_button, addon_prefs.light_button, addon_prefs.camera_button, addon_prefs.empty_button, addon_prefs.curve_button, addon_prefs.armature_button, addon_prefs.surface_button, addon_prefs.text_button, addon_prefs.lattice_button, addon_prefs.field_button, addon_prefs.metaball_button))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}
  
def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.scene_update_post.clear()
    bpy.app.handlers.scene_update_post.append(need_update)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.scene_update_post.remove(need_update)

if __name__ == "__main__":
    register()
