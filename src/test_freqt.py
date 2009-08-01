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

        # Tree used throughout the tests
        tree_string = "1 1 -1 2 -1 1 -1 2 -1 -1 1 1 -1 1 -1 2 -1 -1"
        self.root = tree.OrderedTreeNode("root")
        self.root.build_tree_from_string(tree_string)
        self.root.lock_tree()

        # Build strings for subtrees
        self.subtree_1_str = "1 -1"
        self.subtree_2_str = "2 -1"
        self.subtree_r_str = "root -1"


    def test_get_c1(self):

        c1 = freqt.get_c1(self.root, 0.05)
        self.assertEqual(len(c1), 3)

        self.assertTrue(self.subtree_1_str in c1.keys())
        self.assertEqual(len(c1[self.subtree_1_str]), 6)

        self.assertTrue(self.subtree_2_str in c1.keys())
        self.assertEqual(len(c1[self.subtree_2_str]), 3)

        self.assertTrue(self.subtree_r_str in c1.keys())
        self.assertEqual(len(c1[self.subtree_r_str]), 1)

        c1 = freqt.get_c1(self.root, 0.15)
        self.assertEqual(len(c1), 2)

        self.assertTrue(self.subtree_1_str in c1.keys())
        self.assertTrue(self.subtree_2_str in c1.keys())

        c1 = freqt.get_c1(self.root, 0.8)
        self.assertEqual(len(c1), 0)


    def test_pl_expand(self):

        tree0 = freqt.pl_expand(self.root, 0, 3)
        tree0.lock_tree()
        self.assertEqual(tree0.get_num_nodes(), 11)
        self.assertEqual(tree0.get_nodes()[10].state, '3')
        self.assertEqual(tree0.get_nodes()[10].get_parent().state, '2')

        tree1 = freqt.pl_expand(self.root, 1, 3)
        tree1.lock_tree()
        self.assertEqual(tree1.get_num_nodes(), 11)
        self.assertEqual(tree1.get_nodes()[10].state, '3')
        self.assertEqual(tree1.get_nodes()[10].get_parent().state, '1')

        tree2 = freqt.pl_expand(self.root, 2, 3)
        tree2.lock_tree()
        self.assertEqual(tree2.get_num_nodes(), 11)
        self.assertEqual(tree2.get_nodes()[10].state, '3')
        self.assertEqual(tree2.get_nodes()[10].get_parent().state, "root")


    def test_update_rmo(self):

        # c1 = {1:[1, 2, 4, 6, 7, 8], 2:[3, 5, 9]}
        c1 = freqt.get_c1(self.root, 0.15)

        # Test all possible extensions off of c1.
        rmo_1 = c1[self.subtree_1_str]
        rmo_2 = c1[self.subtree_2_str]

        rmo_11 = freqt.update_rmo(self.root, rmo_1, 0, '1')
        self.assertEqual(len(rmo_11), 4)

        rmo_12 = freqt.update_rmo(self.root, rmo_1, 0, '2')
        self.assertEqual(len(rmo_12), 3)

        rmo_13 = freqt.update_rmo(self.root, rmo_1, 0, '3')
        self.assertEqual(len(rmo_13), 0)

        rmo_21 = freqt.update_rmo(self.root, rmo_2, 0, '1')
        self.assertEqual(len(rmo_21), 0)

        rmo_22 = freqt.update_rmo(self.root, rmo_2, 0, '2')
        self.assertEqual(len(rmo_22), 0)

        rmo_23 = freqt.update_rmo(self.root, rmo_2, 0, '3')
        self.assertEqual(len(rmo_23), 0)

        rmo_11 = freqt.update_rmo(self.root, rmo_1, 0, '1')
        self.assertEqual(len(rmo_11), 4)

        # Test extensions off of rmo_11.  There should be no p=0
        # extensions, but a few from p=1.

        rmo_111_p0 = freqt.update_rmo(self.root, rmo_11, 0, '1')
        self.assertEqual(len(rmo_111_p0), 0)

        rmo_111_p1 = freqt.update_rmo(self.root, rmo_11, 1, '1')
        self.assertEqual(len(rmo_111_p1), 2)

        rmo_112_p0 = freqt.update_rmo(self.root, rmo_11, 0, '2')
        self.assertEqual(len(rmo_112_p0), 0)

        rmo_112_p1 = freqt.update_rmo(self.root, rmo_11, 1, '2')
        self.assertEqual(len(rmo_112_p1), 3)


    def test_expand_trees(self):

        # c1 = {1:[1, 2, 4, 6, 7, 8], 2:[3, 5, 9]}
        c1 = freqt.get_c1(self.root, 0.15)

        c2 = freqt.expand_trees(self.root, c1, 0.15, ['1', '2', 'root'])
        self.assertEqual(len(c2), 2)

        c3 = freqt.expand_trees(self.root, c2, 0.15, ['1', '2', 'root'])
        self.assertEqual(len(c3), 2)

        c3 = freqt.expand_trees(self.root, c2, 0.2, ['1', '2', 'root'])
        self.assertEqual(len(c3), 1)


    def test_freqt(self):

        frequent_subtrees = freqt.freqt(self.root, 0.2)
        self.assertEqual(len(frequent_subtrees), 4)

        frequent_subtrees = freqt.freqt(self.root, 0.15)
        self.assertEqual(len(frequent_subtrees), 5)

if __name__ == '__main__':
    unittest.main()
