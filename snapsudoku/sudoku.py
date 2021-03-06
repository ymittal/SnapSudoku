#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import sys

import cv2
import numpy as np

from scripts.sudokuExtractor import Extractor
from scripts.train import NeuralNetwork
from scripts.sudoku_str import SudokuStr


def create_net(rel_path):
    print (os.getcwd())
    with open(os.getcwd() + rel_path) as in_file:
        sizes, biases, wts = pickle.load(in_file)
    return NeuralNetwork(customValues=(sizes, biases, wts))


def get_cells(color_img):
    net = create_net(rel_path='\\snapsudoku\\networks\\net')
    for row in Extractor(color_img).cells:
        for cell in row:
            x = net.feedforward(np.reshape(cell, (784, 1)))
            x[0] = 0
            digit = np.argmax(x)
            yield str(digit) if list(x[digit])[0] / sum(x) > 0.8 else '.'


def load_image(image_path):
    color_img = cv2.imread(os.path.abspath(image_path))
    if color_img is None:
        raise IOError('Image not loaded')
    print ('Image loaded.')
    return color_img


def getError(error):
    return {
        "message": error
    }


def jsonifyResponse(success, solution, error):
    return {
        "success": success,
        "data": {
            "solution": solution
        },
        "error": getError(error) if error else error
    }
    return str


def convert2arr(str):
    arr = list(str)
    res = []
    for i in range(9):
        res.append(arr[9 * i: 9 * i + 9])
    return res


def snap_sudoku(color_img):
    try:
        grid = ''.join(cell for cell in get_cells(color_img))
    except Exception as e:
        print e
        return jsonifyResponse(success=False,
                               solution=None,
                               error="Could not generate a sudoku grid. Please rescan an appropriate picture.")

    s = SudokuStr(grid)
    try:
        s.solve()
        print('\nSolving...\n\n{}'.format(s))
        arr = convert2arr(s.s)
        return jsonifyResponse(success=True,
                               solution=arr,
                               error=None)
    except ValueError as e:
        print e
        return jsonifyResponse(success=False,
                               solution=None,
                               error="No solution could be found for the scanned picture. Try rescanning?")

if __name__ == '__main__':
    try:
        color_img = load_image(image_path=sys.argv[1])
        snap_sudoku(color_img=color_img)
    except IndexError:
        fmt = 'usage: {} image_path'
        print(fmt.format(__file__.split('/')[-1]))
