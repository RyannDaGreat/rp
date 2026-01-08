import rp
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

__all__=['process_powerpoint_file', 'get_video_sizes', 'get_video_placements']

EMU_PER_INCH = 914400


from dataclasses import dataclass
from functools import cached_property


@dataclass
class VideoPlacement:
    """
    Info about a single video placement on a slide.
    All positions/sizes in inches. Origin is top-left corner of slide;
    x increases rightward, y increases downward.
    See: http://officeopenxml.com/drwSp-location.php
    """
    x: float  # left edge
    y: float  # top edge
    width: float
    height: float
    slide_width: float
    slide_height: float
    slide_number: int

    @cached_property
    def visibility(self) -> str:
        """Return 'onscreen', 'partial', or 'offscreen'."""
        x2, y2 = self.x + self.width, self.y + self.height
        if x2 <= 0 or self.x >= self.slide_width or y2 <= 0 or self.y >= self.slide_height:
            return 'offscreen'
        if self.x >= 0 and self.y >= 0 and x2 <= self.slide_width and y2 <= self.slide_height:
            return 'onscreen'
        return 'partial'

    def __repr__(self):
        return f'VideoPlacement(slide={self.slide_number}, x={self.x:.2f}, y={self.y:.2f}, w={self.width:.2f}, h={self.height:.2f}, {self.visibility})'


def get_video_placements(pptx_root='.') -> dict[str, list[VideoPlacement]]:
    """
    Get all video files with position, size, and visibility from an unzipped PowerPoint.
    All measurements in inches.

    >>> placements = get_video_placements('Demo1')
    >>> placements['media1.mp4'][0].visibility
    'onscreen'
    >>> placements['media3.mp4'][0].visibility
    'offscreen'
    >>> placements['media4.mp4'][0].visibility
    'partial'
    """
    import xml.etree.ElementTree as ET

    ns_rel = 'http://schemas.openxmlformats.org/package/2006/relationships'
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    # Get slide size from presentation.xml
    pres_xml = rp.path_join(pptx_root, 'ppt', 'presentation.xml')
    pres_root = ET.fromstring(rp.text_file_to_string(pres_xml))
    sld_sz = pres_root.find(f'{{{ns_p}}}sldSz')
    slide_w = int(sld_sz.get('cx', 0)) / EMU_PER_INCH
    slide_h = int(sld_sz.get('cy', 0)) / EMU_PER_INCH

    slide_xmls = rp.get_all_files(pptx_root, 'ppt/slides', file_extension_filter='xml', sort_by='number')
    rel_xmls = rp.get_all_files(pptx_root, 'ppt/slides/_rels', file_extension_filter='rels', sort_by='number')

    result: dict[str, list[VideoPlacement]] = {}

    for slide_num, (rel_xml, slide_xml) in enumerate(zip(rel_xmls, slide_xmls), 1):
        rid_to_video = {}
        for rel in ET.fromstring(rp.text_file_to_string(rel_xml)).findall(f'{{{ns_rel}}}Relationship'):
            if 'video' in rel.get('Type', ''):
                rid_to_video[rel.get('Id')] = rp.get_file_name(rel.get('Target', ''))

        root = ET.fromstring(rp.text_file_to_string(slide_xml))
        for pic in root.findall(f'.//{{{ns_p}}}pic'):
            video_file = pic.find(f'.//{{{ns_a}}}videoFile')
            if video_file is None:
                continue
            rid = video_file.get(f'{{{ns_r}}}link')
            if rid not in rid_to_video:
                continue
            xfrm = pic.find(f'{{{ns_p}}}spPr/{{{ns_a}}}xfrm')
            if xfrm is None:
                continue
            off = xfrm.find(f'{{{ns_a}}}off')
            ext = xfrm.find(f'{{{ns_a}}}ext')
            if off is None or ext is None:
                continue
            filename = rid_to_video[rid]
            placement = VideoPlacement(
                x=int(off.get('x', 0)) / EMU_PER_INCH,
                y=int(off.get('y', 0)) / EMU_PER_INCH,
                width=int(ext.get('cx', 0)) / EMU_PER_INCH,
                height=int(ext.get('cy', 0)) / EMU_PER_INCH,
                slide_width=slide_w,
                slide_height=slide_h,
                slide_number=slide_num,
            )
            result.setdefault(filename, []).append(placement)

    return result


def get_video_sizes(pptx_root='.') -> dict[str, list[tuple[float, float]]]:
    """
    Get all video files and their display sizes (in inches) from an unzipped PowerPoint.

    >>> 'media1.mp4' in get_video_sizes('Demo1')
    True
    """
    return {
        name: [(p.width, p.height) for p in placements]
        for name, placements in get_video_placements(pptx_root).items()
    }

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
            rp.text_file_to_string(rel_xml),
            rp.text_file_to_string(slide_xml),
        )
        thumbnail_mappings.update(slide_thumbnail_mapping)
    return rp.gather_vars('thumbnail_mappings slide_xmls rel_xmls')

def process_powerpoint_file(pptx_path):
    folder_name = rp.strip_file_extension(pptx_path) + "_extracted"
    folder_name = rp.get_unique_copy_path(folder_name)
    folder_path = rp.with_folder_name(pptx_path,folder_name)
    rp.unzip_to_folder(pptx_path, folder_path, treat_as="zip")
    assert rp.folder_exists(folder_path)
    try:
        thumbnail_mappings, slide_xmls, rel_xmls = rp.destructure(get_thumbnail_mappings(pptx_root=folder_path))

        with rp.SetCurrentDirectoryTemporarily(rp.path_join(folder_path,'ppt','media')):        
            replacements={}
            for mp4,thumbnail in thumbnail_mappings.items():
                rp.fansi_print(mp4+'  –––––  '+thumbnail,'green')
                gif_path = rp.convert_to_gif_via_ffmpeg(
                    mp4, rp.with_file_extension(thumbnail, "gif", replace=True)
                )
                replacements[thumbnail]=gif_path
                
        print(replacements)

        for file in slide_xmls+rel_xmls:    
            file_text=rp.text_file_to_string(file)
            for before,after in replacements.items():
                file_text=file_text.replace(before,after)
            rp.string_to_text_file(file,file_text)
                
        new_pptx_path=rp.make_zip_file_from_folder(folder_path)
        new_pptx_path=rp.rename_file(new_pptx_path,rp.with_file_extension(new_pptx_path,'pptx',replace=True))

        print()
        print()
        rp.fansi_print("CONVERSION NEARLY COMPLETE!",'yellow','bold')
        rp.fansi_print("Please re-save this using powerpoint, which fixes corruption errors caused by this process",'yellow','bold')
        rp.fansi_print("The file you save in powerpoint can be directly uploaded into Google Slides, with working animations!",'yellow','bold')
        if rp.input_yes_no('Would you like to open it now?'):
            rp.open_file_with_default_application(new_pptx_path)
        

        return new_pptx_path
    
    
    finally:
        rp.delete_directory(folder_path)

#EXAMPLE:
#process_powerpoint_file('/Users/ryan/Desktop/Eyeline_April2_2024.pptx')
