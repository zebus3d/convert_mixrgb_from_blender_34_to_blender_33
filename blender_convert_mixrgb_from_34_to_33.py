import bpy
from bpy.types import ShaderNodeTree

# This script is for convert MixRGB nodes from Blender 3.4 to MixRGB nodes to Blender 3.3, because 3.4 are incompatibles in 3.3.
# Run this script in Blender 3.3

def process_nodes(root_nodes):
    # print('root_nodes', root_nodes)
    #
    if isinstance(root_nodes, ShaderNodeTree):
        #
        nodes = root_nodes.nodes
        #
        for node in nodes:
            if node.type == 'FRAME':
                continue
            #
            if node.type == 'GROUP':
                if hasattr(node, "node_tree"):
                    process_nodes(node.node_tree)
            else:
                if node.type == '':
                    # print('root_nodes, nodes, node.name', root_nodes, nodes, node.name)
                    #
                    #print('Node name:', node.name)
                    new_node = nodes.new('ShaderNodeMixRGB')
                    new_node.location = node.location.copy()
                    # new_node.dimensions = node.dimensions (read only)
                    #
                    # connecting the inputs to the new nodes:
                    for i in range(len(node.inputs)):
                        inputx = node.inputs[i]
                        new_factor_input = None
                        new_color1_input = None
                        new_color2_input = None
                        # blender 3.3 cant read the blend_type from 3.4 :(
                        # new_node.blend_type = node.blend_type
                        if i == 0 and inputx.name == 'Factor':
                            new_factor_input = 'Fac'
                            new_node.inputs[new_factor_input].default_value = inputx.default_value
                        if i == 6 and inputx.name == 'A':
                            new_color1_input = 'Color1'
                            new_node.inputs[new_color1_input].default_value = inputx.default_value
                        if i == 7 and inputx.name == 'B':
                            new_color2_input = 'Color2'
                            new_node.inputs[new_color2_input].default_value = inputx.default_value
                        #
                        if len(inputx.links) > 0:
                            #
                            #print(i, inputx.name)
                            #
                            # left_node = inputx.links[0].from_node
                            left_output = inputx.links[0].from_socket
                            #print("left_node:", left_node.name)
                            # print(left_output)
                            if new_factor_input:
                                root_nodes.links.new(new_node.inputs[new_factor_input], left_output)
                            if new_color1_input:
                                root_nodes.links.new(new_node.inputs[new_color1_input], left_output)
                            if new_color2_input:
                                root_nodes.links.new(new_node.inputs[new_color2_input], left_output)
                    # connecting outputs to the new nodes:
                    for i in range(len(node.outputs)):
                        outputx = node.outputs[i]
                        if len(outputx.links) > 0:
                            #print(i, outputx.name)
                            new_factor_output = None
                            if i == 2 and outputx.name == 'Result':
                                new_factor_output = 'Color'
                            #
                            right_node = outputx.links[0].to_node
                            right_node_input = outputx.links[0].to_socket
                            #print("right_node:", right_node.name)
                            #print("right_node_input:", right_node_input)
                            if new_factor_output:
                                print("new_factor_output", new_factor_output)
                                root_nodes.links.new(new_node.outputs[new_factor_output], right_node_input)
                    #
                    new_node.name = node.name
                    new_node.select = False
                    nodes.remove(node)
    #
    # print("\n")


for obj in bpy.data.objects:
    if obj.type != 'MESH' and 'Domain' not in obj:
        continue
    #
    for mslot in obj.material_slots:
        material = mslot.material
        #
        root_nodes = material.node_tree
        process_nodes(root_nodes)
