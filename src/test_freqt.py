#!/usr/bin/env python

# Copyright (c) 2009, Regents of the University of California
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#
#     * Neither the name of the University of California, Los Angeles
#     nor the names of its contributors may be used to endorse or
#     promote products derived from this software without specific prior
#     written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Author: Roy Shea
# Date: June 2009

import unittest
import tree
import freqt

class TestFreqt(unittest.TestCase):

    def setUp(self):
        tree_string = "1 1 -1 2 -1 1 -1 2 -1 -1 1 1 -1 1 -1 2"
        self.root = tree.OrderedTreeNode("root")
        self.root.build_tree_from_string(tree_string)

    def test_get_c1(self):
        c1 = freqt.get_c1(self.root, 0.05)
        self.assertTrue(1 in c1.keys())
        self.assertTrue(2 in c1.keys())
        self.assertTrue("root" in c1.keys())
        self.assertEqual(len(c1), 3)

        c1 = freqt.get_c1(self.root, 0.15)
        self.assertTrue(1 in c1.keys())
        self.assertTrue(2 in c1.keys())
        self.assertEqual(len(c1), 2)

        c1 = freqt.get_c1(self.root, 0.8)
        self.assertEqual(len(c1), 0)


    def test_pl_expond(self):

        tree0 = freqt.pl_expand(self.root, 0, 3)
        self.assertEqual(tree0.get_num_nodes(), 11)
        self.assertEqual(tree0.get_nodes()[10].state, 3)
        self.assertEqual(tree0.get_nodes()[10].get_parent().state, 2)

        tree1 = freqt.pl_expand(self.root, 1, 3)
        self.assertEqual(tree1.get_num_nodes(), 11)
        self.assertEqual(tree1.get_nodes()[10].state, 3)
        self.assertEqual(tree1.get_nodes()[10].get_parent().state, 1)

        tree2 = freqt.pl_expand(self.root, 2, 3)
        self.assertEqual(tree2.get_num_nodes(), 11)
        self.assertEqual(tree2.get_nodes()[10].state, 3)
        self.assertEqual(tree2.get_nodes()[10].get_parent().state, "root")


if __name__ == '__main__':
    unittest.main()

