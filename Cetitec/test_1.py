import unittest
import subprocess
import os
import filecmp

class Test_test_1(unittest.TestCase):
    def test_hex_not(self):
        self.proces_file(4)

    def test_input_value_range(self):
        self.proces_file(5)
        #edge cases testing
        self.proces_file(11)

    def test_input_truncation(self):
        self.proces_file(6)

    def test_factor_range(self):
        self.proces_file(7)
        #edge cases testing
        self.proces_file(12)
        self.proces_file(13)

    def test_missing_input_file(self):
        self.call_app("TestInput99.txt", "TestOutput99.txt", True)
        self.assertFalse(os.path.exists("TestOutput99.txt"))

    def test_output_overwrite(self):
        with open("TestOutput10.txt", "w") as f:
            print("jkll", file=f)
        self.proces_file(10, False)

    def test_output_value(self):
        self.proces_file(14)

    def proces_file(self, num, del_output = True):
        in_file = "TestInput{:0>2d}.txt".format(num)
        out_file = "TestOutput{:0>2d}.txt".format(num)
        chk_file = "TestCheck{:0>2d}.txt".format(num)
        self.call_app(in_file, out_file, del_output)
        self.assertTrue(filecmp.cmp(out_file, chk_file))

    def call_app(self, in_file, out_file, del_output):
        if del_output and os.path.exists(out_file): os.remove(out_file)
        subprocess.call("python TesterApp.py {}".format(in_file), shell=True)
    
if __name__ == '__main__':
    unittest.main()
