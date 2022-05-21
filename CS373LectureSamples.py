from matplotlib import pyplot

# import our basic, light-weight png reader library
import imageIO.png

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b


def readRGBImageToSeparatePixelArrays(input_filename):
    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows,
     rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value
def createInitializedGreyscalePixelArray(image_width, image_height, initValue=0):

    new_array = [[initValue for x in range(
        image_width)] for y in range(image_height)]
    return new_array


def computeHistogram(pixel_array, image_width, image_height, nr_bins):

    histogram = [0.0 for i in range(nr_bins)]

    # your task to compute the correct histogram!
    step_size = 256 / nr_bins
    for r in range(image_height):
        for c in range(image_width):
            histogram[int(pixel_array[r][c] / step_size)] += 1.0

    return histogram


def computeMean3x3(pixel_array, image_width, image_height):
    mean_array = createInitializedGreyscalePixelArray(image_width, image_height)

    for y in range(1, image_height-1):
        for x in range(1, image_width-1):
            output_pixel = 0.0
            for eta in [-1, 0, 1]:
                for xi in [-1, 0, 1]:
                    output_pixel += pixel_array[y + eta][x + xi]
            output_pixel /= 9.0

            mean_array[y][x] = int(output_pixel)

    return mean_array


def main():
    filename = "krakow.png"

    (image_width, image_height, px_array_r, px_array_g,
     px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    pixel_array = px_array_r

    filtered_image = computeMean3x3(pixel_array, image_width, image_height)

    fig1, axs1 = pyplot.subplots(2, 1)
    axs1[0].set_title('Input image')
    axs1[0].imshow(pixel_array, cmap='gray')

    nr_bins = 64
    # dummy_histogram = computeHistogram(pixel_array, image_width, image_height, nr_bins)

    axs1[1].set_title('Mean')
    axs1[1].imshow(filtered_image, cmap='gray')

    # axs1[1].set_title('Histogram')
    # axs1[1].bar(range(nr_bins), dummy_histogram)

    pyplot.show()


if __name__ == "__main__":
    main()
