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
	"author": "Alesis, Luciano & Nikos",
	"version": (1,5),
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
global obj_num, selected_objects, is_ctrl, panic

is_ctrl = False
obj_num = 1
restrict_to_selection = False
invert_call = False
panic = False


@persistent
def need_update(dummy):
    global obj_num
    scene = bpy.context.scene
    objects = bpy.data.objects
    if objects.is_updated:
        if len(objects) != obj_num:
            obj_num = len(objects)
            update()


def is_ctrl_pressed():
    global is_ctrl
    bpy.ops.object.ctrl_operator('INVOKE_DEFAULT')
    if is_ctrl :
        is_ctrl = False
        return True
    else:
        is_ctrl = False
        return False


def prop_update(self,context):
    update()


def swap(prop):
    global panic
    panic = True
    s = bpy.context.scene
    v = not getattr(s, prop)
    attributes = 'meshes lights cameras nurbs lattices empties texts bones surfaces metaballs fields'.split(' ')
    for attribute in attributes:
        setattr(s, attribute, not v if prop == attribute else v)
    panic = False
    update()


def create_update_func(prop):
    def self_update(self, context):
        global panic
        if panic != True:
            if is_ctrl_pressed():
                swap(prop)
            else:
                update()
    return self_update


def is_emissive(obj):
    try:
        for mat in obj.data.materials:
            for n in mat.node_tree.nodes:
                if n.type == "EMISSION":
                    return True
    except:
        return False


def initial_selection_read():
    global selected_objects
    selected_objects = []
    for obj in bpy.context.scene.objects:
        if obj.select:
            selected_objects.append(obj)


def initial_selection_write():
    global selected_objects
    for obj in bpy.context.scene.objects:
        if obj in selected_objects:
            print(obj.name)
            obj.hide_select = False
        else:
            obj.hide_select = True


def update():
    global sel_restrictor
    context = bpy.context
    scene = context.scene
    p = bpy.context.user_preferences.addons[__name__].preferences
    emissive_as_light = bpy.context.user_preferences.addons[__name__].preferences.emissive_as_light
    hidden_selectable = bpy.context.user_preferences.addons[__name__].preferences.hidden_selectable
    start_with = bpy.context.user_preferences.addons[__name__].preferences.start_with
    types = 'LAMP CAMERA CURVE LATTICE EMPTY FONT ARMATURE SURFACE META'.split(' ')
    props = 'lights cameras nurbs lattices empties texts bones surfaces metaballs'.split(' ')

    if sel_restrictor:
        
        # PANEL
        for obj in scene.objects: 
            # MESHES
            if obj.type == 'MESH':
                if emissive_as_light and is_emissive(obj) and obj.name.startswith(start_with):
                    obj.hide_select = not scene.lights  
                else:
                    obj.hide_select = not scene.meshes
            # FIELDS
            elif obj.field.type != 'NONE':
                    obj.hide_select = not scene.fields
            # OTHERS
            else:
                for i, typo in enumerate(types):
                    if obj.type == typo:
                        obj.hide_select = not getattr(scene, props[i])
        
        # PREFERENCES --> HIDDEN        
        types = 'MESH LAMP CAMERA CURVE LATTICE EMPTY FONT ARMATURE SURFACE META'.split(' ')
        buttons = 'mesh_button light_button camera_button curve_button lattice_button empty_button text_button armature_button surface_button metaball_button'.split(' ')

        for obj in scene.objects:
            for i, typo in enumerate(types): 
                if obj.type == typo and not getattr (p,buttons[i]):
                    obj.hide_select = hidden_selectable
                if obj.field.type != 'NONE' and not p.field_button:
                    obj.hide_select = hidden_selectable
        
        # SELECTION ONLY
        if scene.restrict_to_selected_objects:
            initial_selection_read()
            for obj in scene.objects:
                if not obj.select:
                    obj.hide_select = True
                else:
                    obj.hide_select = False

        # DESELECT THE UNSELECTABLES
        for obj in scene.objects:        
                if obj.select and obj.hide_select :
                    obj.select = False
 
def restrict_to_selection(self,context):
    if context.scene.restrict_to_selected_objects:
        initial_selection_read()
        for obj in context.scene.objects:
            if not obj.select:
                obj.hide_select = True
            else:
                obj.hide_select = False
    else:
        update()

S = bpy.types.Scene        
S.meshes = bpy.props.BoolProperty(name="Meshes", default = True, update =create_update_func("meshes"))
S.nurbs = bpy.props.BoolProperty(name="Nurbs", default = True, update =create_update_func("nurbs"))
S.cameras = bpy.props.BoolProperty(name="Cameras", default = True, update =create_update_func("cameras"))
S.lights = bpy.props.BoolProperty(name="Lights", default = True, update =create_update_func("lights"))
S.empties = bpy.props.BoolProperty(name="Empties", default = True,update =create_update_func("empties"))
S.bones = bpy.props.BoolProperty(name="Bones", default = True, update =create_update_func("bones"))
S.surfaces = bpy.props.BoolProperty(name="surfaces", default = True, update =create_update_func("surfaces"))
S.texts = bpy.props.BoolProperty(name="texts", default = True, update =create_update_func("texts"))
S.lattices = bpy.props.BoolProperty(name="lattices", default = True, update =create_update_func("lattices"))
S.fields = bpy.props.BoolProperty(name="fields", default = True, update =create_update_func("fields"))
S.metaballs = bpy.props.BoolProperty(name="metaballs", default = True, update =create_update_func("metaballs"))
S.restrict_to_selected_objects = bpy.props.BoolProperty(name="restrict_to_selected_objects", default = False, update = restrict_to_selection)
bpy.types.Object.init = bpy.props.BoolProperty(name="init",description="Initial state",default = False)

