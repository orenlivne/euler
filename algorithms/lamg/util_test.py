import unittest, util, numpy as np, numpy.testing as nt

def test_caliber_one_interpolation():
  P = util.caliber_one_interpolation(np.array([0,0,1,1,2,2,3,3,4,4]))

  P_expected = np.matrix(
      [[ 1.,  0., 0.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.],
       [ 0.,  1.,  0.,  0.,  0.],
       [ 0.,  1.,  0.,  0.,  0.],
       [ 0.,  0.,  1.,  0.,  0.],
       [ 0.,  0.,  1.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.],
       [ 0.,  0.,  0.,  1.,  0.],
       [ 0.,  0.,  0.,  0.,  1.],
       [ 0.,  0.,  0.,  0.,  1.]])

  nt.assert_array_equal(P.todense(), P_expected)

def test_caliber_one_interpolation_weighted():
  P = util.caliber_one_interpolation_weighted(
      np.array([0,0,1,1,2,2,3,3,4,4]), np.arange(1,11))

  P_expected = np.matrix(
      [[ 1.,  0., 0.,  0.,  0.],
       [ 2.,  0.,  0.,  0.,  0.],
       [ 0.,  3.,  0.,  0.,  0.],
       [ 0.,  4.,  0.,  0.,  0.],
       [ 0.,  0.,  5.,  0.,  0.],
       [ 0.,  0.,  6.,  0.,  0.],
       [ 0.,  0.,  0.,  7.,  0.],
       [ 0.,  0.,  0.,  8.,  0.],
       [ 0.,  0.,  0.,  0.,  9.],
       [ 0.,  0.,  0.,  0.,  10.]])

  nt.assert_array_equal(P.todense(), P_expected)
