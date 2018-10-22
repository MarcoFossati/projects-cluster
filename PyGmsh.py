# created by James Black
# 21/10/2018
# This script is used to carry out any meshing procedures using Gmsh Open-Source tool.

import subprocess


def convert_cad_2_geo():
    print("Converting CAD files to .geo format...")


# function that carries out basic default meshing
def do_basic_mesh(gmsh_path, path_cad, dimension, output_file):
    print("Starting mesh creation...")
    print("PyGmsh : do_basic_mesh : gmsh_path" + gmsh_path)
    print("PyGmsh : do_basic_mesh : path_cad" + path_cad)
    print("PyGmsh : do_basic_mesh : dimension" + dimension)
    print("PyGmsh : do_basic_mesh : output_file" + output_file)
    subprocess.call("{0} {1} {2} -o {3}".format(gmsh_path, path_cad, dimension, output_file), shell=True)
    print("Meshing done.")


# function that will display the given mesh file in a Gmsh window
def show_mesh(gmsh_path, output_file):
    print("PyGmsh : show_mesh : gmsh_path : " + gmsh_path)
    print("PyGmsh : show_mesh : output_file : " + output_file)
    subprocess.call("{0} -open {1}".format(gmsh_path, output_file))
