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
        root.append_child()
        self.assertEqual(len(root.children), 1)


    def test_num_children(self):

        root = tree.TreeNode()
        num_children = root.get_num_children()
        self.assertEqual(num_children, 0)

        root.append_child()
        num_children = root.get_num_children()
        self.assertEqual(num_children, 1)

        root.append_child()
        num_children = root.get_num_children()
        self.assertEqual(num_children, 2)


    def test_build_tree_from_string(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode("root")
        root.build_tree_from_string(tree_string)
        num_children = root.get_num_children()
        self.assertEqual(num_children, 1)
        num_children = root.get_children()[0].get_num_children()
        self.assertEqual(num_children, 2)

        tree_string = "3 -1 -1"
        root = tree.TreeNode("root")
        self.assertRaises(AssertionError, root.build_tree_from_string,
                tree_string)

        tree_string = "-1"
        root = tree.TreeNode("root")
        self.assertRaises(AssertionError, root.build_tree_from_string,
                tree_string)

        tree_string = "cow"
        root = tree.TreeNode("root")
        self.assertRaises(ValueError, root.build_tree_from_string,
                tree_string)


    def test_get_children(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode("root")
        root.build_tree_from_string(tree_string)

        # Root should have 3 as a child
        children = root.get_children()
        self.assertEqual(len(children), 1)
        child = children[0]
        self.assertEqual(child.state, 3)

        # Node with state 3 should have two children with states 4 and 5
        children = child.get_children()
        self.assertEqual(len(children), 2)
        child = children[0]
        self.assertTrue(child.state == 4 or child.state == 5)
        child = children[1]
        self.assertTrue(child.state == 4 or child.state == 5)

        # Find the child with ID 4
        children = root.get_children()[0].get_children()
        if children[0].state == 4:
            child = children[0]
        else:
            child = children[1]
        next_children = child.get_children()
        self.assertEqual(len(next_children), 2)


    def test_get_depth(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode("root")
        root.build_tree_from_string(tree_string)
        self.assertEqual(root.get_depth(), 0)

        # Find the child with ID 4
        children = root.get_children()[0].get_children()
        if children[0].state == 4:
            depth_2 = children[0]
        else:
            depth_2 = children[1]
        self.assertEqual(depth_2.get_depth(), 2)

        depth_3 = depth_2.get_children()[0]
        self.assertEqual(depth_3.get_depth(), 3)


    def test_get_root(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        root = tree.TreeNode("root")
        root.build_tree_from_string(tree_string)

        # Find the child with ID 4
        children = root.get_children()[0].get_children()
        if children[0].state == 4:
            depth_2 = children[0]
        else:
            depth_2 = children[1]

        depth_3 = depth_2.get_children()[0]
        self.assertEqual(depth_3.get_root(), root)


    def test_print(self):

        tree_string = "3 4 2 -1 1 -1 -1 5"
        printed_tree = "root\n3\n4\n2\n4 -> 2\n1\n4 -> 1\n3 -> 4\n5\n3 -> 5\nroot -> 3\n"

        root = tree.TreeNode("root")
        root.build_tree_from_string(tree_string)
        self.assertEqual(str(root), printed_tree)


class OrderedTestTree(unittest.TestCase):

    def setUp(self):
        tree_string = "3 4 2 -1 1 -1 -1 5"
        self.root = tree.OrderedTreeNode("root")
        self.root.build_tree_from_string(tree_string)


    def test_init(self):

        # Verify root
        self.assertEqual(self.root.state, "root")
        self.assertEqual(len(self.root.children), 1)

        # Verify node with state 3
        node3 = self.root.get_children()[0]
        self.assertEqual(node3.state, 3)
        self.assertEqual(len(node3.children), 2)

        # Verify node with state 4
        node4 = node3.get_children()[0]
        self.assertEqual(node4.state, 4)
        self.assertEqual(len(node4.children), 2)
        self.assertEqual(node4.get_children()[0].state, 2)
        self.assertEqual(node4.get_children()[1].state, 1)


if __name__ == '__main__':
    unittest.main()
