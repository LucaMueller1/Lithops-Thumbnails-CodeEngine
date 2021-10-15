import os
from PIL import Image
import io
import time
from lithops import Storage
from lithops.multiprocessing import Pool
# from multiprocessing import Pool


def create_thumbnail(tuple_file):
    tuple_file = list(tuple_file)
    size = tuple_file[0]
    file = tuple_file[1]
    key = tuple_file[2]
    print(size, key)

    outfile = key.split("/")[-1] + ".thumbnail" + str(size)
    try:
        with Image.open(io.BytesIO(file)) as im:
            im.thumbnail((size, size))

            img_byte_arr = io.BytesIO()
            im.save(img_byte_arr, "JPEG")
            return_tuple = (outfile, img_byte_arr)
            return return_tuple
    except OSError:
        print("cannot create thumbnail for", key)


'''
def create_thumbnails(files):
    sizes = [(64, 64), (128, 128), (256, 256), (512, 512)]
    output = []
    files = list(files)

    for size in sizes:
        for file, key in files:
            print(key)
            outfile = key.split("/")[-1] + ".thumbnail" + str(size[0])
            try:
                with Image.open(io.BytesIO(file)) as im:
                    im.thumbnail(size)

                    img_byte_arr = io.BytesIO()
                    im.save(img_byte_arr, "JPEG")
                    output.append((outfile, img_byte_arr))
            except OSError:
                print("cannot create thumbnail for", key)
    return output
'''

if __name__ == '__main__':
    storage = Storage()

    cos_keys = storage.list_keys(bucket='cos-lithops-thesis-bucket', prefix='images/')
    input_files = []

    print("Retrieving images from bucket")
    for cos_key in cos_keys:
        cos_file = storage.get_object(bucket='cos-lithops-thesis-bucket', key=cos_key)
        input_files.append(cos_file)

    print("Creating thumbnails...")
    start_time = time.time()

    # directory = "/Users/lucamueller/Desktop/unsamples"
    # files = os.listdir(directory)

    sizes = [128]

    in_tuple = []
    for sz in sizes:
        in_tuple = in_tuple + list(zip(([sz] * len(input_files)), input_files, cos_keys))

    with Pool() as pool:
        output_files = pool.map(create_thumbnail, in_tuple)
        print(output_files)

    print("Time needed: " + str(time.time() - start_time))

    print("Saving thumbnails to bucket")
    for image in output_files:
        save_key = "thumbnails/" + image[0] + ".jpg"
        # storage.put_object(bucket='cos-lithops-thesis-bucket', key=save_key, body=image[1].getvalue())

    print("Finished")
