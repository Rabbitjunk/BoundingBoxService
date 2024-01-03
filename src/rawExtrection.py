
import torch
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from threading import Thread
from pdf2image import convert_from_path
from pathlib import Path
from craft_text_detector import (
    read_image,
    load_craftnet_model,
    load_refinenet_model,
    get_prediction,
    export_detected_regions,
    export_extra_results,
    empty_cuda_cache
)
from src.Classes.Rectangle import rectangles_to_array

from src.refineExtractions import loadRefinedRectangle
from PIL import Image
def extractRawRegions(filepath):
    pages = convert_from_path(filepath, 500, poppler_path=r'poppler-23.11.0\Library\bin')
        # Use os.path.basename to get the filename from the path
    filename = os.path.basename(filepath)
        # Use os.path.splitext to split the filename and extension
    filename_without_extension, _ = os.path.splitext(filename)
    output_dir = f'outputs/{filename_without_extension}/'

    cretaFolderIfNeeded(output_dir)
    Files = []
    for count, page in enumerate(pages):
        cretaFolderIfNeeded(f'{output_dir}/{count}/')
        page.save(f'{output_dir}/{count}/orginal.jpg')
        Files.append(f'{output_dir}/{count}/orginal.jpg')

    
    if torch.cuda.is_available() == True:
        refine_net = load_refinenet_model(cuda=True)
        craft_net = load_craftnet_model(cuda=True)
    else:
        refine_net = load_refinenet_model(cuda=False)
        craft_net = load_craftnet_model(cuda=False)
    
    for count,file in enumerate(Files):

        # read image
        image = read_image(file)
        output_dir = f'outputs/{filename_without_extension}/{count}/'
        cretaFolderIfNeeded(output_dir)

        # load models
        # perform prediction
        if torch.cuda.is_available() == True:
            prediction_result = get_prediction(
                image=file,
                craft_net=craft_net,
                refine_net=refine_net,
                text_threshold=0.7,
                link_threshold=0.4,
                low_text=0.4,
                cuda=True,
                long_size=1280
            )
        else:
            prediction_result = get_prediction(
                image=file,
                craft_net=craft_net,
                refine_net=refine_net,
                text_threshold=0.7,
                link_threshold=0.4,
                low_text=0.4,
                cuda=False,
                long_size=1280
            )
        # export heatmap, detection points, box visualization
        export_extra_results(
            image=image,
            regions=prediction_result["boxes"],
            heatmaps=prediction_result["heatmaps"],
            output_dir=output_dir,
        )
    # unload models from gpu
    empty_cuda_cache()
    os.remove(filepath)
    print(f"Thread for {filename_without_extension} finished")

    return  f'outputs/{filename_without_extension}/'

def cretaFolderIfNeeded(folder_path):
    if os.path.exists(folder_path)== False:
        os.makedirs(folder_path)


def extractdefiniedRegions(filepath):
    if os.path.exists(filepath):
        inhalt = os.listdir(filepath)
        allRectangles=[]
        if torch.cuda.is_available() == True:
                refine_net = load_refinenet_model(cuda=True)
                craft_net = load_craftnet_model(cuda=True)
        else:
                refine_net = load_refinenet_model(cuda=False)
                craft_net = load_craftnet_model(cuda=False)
        for element in inhalt:
            element_pfad = os.path.join(filepath, element)
            allRectangles = loadRefinedRectangle(element_pfad)
            image = read_image(os.path.join(element_pfad,"orginal.jpg"))
            output_dir = f'{element_pfad}/Parts/'
            cretaFolderIfNeeded(output_dir)
            export_detected_regions(
                image=image,
                regions=rectangles_to_array(allRectangles),
                output_dir=output_dir,
                rectify= True
                )
            