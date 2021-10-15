from PIL import Image
from PIL import ImageEnhance
import io
import time
from lithops import Storage
from lithops.multiprocessing import Pool


def create_thumbnail(cos_key, sizes):
    storage = Storage()
    cos_file = storage.get_object(bucket='cos-lithops-thesis-bucket', key=cos_key)
    print("Fetching file: ", cos_key)
    output_list = []

    for size in sizes:

        outfile = cos_key.split("/")[-1] + ".thumbnail" + str(size)
        try:
            im = Image.open(io.BytesIO(cos_file))
            im.thumbnail(size)
            #enh = ImageEnhance.Contrast(im)
            #im = enh.enhance(1.3)


            img_byte_arr = io.BytesIO()
            im.save(img_byte_arr, "JPEG")
            return_tuple = (outfile, img_byte_arr)
            output_list.append(return_tuple)
        except OSError:
            print("cannot create thumbnail for", cos_key)
    return output_list


if __name__ == '__main__':
    storage = Storage()

    cos_keys = storage.list_keys(bucket='cos-lithops-thesis-bucket', prefix='images/')
    image_count = int(input("Number of images to be processed (max: " + str(len(cos_keys)) + "): "))
    if image_count < len(cos_keys):
        cos_keys = cos_keys[:image_count]

    input_files = []

    print("Creating %s thumbnails..." % image_count)
    start_time = time.time()

    sizes = [[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512)]]

    minTimestamp = 0
    maxTimestamp = 0
    minTimestamp2 = 0
    maxTimestamp2 = 0

    with Pool() as pool:
        output_files = pool.starmap(create_thumbnail, zip(cos_keys, sizes*len(cos_keys)))
        print("Job finished. Generating charts...")
        for fut in pool._executor.futures:
            # print(fut.stats)
            if fut.stats['worker_func_start_tstamp'] < minTimestamp or minTimestamp == 0:
                minTimestamp = fut.stats['worker_func_start_tstamp']
            if fut.stats['worker_func_end_tstamp'] > maxTimestamp:
                maxTimestamp = fut.stats['worker_func_end_tstamp']

            if fut.stats['worker_start_tstamp'] < minTimestamp2 or minTimestamp2 == 0:
                minTimestamp2 = fut.stats['worker_start_tstamp']
            if fut.stats['worker_end_tstamp'] > maxTimestamp2:
                maxTimestamp2 = fut.stats['worker_end_tstamp']
        dst = "./stats/lithops_" + str(time.time()) + "_" + str(round((maxTimestamp2 - minTimestamp2), 2)) + "_" + str(image_count)
        pool._executor.plot(dst=dst)

    print("Time (func exec): ", maxTimestamp-minTimestamp)
    print("Time (worker exec): ", maxTimestamp2 - minTimestamp2)

    #print("Time needed (Lithops serverless Multiprocessing): " + str(time.time() - start_time))

'''
    print("Saving thumbnails to bucket")
    for images in output_files:
        for image in images:
            save_key = "thumbnails/" + str(image[0]) + ".jpg"
            storage.put_object(bucket='cos-lithops-thesis-bucket', key=save_key, body=image[1].getvalue())

    print("Finished")
'''
