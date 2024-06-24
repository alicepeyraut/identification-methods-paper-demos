#coding=utf8

################################################################################

import os
import dolfin

import myPythonLibrary as mypy
import dolfin_warp     as dwarp
from generate_images_and_meshes_from_RivlinCube import generate_images_and_meshes_from_RivlinCube


################################################################################

def generate_images(model_error_b=False):
    images_folder = "generate_images"

    dim_lst  = [ ]
    dim_lst += [2]
    # dim_lst += [3]

    deformation_type_lst  = [       ]
    deformation_type_lst += ["grav"]
    deformation_type_lst += ["compx"]

    texture_type_lst  = [         ]
    texture_type_lst += ["tagging"]

    noise_level_lst  = [   ]
    noise_level_lst += [0.0]
    noise_level_lst += [0.1]
    noise_level_lst += [0.2]
    noise_level_lst += [0.3]

    n_runs_for_noisy_images = 10

    mesh_size_lst  = [        ]
    mesh_size_lst += [0.1     ]
    mesh_size_lst += [0.1/2**1] # 0.05

    if model_error_b:
        regul_b_lst  = []
        regul_b_lst += [0.0]
        regul_b_lst += [0.24]
        regul_b_lst += [0.27]
        regul_b_lst += [0.3]
        regul_b_lst += [0.33]
        regul_b_lst += [0.36]
    else:
        regul_b_lst = [0.0]

    regul_level_lst  = [        ]
    regul_level_lst += [0.1*2**1] # 0.2
    regul_level_lst += [0.1     ] # 0.1
    regul_level_lst += [0.1/2**1] # 0.05
    regul_level_lst += [0.] # 0.0

    do_generate_images = 1
    do_generate_meshes = 1
    do_run_warp = 1
################################################################################



############################################################ generate_images ###

    if (do_generate_images):
        for dim in dim_lst:
            for deformation_type in deformation_type_lst:

                # Need to run the model before generating all images in parallel
                print("*** running model ***"              )
                print("dim:"             , dim             )
                print("deformation_type:", deformation_type)

                n_voxels        = 100
                texture_type    = "no"
                noise_level     = 0
                run_model       = True
                generate_images = False

    
                generate_images_and_meshes_from_RivlinCube(
                        images_n_dim     = dim             ,
                        images_n_voxels  = n_voxels        ,
                        deformation_type = deformation_type,
                        texture_type     = texture_type    ,
                        noise_level      = noise_level     ,
                        run_model        = run_model       ,
                        generate_images  = generate_images )

                # Now we can generate all images in parallel
                for texture_type in texture_type_lst:
                    for noise_level  in noise_level_lst :

                        n_runs          = n_runs_for_noisy_images if (noise_level > 0) else 1
                        run_model       = False
                        generate_images = True

                        for k_run in range(1, n_runs+1):

                            print("*** generate_images ***"            )
                            print("dim:"             , dim             )
                            print("deformation_type:", deformation_type)
                            print("texture_type:"    , texture_type    )
                            print("noise_level:"     , noise_level     )
                            print("k_run:"           , k_run           )

                            generate_images_and_meshes_from_RivlinCube(
                                images_n_dim     = dim                            ,
                                images_n_voxels  = n_voxels                       ,
                                deformation_type = deformation_type               ,
                                texture_type     = texture_type                   ,
                                noise_level      = noise_level                    ,
                                k_run            = k_run if (n_runs > 1) else None,
                                run_model        = run_model                      ,
                                generate_images  = generate_images                )


############################################################ generate_meshes ###

    if (do_generate_meshes):
        for dim              in dim_lst            :
            for deformation_type in deformation_type_lst:
                for mesh_size        in mesh_size_lst       :

                    print("*** generate_meshes ***"            )
                    print("dim:"             , dim             )
                    print("deformation_type:", deformation_type)
                    print("mesh_size:"       , mesh_size       )

                    n_voxels        = 1
                    texture_type    = "no"
                    noise_level     = 0
                    run_model       = True
                    generate_images = False

                    generate_images_and_meshes_from_RivlinCube(
                            images_n_dim     = dim                            ,
                            images_n_voxels  = n_voxels                       ,
                            mesh_size        = mesh_size                      ,
                            deformation_type = deformation_type               ,
                            texture_type     = texture_type                   ,
                            noise_level      = noise_level                    ,
                            run_model        = run_model                      ,
                            generate_images  = generate_images,
                            refine=True                )

