import unittest

from ray.data import read_binary_files
from dataset import split_text


class DataSetTest(unittest.TestCase):
    def test_load_data(self):
        ds = read_binary_files("../contents/posts")
        ds.flat_map(split_text)
        for i in ds.iter_rows():
            print(i)
        self.assertEqual(3, 4)


if __name__ == "__main__":
    unittest.main()
