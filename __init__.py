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
submenu_draw_funcs = []
dir_path = os.path.dirname(__file__)

def draw_sdf_menu(self, context):
    self.layout.menu("NODE_MT_sdf_menu", text="SDF", icon="CON_TRANSFORM")

def append_submenu_to_parent(name, label):
    def draw(self, context):
        self.layout.menu(name, text=label.removesuffix("_"))
        if "_" in label:
            self.layout.separator(factor=1.0)
    submenu_draw_funcs.append(draw)
    bpy.types.NODE_MT_sdf_menu.append(draw)
    return draw

def generate_submenu(label, idname, contents):
    def draw(self, context):
        layout = self.layout
        for group_name in contents:
            if group_name == "_":
                layout.separator(factor=1.0)
                continue
            if group_name.startswith("+"):
                layout.label(text=group_name.removeprefix("+"))
                continue

            group_name, *tooltip = group_name.split("@")
            group_label = group_name
            for chars in ("sd", "op", "3D", "LN"):
                group_label = group_label.removeprefix(chars).removesuffix(chars)

            props = layout.operator(NODE_OT_append_group.bl_idname, text=group_label)
            props.group_name = group_name
            # Override tooltip
            if tooltip != []:
                props.tooltip = tooltip[0]


    submenu_class = type(idname,(bpy.types.Menu,),
        {
            "bl_idname": idname,
            "bl_label": label,
            "draw": draw,
        }
    )

    submenu_classes.append(submenu_class)
    bpy.utils.register_class(submenu_class)


class NODE_MT_sdf_menu(Menu):
    bl_label = "SDF"
    bl_idname = "NODE_MT_sdf_menu"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ShaderNodeTree"

    def draw(self, context):
        pass

class NODE_OT_append_group(Operator):
    bl_idname = "b3dsdf.append_group"
    bl_label = "Append Node Group"
    bl_description = "Append Node Group"
    bl_options = {"REGISTER", "UNDO"}

    group_name: StringProperty()
    tooltip: StringProperty()

    # adapted from https://github.com/blender/blender/blob/master/release/scripts/startup/bl_operators/node.py
    @staticmethod
    def store_mouse_cursor(context, event):
        context.space_data.cursor_location_from_region(event.mouse_region_x, event.mouse_region_y)

    @staticmethod
    def search_for_blendfile():
        for file in os.listdir(dir_path):
            if file.endswith(".blend"):
                return os.path.join(dir_path, file)
        else:
            raise FileNotFoundError("No .blend File in directory " + dir_path)       

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ShaderNodeTree"

    @classmethod
    def description(self, context, props):
        return props.tooltip

    def execute(self, context):
        if self.group_name not in bpy.data.node_groups:
            old_groups = set(bpy.data.node_groups)

            filepath = self.search_for_blendfile()
            with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.node_groups.append(self.group_name)
    
            added_groups = tuple(set(bpy.data.node_groups)-old_groups)
            for group in added_groups:
                for node in group.nodes:
                    if node.type == "GROUP":
                        node.node_tree = bpy.data.node_groups[node.node_tree.name.split(".")[0]]
            for group in added_groups:
                group_name = group.name.split(".")
                #remove nodegroup if duplicate already exists
                if len(group_name) >= 2 and group_name[0] in bpy.data.node_groups:
                    bpy.data.node_groups.remove(group)              

        bpy.ops.node.add_group(name=self.group_name)
        context.active_node.location = context.space_data.cursor_location
        bpy.ops.node.translate_attach_remove_on_cancel("INVOKE_DEFAULT")
        return {"FINISHED"}

    def invoke(self, context, event):
        self.store_mouse_cursor(context, event)
        return self.execute(context)


def register():
    submenu_classes.clear()
    submenu_draw_funcs.clear()

    with open(os.path.join(dir_path, "shader_nodes.json"), "r") as f:
        sdf_group_cache = json.loads(f.read())

    if not hasattr(bpy.types, "NODE_MT_sdf_menu"):
        bpy.utils.register_class(NODE_MT_sdf_menu)
        bpy.types.NODE_MT_add.append(draw_sdf_menu)
    bpy.utils.register_class(NODE_OT_append_group)

    # adapted from https://github.com/blender/blender/blob/master/release/scripts/modules/nodeitems_utils.py
    for submenu_label, submenu_contents in sdf_group_cache.items():
        submenu_idname = "NODE_MT_category_" + submenu_label.removesuffix("_").replace(" ", "_").replace("-", "_")

        generate_submenu(submenu_label, submenu_idname, submenu_contents)
        append_submenu_to_parent(submenu_idname, submenu_label)


def unregister():
    for draw_func in submenu_draw_funcs:
        bpy.types.NODE_MT_sdf_menu.remove(draw_func)
    for cls in submenu_classes:
        bpy.utils.unregister_class(cls)

    if hasattr(bpy.types, "NODE_MT_sdf_menu"):
        bpy.utils.unregister_class(NODE_MT_sdf_menu)
        bpy.types.NODE_MT_add.remove(draw_sdf_menu)
    bpy.utils.unregister_class(NODE_OT_append_group)
