import bpy

# este script es para convertir los MixRGB de Blender 3.4 a los de Blender 3.3 ya que son incompatibles.
# tienes que ejecutar este script en Blender 3.3

for obj in bpy.data.objects:
    if obj.type != 'MESH' and 'Domain' not in obj:
        continue
    #    
    for mslot in obj.material_slots: 
        material = mslot.material
        #   
        for main_node in material.node_tree.nodes:
            if main_node.type != 'GROUP':
                continue
            nodes = main_node.node_tree.nodes
            #
            for node in nodes:
                if node.type == '':
                    #
                    print('Node name:', node.name)
                    new_node = nodes.new('ShaderNodeMixRGB')
                    new_node.location = node.location.copy()
                    #new_node.dimensions = node.dimensions (read only)
                    #
                    # conectando las entradas a los nodos nuevos:
                    for i in range(len(node.inputs)):
                        inputx = node.inputs[i]
                        new_factor_input = None
                        new_color1_input = None
                        new_color2_input = None
                        # blender 3.3 es incapaz de leer el blend_type de 3.4 :(
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
                            left_node = inputx.links[0].from_node
                            left_output = inputx.links[0].from_socket
                            #print("left_node:", left_node.name)
                            #print(left_output)
                            if new_factor_input:
                                main_node.node_tree.links.new(new_node.inputs[new_factor_input], left_output)
                            if new_color1_input:
                                main_node.node_tree.links.new(new_node.inputs[new_color1_input], left_output)
                            if new_color2_input:
                                main_node.node_tree.links.new(new_node.inputs[new_color2_input], left_output)
                    # conectando las salidas a los nodos nuevos:
                    for i in range(len(node.outputs)):
                        outputx = node.outputs[i]
                        if len(outputx.links) > 0:
                            print(i, outputx.name)
                            new_factor_output = None
                            if i == 2 and outputx.name == 'Result':
                                new_factor_output = 'Color'
                            #
                            right_node = outputx.links[0].to_node
                            right_node_input = outputx.links[0].to_socket
                            print("right_node:", right_node.name)
                            print("right_node_input:", right_node_input)
                            if new_factor_output:
                                print("new_factor_output", new_factor_output)
                                main_node.node_tree.links.new(new_node.outputs[new_factor_output], right_node_input)
                    #
                    new_node.name = node.name
                    new_node.select = False
                    main_node.node_tree.nodes.remove(node)
