import base64

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Example usage
image_path_1 = 'src/images/central-point.png'
image_path_2 = 'src/images/zpt.png'

encoded_image = encode_image_to_base64(image_path_1)
print(encoded_image)
encoded_image = encode_image_to_base64(image_path_2)
print(encoded_image)