sel_restrictor = False

def initial_read():
    for obj in bpy.context.scene.objects:
        obj.init = obj.hide_select


def initial_write():
    for obj in bpy.context.scene.objects:
        obj.hide_select = obj.init


class ctrl_key_operator(bpy.types.Operator):
    """Ctrl key"""
    bl_idname = "object.ctrl_operator"
    bl_label = "Ctrl Key Op"

    def invoke(self, context, event):
        global is_ctrl
        if event.ctrl:
            is_ctrl = True
        return {'FINISHED'}


class selective_panel(Header):
    bl_space_type = 'VIEW_3D'
    bl_label = "Selective"
    bl_idname = "OBJECT_PT_Selective"
    bl_region_type = 'HEADER'
    bl_context = "scene"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        p = bpy.context.user_preferences.addons[__name__].preferences
        global sel_restrictor, empties, lights, bones, cameras, meshes, nurbs

        if not sel_restrictor :
            row = layout.row()
            row.separator()
            row.operator("objects.activate", icon='TRIA_RIGHT', text='Selection Restrictor')
        else :
            row = layout.row(align=True)
            row.separator()
            row.operator("objects.activate", icon='TRIA_DOWN', text='')
            if p.mesh_button : row.prop(bpy.context.scene,"meshes", "", icon='MESH_DATA')
            if p.light_button : row.prop(bpy.context.scene,"lights", "", icon='LAMP_DATA')
            if p.camera_button : row.prop(bpy.context.scene,"cameras", "", icon='OUTLINER_DATA_CAMERA')
            if p.empty_button : row.prop(bpy.context.scene,"empties", "", icon='OUTLINER_DATA_EMPTY')
            if p.curve_button : row.prop(bpy.context.scene,"nurbs", "", icon='CURVE_DATA')
            if p.armature_button : row.prop(bpy.context.scene,"bones", "", icon='ARMATURE_DATA')
            if p.surface_button : row.prop(bpy.context.scene, "surfaces", "", icon="SURFACE_DATA")
            if p.text_button : row.prop(bpy.context.scene, "texts", "",icon="FONT_DATA")
            if p.lattice_button : row.prop(bpy.context.scene, "lattices", "", icon="LATTICE_DATA")
            if p.field_button : row.prop(bpy.context.scene, "fields", "",icon="FORCE_FORCE")
            if p.metaball_button : row.prop(bpy.context.scene, "metaballs", "", icon="META_BALL")

            if context.scene.restrict_to_selected_objects:
                row.active = False
            else:
                row.active = True
            
            row = layout.row(align=True)
            if context.active_object is not None:
                row.prop(bpy.context.scene, "restrict_to_selected_objects", "", icon="BORDER_RECT")

# PREFERENCES
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
    mesh_button = BoolProperty(name="mesh button", default=True,)
    light_button = BoolProperty(name="light button", default=True,)
    camera_button = BoolProperty(name="camera button", default=True,)
    empty_button = BoolProperty(name="empty button", default=True,)
    curve_button = BoolProperty(name="curve button", default=True,)
    armature_button = BoolProperty(name="armature button", default=True,)
    surface_button = BoolProperty(name="surface button", default=True,)
    text_button = BoolProperty(name="text button", default=False,)
    lattice_button = BoolProperty(name="lattice button", default=False,)
    field_button = BoolProperty(name="field button",default=False,)
    metaball_button = BoolProperty(name="metaball button", default=False,)
    emissive_as_light = BoolProperty(name="other light", default=False,)
    start_with = StringProperty(name="begins with:",)
    hidden_selectable = BoolProperty(name="hidden selectable", default=False,)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Display only:")
        row = layout.row(align=True)
        row.prop(self, "mesh_button", icon='MESH_DATA', text='')
        row.prop(self, "light_button", icon='LAMP', text='')
        row.prop(self, "camera_button", icon="OUTLINER_DATA_CAMERA", text='')
        row.prop(self, "empty_button", icon="OUTLINER_DATA_EMPTY", text='')
        row.prop(self, "curve_button", icon="CURVE_DATA", text='')
        row.prop(self, "armature_button", icon="ARMATURE_DATA", text='')
        row.prop(self, "surface_button", icon="SURFACE_DATA", text='')
        row.prop(self, "text_button", icon="FONT_DATA", text='')
        row.prop(self, "lattice_button", icon="LATTICE_DATA", text='')
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
