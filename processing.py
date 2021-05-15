import numpy as np
import cv2

# generate componentss from image
def get_components(labels, pad_width=3, erosion_percent=0.4, show=True):
    components = {}
    # total no of components or characters from the image
    total_components = len(np.unique(labels))
    # defining each component
    for i in range(1, total_components):
        components[i] = {'label': None,
                      'output': None,
                      'tl': None,
                      'br': None,
                      'pic': None,
                      'group': None,
                      'sup': False,
                      'sub': False,
                      'num': False,
                      'deno': False,
                      'frac': False}
                  
    for i in sorted(components.keys()):
        # extract a particular component from the image
        label = labels.copy()
        arr_new = np.hstack([np.zeros([label.shape[0], pad_width]), label])
        arr_new = np.hstack([arr_new, np.zeros([arr_new.shape[0], pad_width])])
        arr_new = np.vstack([np.zeros([pad_width, arr_new.shape[1]]), arr_new])
        arr_new = np.vstack([arr_new, np.zeros([pad_width, arr_new.shape[1]])])
        label_padded = arr_new
        xs, ys = np.where(label == i)
        top, bottom, left, right = np.min(xs), np.max(xs), np.min(ys), np.max(ys)
        components[i]['br'] = (bottom, right)
        components[i]['tl'] = (top, left)
        label_padded[label_padded != i] = 0
        label_padded = label_padded//i
        # resize the extrated component to 45*45
        arr_square = label_padded[top :bottom + pad_width + pad_width, left :right + pad_width + pad_width]
        x = arr_square.shape[1]
        y = arr_square.shape[0]
        diff = abs(x - y)
        pad = diff // 2
        if y < x:
            arr_square = np.vstack([np.zeros([pad, x]), arr_square])
            arr_square = np.vstack([arr_square, np.zeros([pad + (diff % 2 == 1), x])])
        elif y >= x:
            arr_square = np.hstack([np.zeros([y, pad]), arr_square])
            arr_square = np.hstack([arr_square, np.zeros([y, pad + (diff % 2 == 1)])])
        label_square = arr_square
        dimension = 45
        label_square = cv2.resize(label_square, (dimension, dimension))
        label_square[label_square != 0] = 1
        skip = 1
        for dim in range(1, 12, skip):
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dim, dim))
            erosion = cv2.erode(label_square, kernel, iterations = 1)
            if np.sum(erosion) / np.sum(label_square) < erosion_percent:
                break
        dim = dim - 1
        # process the image
        kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (dim, dim))
        label_eroded = cv2.erode(label_square, kernel, iterations = 1)
        # saving the image to component
        components[i]['pic'] = label_eroded.ravel()
    return components

