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

class TestTree(unittest.TestCase):

    def setUp(self):
        pass


    def test_init(self):

        root = tree.TreeNode()
        self.assertEqual(root.parent, None)
        self.assertEqual(root.children, [])
        self.assertEqual(root.state, None)

        root = tree.TreeNode("test")
        self.assertEqual(root.parent, None)
        self.assertEqual(root.children, [])
        self.assertEqual(root.state, "test")


    def test_add_child(self):

        root = tree.TreeNode()
        root.create_child()
        self.assertEqual(len(root.children), 1)


    def test_num_children(self):

        root = tree.TreeNode()
        num_children = root.get_num_children()
        self.assertEqual(num_children, 0)

        root.create_child()
        num_children = root.get_num_children()
        self.assertEqual(num_children, 1)

        root.create_child()
        num_children = root.get_num_children()
        self.assertEqual(num_children, 2)


    def test_build_tree_from_string(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode.build_tree_from_string(tree_string)
        num_children = root.get_num_children()
        self.assertEqual(num_children, 2)

        tree_string = "3 -1 -1"
        self.assertRaises(AssertionError,
                tree.TreeNode.build_tree_from_string, tree_string)

        tree_string = "-1"
        self.assertRaises(AssertionError,
                tree.TreeNode.build_tree_from_string, tree_string)

        tree_string = "cow"
        self.assertRaises(ValueError,
                tree.TreeNode.build_tree_from_string, tree_string)


    def test_get_children(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode.build_tree_from_string(tree_string)

        children = root.get_children()
        self.assertEqual(len(children), 2)
        child = children[0]
        self.assertTrue(child.state == 4 or child.state == 5)

        # Find the child with ID 4
        children = root.get_children()
        if children[0].state == 4:
            child = children[0]
        else:
            child = children[1]
        next_children = child.get_children()
        self.assertEqual(len(next_children), 2)


    def test_get_depth(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode.build_tree_from_string(tree_string)
        self.assertEqual(root.get_depth(), 0)

        # Find the child with ID 4
        children = root.get_children()
        if children[0].state == 4:
            depth_1 = children[0]
        else:
            depth_1 = children[1]
        self.assertEqual(depth_1.get_depth(), 1)

        depth_2 = depth_1.get_children()[0]
        self.assertEqual(depth_2.get_depth(), 2)


    def test_get_root(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode.build_tree_from_string(tree_string)
        self.assertEqual(root.get_depth(), 0)

        # Find the child with ID 4
        children = root.get_children()
        if children[0].state == 4:
            depth_1 = children[0]
        else:
            depth_1 = children[1]

        depth_2 = depth_1.get_children()[0]
        self.assertEqual(depth_2.get_root(), root)


    def test_print(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        printed_tree = "3\n4\n2\n4 -> 2\n1\n4 -> 1\n3 -> 4\n5\n3 -> 5\n"

        root = tree.TreeNode.build_tree_from_string(tree_string)
        self.assertEqual(str(root), printed_tree)



if __name__ == '__main__':
    unittest.main()