################################################################### run_warp ###
    if (do_run_warp):
        for dim in dim_lst             :
            for deformation_type in deformation_type_lst:
                for texture_type     in texture_type_lst    :
                    for noise_level      in noise_level_lst     :

                        n_runs = n_runs_for_noisy_images if (noise_level > 0) else 1

                        for k_run       in range(1, n_runs+1):
                            for mesh_size   in mesh_size_lst     :
                                for regul_b     in regul_b_lst       :
                                    for regul_level in regul_level_lst   :
                                        if deformation_type=="compx":
                                            regul_type="discrete-equilibrated-tractions-tangential"
                                            working_folder="run_warp_compx"
                                        elif deformation_type=="grav":
                                            regul_type="discrete-equilibrated-tractions-normal-tangential"
                                            working_folder="run_warp_grav"
                                        else:
                                            print("Deformation type should be either compx or grav...")

                                        regul_model = "ciarletgeymonatneohookean"
                                        regul_poisson = 0.3

                                        print("*** run_warp ***"                   )
                                        print("deformation_type:", deformation_type)
                                        print("texture_type:"    , texture_type    )
                                        print("noise_level:"     , noise_level     )
                                        print("k_run:"           , k_run           )
                                        print("mesh_size:"       , mesh_size       )
                                        print("regul_type:"      , regul_type      )
                                        print("regul_model:"     , regul_model     )
                                        print("regul_level:"     , regul_level     )
                                        print("regul_poisson:"   , regul_poisson   )
                                        print("regul_b:"         , regul_b         )

                                        if   (dim == 2): images_basename = "square"
                                        elif (dim == 3): images_basename = "cube"
                                        images_basename += "-"+deformation_type
                                        images_basename += "-"+texture_type
                                        images_basename += "-noise="+str(noise_level)
                                        if (n_runs > 1):
                                            images_basename += "-run="+str(k_run).zfill(2)

                                        mesh_folder = images_folder

                                        if   (dim == 2): mesh_basename = "square"
                                        elif (dim == 3): mesh_basename = "cube"
                                        mesh_basename += "-"+deformation_type
                                        mesh_basename += "-h="+str(mesh_size)
                                        mesh_basename += "-mesh"
                                        if mesh_size==0.1:
                                            mesh_basename=[mesh_basename+"coarse", mesh_basename+"refined"]
                                        else:
                                            mesh_basename=mesh_basename
                                        

                                        working_basename = images_basename
                                        working_basename += "-h="+str(mesh_size)
                                        working_basename += "-"+regul_type
                                        working_basename += "-regul="+str(regul_level)
                                        working_basename += "-b="+str(regul_b)

                                        relax_type                                  = "backtracking"
                                        tol_dU                                      = 1e-2
                                        n_iter_max                                  = 100
                                        normalize_energies                          = 1
                                        continue_after_fail                         = 1
                                        write_VTU_files                             = 1
                                        write_VTU_files_with_preserved_connectivity = 1
                                        print_iterations                            = 0

                                        if mesh_size==0.1:
                                            refinement_levels=[0,1]
                                            dwarp.warp_and_refine(
                                                working_folder                              = working_folder                             ,
                                                working_basename                            = working_basename                           ,
                                                images_folder                               = images_folder                              ,
                                                images_basename                             = images_basename                            ,
                                                mesh_folder                                 = mesh_folder                                ,
                                                mesh_basenames                              = mesh_basename                              ,
                                                # mesh                                        = dolfin.Mesh(mesh_folder+"/"+mesh_basename+".xml"),
                                                regul_type                                  = regul_type                                 ,
                                                regul_model                                 = regul_model                                ,
                                                regul_level                                 = regul_level                                ,
                                                regul_poisson                               = regul_poisson                              ,
                                                regul_b                                     = [regul_b]+[0.]*(dim-1)                     ,
                                                relax_type                                  = relax_type                                 ,
                                                normalize_energies                          = normalize_energies                         ,
                                                tol_dU                                      = tol_dU                                     ,
                                                n_iter_max                                  = n_iter_max                                 ,
                                                continue_after_fail                         = continue_after_fail                        ,
                                                refinement_levels                           = refinement_levels                          ,
                                                print_iterations                            = print_iterations                           )      
                                        else:
                                            dwarp.warp(
                                                working_folder                              = working_folder                             ,
                                                working_basename                            = working_basename                           ,
                                                images_folder                               = images_folder                              ,
                                                images_basename                             = images_basename                            ,
                                                mesh_folder                                 = mesh_folder                                ,
                                                mesh_basename                               = mesh_basename                              ,
                                                regul_type                                  = regul_type                                 ,
                                                regul_model                                 = regul_model                                ,
                                                regul_level                                 = regul_level                                ,
                                                regul_poisson                               = regul_poisson                              ,
                                                regul_b                                     = [regul_b]+[0.]*(dim-1)                     ,
                                                relax_type                                  = relax_type                                 ,
                                                normalize_energies                          = normalize_energies                         ,
                                                tol_dU                                      = tol_dU                                     ,
                                                n_iter_max                                  = n_iter_max                                 ,
                                                continue_after_fail                         = continue_after_fail                        ,
                                                write_VTU_files                             = write_VTU_files                            ,
                                                write_VTU_files_with_preserved_connectivity = write_VTU_files_with_preserved_connectivity,
                                                print_iterations                            = print_iterations                           )
                                            
    return
                                