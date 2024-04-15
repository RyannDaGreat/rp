"""
Ryan Burgert, April 2024

This tool is meant to solve a problem: when I have powerpoint files with MP4 files, and I upload them to Google Slides, all the videos are replaced by images! What the fuck?
Turns out the official way to add videos to Google Slides is to upload each video to Google Drive, then in the Google Slides interface select them for insertion one by one. Very annoying.

This script changes a powerpoint file so that when its uploaded to Google Slides, the MP4 animations are all converted to GIF's!
Whatsmore - it doesn't destroy *anything* in the original powerpoint file - you can use it as normal!

How does it work?
Well, those static images google slides replaces your videos with - they're thumnails that can be found in the powerpoint file, that are automatically created when you upload an MP4 to powerpoint.
Did you know that .pptx files are actually zip files? Yeah! You can unzip them and look inside - you'll find a file structure!
Usually these thumbnails are png images - but we can replace them with GIF's of the original videos - and these will be animated when viewed in a web browser!
Note that this causes some 'corruption' to the powerpoint file (no damage that I can see) - but to fix it open the new pptx file this script creates, let powerpoint correct the errors, then re-save it.
That file can be uploaded to Google Slides and all the animations will work!

To use this code:
    process_powerpoint_file('/Users/ryan/Desktop/Eyeline_April2_2024.pptx')

"""

from rp import *

__all__=['process_powerpoint_file']

def _get_thumbnail_mapping(index_xml, slide_xml):    
    #https://chat.openai.com/share/35113188-1527-4309-ae6e-cbb0c4643218
    import xml.etree.ElementTree as ET

    # Parse the XML data
    index_root = ET.fromstring(index_xml)
    slide_root = ET.fromstring(slide_xml)

    # Extract relationship mappings from the index XML
    relationship_map = {}
    for relationship in index_root.findall("{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
        r_id = relationship.get("Id")
        target = relationship.get("Target")
        relationship_map[r_id] = target.split('/')[-1]  # Extract the file name

    # Now find video to image mappings in the slide XML
    video_thumbnail_map = {}
    for pic in slide_root.findall(".//{http://schemas.openxmlformats.org/presentationml/2006/main}pic"):
        nv_pr = pic.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}nvPr")
        if nv_pr is not None and nv_pr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}videoFile") is not None:
            video_r_id = nv_pr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}videoFile").get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}link")
            blip = pic.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
            if blip is not None:
                image_r_id = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                video_file = relationship_map.get(video_r_id, None)
                image_file = relationship_map.get(image_r_id, None)
                if video_file and image_file:
                    video_thumbnail_map[video_file] = image_file

    return video_thumbnail_map

def get_thumbnail_mappings(pptx_root='.'):
    #Returns something like {'media1.mp4': 'image1.png', 'media2.mp4': 'image2.png', 'media3.mp4': 'image3.png', 'media4.mp4': 'image4.png' ... }
    slide_xmls=rp.get_all_files(pptx_root,'ppt/slides',file_extension_filter='xml',sort_by='number')
    rel_xmls=rp.get_all_files(pptx_root,'ppt/slides/_rels',file_extension_filter='rels',sort_by='number')
    print(pptx_root)

    thumbnail_mappings={}
    for rel_xml,slide_xml in zip(rel_xmls,slide_xmls):
        slide_thumbnail_mapping=_get_thumbnail_mapping(
            text_file_to_string(rel_xml),
            text_file_to_string(slide_xml),
        )
        thumbnail_mappings.update(slide_thumbnail_mapping)
    return gather_vars('thumbnail_mappings slide_xmls rel_xmls')

def convert_mp4_to_gif(mp4_path,gif_path=None):
    if path_exists(gif_path):
        return gif_path#Don't re-do work for no reason
    pip_import('moviepy')
    from moviepy.editor import VideoFileClip
    videoClip = VideoFileClip(mp4_path)
    gif_path=gif_path or with_file_extension(mp4_path,'gif',replace=True)
    print(gif_path)
    videoClip.write_gif(gif_path)
    return gif_path

def process_powerpoint_file(pptx_path):
    folder_name = strip_file_extension(pptx_path) + "_extracted"
    folder_name = get_unique_copy_path(folder_name)
    folder_path = with_folder_name(pptx_path,folder_name)
    unzip_to_folder(pptx_path, folder_path, treat_as="zip")
    assert folder_exists(folder_path)
    try:
        thumbnail_mappings, slide_xmls, rel_xmls = destructure(get_thumbnail_mappings(pptx_root=folder_path))

        with SetCurrentDirectoryTemporarily(path_join(folder_path,'ppt','media')):        
            replacements={}
            for mp4,thumbnail in thumbnail_mappings.items():
                fansi_print(mp4+'  –––––  '+thumbnail,'green')
                gif_path=convert_mp4_to_gif(mp4,with_file_extension(thumbnail,'gif',replace=True))
                replacements[thumbnail]=gif_path
                
        print(replacements)

        for file in slide_xmls+rel_xmls:    
            file_text=text_file_to_string(file)
            for before,after in replacements.items():
                file_text=file_text.replace(before,after)
            string_to_text_file(file,file_text)
                
        new_pptx_path=make_zip_file_from_folder(folder_path)
        new_pptx_path=rename_file(new_pptx_path,with_file_extension(new_pptx_path,'pptx',replace=True))

        print()
        print()
        fansi_print("CONVERSION NEARLY COMPLETE!",'yellow','bold')
        fansi_print("Please re-save this using powerpoint, which fixes corruption errors caused by this process",'yellow','bold')
        fansi_print("The file you save in powerpoint can be directly uploaded into Google Slides, with working animations!",'yellow','bold')
        if input_yes_no('Would you like to open it now?'):
            open_file_with_default_application(new_pptx_path)
        

        return new_pptx_path
    
    
    finally:
        delete_directory(folder_path)

#EXAMPLE:
#process_powerpoint_file('/Users/ryan/Desktop/Eyeline_April2_2024.pptx')
