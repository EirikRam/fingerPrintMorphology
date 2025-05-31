import cv2
import numpy as np
import matplotlib.pyplot as plt

# list of the images we wanna process
image_files = ['fingerprint-glass.jpg', 'fingerprint-glasscup.jpg', 'fingerprint-sunglasses.jpg']

# loop over each image file
for image_name in image_files:
    # load the fingerprint in grayscale
    img = cv2.imread(image_name, 0)

    # try to improve contrast a bit so features pop more
    equalized_img = cv2.equalizeHist(img)

    # turn image into binary (black and white) using a fixed threshold
    _, binary_img = cv2.threshold(equalized_img, 127, 255, cv2.THRESH_BINARY)

    # kernel for morph operations, small 3x3 square
    kernel = np.ones((3, 3), np.uint8)

    # do dilation - grows the white areas a bit
    dilated_img = cv2.dilate(binary_img, kernel, iterations=1)

    # do erosion - shrinks the white areas a bit
    eroded_img = cv2.erode(binary_img, kernel, iterations=1)

    # opening = erosion followed by dilation, good for removing small noise
    opening_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

    # closing = dilation followed by erosion, fills small holes
    closing_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    # show all the results together for comparison
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))

    axs[0, 0].imshow(binary_img, cmap='gray')
    axs[0, 0].set_title('Binary Image')

    axs[0, 1].imshow(dilated_img, cmap='gray')
    axs[0, 1].set_title('Dilated Image')

    axs[0, 2].imshow(eroded_img, cmap='gray')
    axs[0, 2].set_title('Eroded Image')

    axs[1, 0].imshow(opening_img, cmap='gray')
    axs[1, 0].set_title('Opening Image')

    axs[1, 1].imshow(closing_img, cmap='gray')
    axs[1, 1].set_title('Closing Image')

    axs[1, 2].imshow(equalized_img, cmap='gray')
    axs[1, 2].set_title('Equalized Image')

    for ax in axs.flat:
        ax.axis('off')  # no axis lines

    # save the figure with modified image name
    output_image_name = image_name.split('.')[0] + '_morphology.png'
    plt.savefig(output_image_name)

    plt.close(fig)  # close the plot to not clutter memory

    print(f"Processed and saved {output_image_name}")
