# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "b3dsdf",
    "author": "cmzw",
    "description": "A toolkit of signed distance functions, operators and utility nodegroups",
    "blender": (2, 83, 0),
    "version": (0, 9, 0),
    "location": "Shader Editor > Add > SDF",
    "tracker_url": "https://github.com/williamchange/b3dsdf/issues/new",
    "doc_url": "https://github.com/williamchange/b3dsdf/wiki/Examples",
    "category": "Node",
}
import json
import bpy
import os
from bpy.types import Operator, Menu
from bpy.props import StringProperty


submenu_classes = []
category_draw_funcs = []
dir_path = os.path.dirname(__file__)

def add_sdf_button(self, context):
    self.layout.menu("NODE_MT_sdf_menu", text="SDF", icon="CON_TRANSFORM")

class NODE_MT_sdf_menu(Menu):
    bl_label = "SDF"
    bl_idname = "NODE_MT_sdf_menu"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ShaderNodeTree"

    def draw(self, context):
        pass

class NODE_OT_append_group(Operator):
    """Add a node group"""

    bl_idname = "b3dsdf.append_group"
    bl_label = "Append Node Group"
    bl_description = "Append Node Group"
    bl_options = {"REGISTER", "UNDO"}

    group_name: StringProperty()
    tooltip: StringProperty()

    # adapted from https://github.com/blender/blender/blob/master/release/scripts/startup/bl_operators/node.py
    @staticmethod
    def store_mouse_cursor(context, event):
        space = context.space_data
        if context.region.type == "WINDOW":
            space.cursor_location_from_region(event.mouse_region_x, event.mouse_region_y)
        else:
            space.cursor_location = space.edit_tree.view_center

    @classmethod
    def poll(cls, context):
        return context.space_data.node_tree

    @classmethod
    def description(self, context, props):
        return props.tooltip

    def execute(self, context):
        if self.group_name not in bpy.data.node_groups:
            for file in os.listdir(dir_path):
                if file.endswith(".blend"):
                    filepath = os.path.join(dir_path, file)
                    break
            else:
                raise FileNotFoundError("No .blend File in directory " + dir_path)
        
            with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.node_groups.append(self.group_name)

        bpy.ops.node.add_group(name=self.group_name)
        bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")
        return {"FINISHED"}

    def invoke(self, context, event):
        self.store_mouse_cursor(context, event)
        return self.execute(context)


def register():
    submenu_classes.clear()
    category_draw_funcs.clear()

    with open(os.path.join(dir_path, "shader_nodes.json"), "r") as f:
        sdf_group_cache = json.loads(f.read())

    if not hasattr(bpy.types, "NODE_MT_sdf_menu"):
        bpy.utils.register_class(NODE_MT_sdf_menu)
        bpy.types.NODE_MT_add.append(add_sdf_button)
    bpy.utils.register_class(NODE_OT_append_group)

    # adapted from https://github.com/blender/blender/blob/master/release/scripts/modules/nodeitems_utils.py
    for submenu_label in sdf_group_cache.keys():
        def submenu_draw(self, context):
            layout = self.layout
            for group_name in sdf_group_cache[self.bl_label]:
                if group_name == "_":
                    layout.separator(factor=1.0)
                    continue
                if group_name.startswith("+"):
                    layout.label(text=group_name.removeprefix("+"))
                    continue

                group_name, *tooltip = group_name.split("@")
                props = layout.operator(
                    NODE_OT_append_group.bl_idname,
                    text=group_name
                    .replace("sd", "")
                    .replace("op", "")
                    .replace("3D", "")
                    .replace("LN", ""),
                )
                props.group_name = group_name
                # Override tooltip
                if tooltip != []:
                    props.tooltip = tooltip[0]


        itemid = submenu_label.removesuffix("_").replace(" ", "_").replace("-", "_")
        submenu_idname = "NODE_MT_category_" + itemid
        submenu_class = type(submenu_idname,(bpy.types.Menu,),
            {
                "bl_idname": submenu_idname,
                "bl_label": submenu_label,
                "draw": submenu_draw,
            }
        )
        
        def generate_draw_func(name, label):
            def draw(self, context):
                self.layout.menu(name, text=label.removesuffix("_"))
                if "_" in label:
                    self.layout.separator(factor=1.0)
            return draw
        draw_func = generate_draw_func(submenu_idname, submenu_label)    

        bpy.utils.register_class(submenu_class)
        bpy.types.NODE_MT_sdf_menu.append(draw_func)

        submenu_classes.append(submenu_class)
        category_draw_funcs.append(draw_func)


def unregister():
    for draw_func in category_draw_funcs:
        bpy.types.NODE_MT_sdf_menu.remove(draw_func)

    if hasattr(bpy.types, "NODE_MT_sdf_menu"):
        bpy.utils.unregister_class(NODE_MT_sdf_menu)
        bpy.types.NODE_MT_add.remove(add_sdf_button)
    bpy.utils.unregister_class(NODE_OT_append_group)
