import requests
from hashlib import md5
from PIL import Image
from io import BytesIO

def restore_sliced_captcha_image(image_path):
    if image_path[:4]=="http":
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
        response = requests.get(image_path, headers=headers)
        assert response.status_code==200, f"Failed to open captcha image, error cod: {response.status_code}"
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(image_path)
    width, height = img.size
    positions = [[-157, 0], [-145, 0], [-265, 0], [-277, 0], [-181, 0], [-169, 0], [-241, 0],
                [-253, 0], [-109, 0], [-97, 0],  [-289, 0], [-301, 0], [-85, 0],  [-73, 0], 
                [-25, 0],  [-37, 0],  [-13, 0],  [-1, 0],   [-121, 0], [-133, 0], [-61, 0], 
                [-49, 0],  [-217, 0], [-229, 0], [-205, 0], [-193, 0], 
                [-145, -80], [-157, -80], [-277, -80], [-265, -80], [-169, -80], [-181, -80], 
                [-253, -80], [-241, -80], [-97, -80],  [-109, -80], [-301, -80], [-289, -80], 
                [-73, -80],  [-85, -80],  [-37, -80],  [-25, -80],  [-1, -80],   [-13, -80], 
                [-133, -80], [-121, -80], [-49, -80],  [-61, -80],  [-229, -80], [-217, -80], 
                [-193, -80], [-205, -80]]
    slice_width, slice_height = 12, 80
    count = x2 = y2 = 0
    half_len = int(len(positions)/2)
    captcha = Image.new('RGB', (int((slice_width - 2) * (width / slice_width)), height))
    for x, y in positions:
        slice_box = (abs(x)-1, abs(y), abs(x)-1+slice_width, slice_height+abs(y))
        slice_region = img.crop(slice_box)
        captcha.paste(slice_region, (x2, y2))
        # x2要递增10，而不是12，是因为原图片每个切块宽度有多余的2像素
        x2 += 10
        count +=1
        if count==half_len:
            x2 = 0
            y2 = slice_height
    return captcha



if __name__ == "__main__":
    captcha_images = ['./captcha_image_1.png',
                      './captcha_image_2.png']
    for i in captcha_images:
        new_capthca_image = restore_sliced_captcha_image(i)
        with BytesIO() as output:
            new_capthca_image.save(output, format='PNG')
            image_bytes = output.getvalue()
        new_capthca_image.show()