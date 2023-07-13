import nibabel as nib


def canonical_img(img):
    """Return image in canonical orientation"""
    return nib.as_closest_canonical(img)

def get_data(infile):
    """Load image and return data matrix"""
    img = nib.load(infile)
    img = canonical_img(img)
    img_data = img.get_fdata()
    return img_data
