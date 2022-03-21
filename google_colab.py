def mp4_to_html(path):
    #Currently realllly ugly, hence the name...
    # EXAMPLE:
    #     from IPython.display import HTML
    #     HTML(mp4_html('video.mp4'))
    from base64 import b64encode
    mp4 = open(path,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    return("""
    <video width=800 controls>
        <source src="%s" type="video/mp4">
    </video>
    """ % data_url)