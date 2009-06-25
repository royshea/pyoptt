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
        tree_string = "3 4 2 -1 1 -1 -1 5 -1 -1"
        self.root = tree.OrderedTreeNode("root")
        self.root.build_tree_from_string(tree_string)

        # Find the child with ID 3
        self.node3 = self.root.get_children()[0]

        # Find the child with ID 4
        children = self.node3.get_children()
        if children[0].state == '4':
            self.node4 = children[0]
        else:
            self.node4 = children[1]

        # Find the child with ID 5
        children = self.node3.get_children()
        if children[0].state == '5':
            self.node5 = children[0]
        else:
            self.node5 = children[1]


    def test_init(self):

        local_root = tree.TreeNode()
        self.assertEqual(local_root.parent, None)
        self.assertEqual(local_root.children, [])
        self.assertEqual(local_root.state, None)

        local_root = tree.TreeNode("test")
        self.assertEqual(local_root.parent, None)
        self.assertEqual(local_root.children, [])
        self.assertEqual(local_root.state, "test")


    def test_add_child(self):

        local_root = tree.TreeNode()
        local_root.append_child()
        self.assertEqual(len(local_root.children), 1)


    def test_num_children(self):

        local_root = tree.TreeNode()
        num_children = local_root.get_num_children()
        self.assertEqual(num_children, 0)

        local_root.append_child()
        num_children = local_root.get_num_children()
        self.assertEqual(num_children, 1)

        local_root.append_child()
        num_children = local_root.get_num_children()
        self.assertEqual(num_children, 2)


    def test_build_tree_from_string(self):

        tree_string = "3 4 2 -1 1 -1 -1 5 -1 -1"
        local_root = tree.TreeNode("local_root")
        local_root.build_tree_from_string(tree_string)
        num_children = local_root.get_num_children()
        self.assertEqual(num_children, 1)
        num_children = local_root.get_children()[0].get_num_children()
        self.assertEqual(num_children, 2)

        tree_string = "3 -1 -1"
        local_root = tree.TreeNode("local_root")
        self.assertRaises(AssertionError, local_root.build_tree_from_string,
                tree_string)

        tree_string = "-1"
        local_root = tree.TreeNode("local_root")
        self.assertRaises(AssertionError, local_root.build_tree_from_string,
                tree_string)


    def test_unrooted_build_tree_from_string(self):

        tree_string = "3 4 2 -1 1 -1 -1 5 -1 -1"
        local_root = tree.TreeNode.unrooted_build_tree_from_string(tree_string)
        num_children = local_root.get_num_children()
        self.assertEqual(num_children, 2)
        num_nodes = local_root.get_num_nodes()
        self.assertEqual(num_nodes, 5)

        tree_string = "3 -1 -1"
        self.assertRaises(AssertionError, tree.TreeNode.unrooted_build_tree_from_string,
                tree_string)


    def test_get_children(self):

        # Root should have 3 as a child
        children = self.root.get_children()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0], self.node3)

        # Node with state 3 should have two children with states 4 and 5
        children = self.node3.get_children()
        self.assertEqual(len(children), 2)
        child = children[0]
        self.assertTrue(child.state == '4' or child.state == '5')
        child = children[1]
        self.assertTrue(child.state == '4' or child.state == '5')

        # Node with state 4 should have two children with states 2 and 1
        children = self.node4.get_children()
        self.assertEqual(len(children), 2)
        child = children[0]
        self.assertTrue(child.state == '2' or child.state == '1')
        child = children[1]
        self.assertTrue(child.state == '2' or child.state == '1')


    def test_get_parent(self):

        # Root should have no parents
        self.assertEqual(self.root.get_parent(), None)

        # Node 4 should have node 3 as its parent
        self.assertEqual(self.node4.get_parent().state, '3')

        # Node 3 should have "root" as its parent
        self.assertEqual(self.node3.get_parent().state, "root")


    def test_get_pth_parent(self):

        self.assertEqual(self.root.get_pth_parent(0), self.root)
        self.assertRaises(AssertionError, self.root.get_pth_parent, 1)

        self.assertEqual(self.node3.get_pth_parent(0), self.node3)
        self.assertEqual(self.node3.get_pth_parent(1), self.root)
        self.assertRaises(AssertionError, self.node3.get_pth_parent, 2)

        self.assertEqual(self.node4.get_pth_parent(0), self.node4)
        self.assertEqual(self.node4.get_pth_parent(1), self.node3)
        self.assertEqual(self.node4.get_pth_parent(2), self.root)
        self.assertRaises(AssertionError, self.node4.get_pth_parent, 3)


    def test_get_depth(self):

        self.assertEqual(self.root.get_depth(), 0)
        self.assertEqual(self.node3.get_depth(), 1)
        self.assertEqual(self.node4.get_depth(), 2)


    def test_get_root(self):

        self.assertEqual(self.root.get_root(), self.root)
        self.assertEqual(self.node3.get_root(), self.root)
        self.assertEqual(self.node4.get_root(), self.root)


    def test_get_num_nodes(self):

        self.assertEqual(self.root.get_num_nodes(), 6)
        self.assertEqual(self.node3.get_num_nodes(), 5)
        self.assertEqual(self.node4.get_num_nodes(), 3)


    def test_get_nodes(self):

        nodes = self.root.get_nodes()
        self.assertEqual(len(nodes), 6)


class OrderedTestTree(unittest.TestCase):

    def setUp(self):

        tree_string = "3 4 2 -1 1 -1 -1 5 -1 -1"
        self.root = tree.OrderedTreeNode("root")
        self.root.build_tree_from_string(tree_string)

        # Find the child with ID 3
        self.node3 = self.root.get_children()[0]

        # Find the child with ID 4
        children = self.node3.get_children()
        if children[0].state == '4':
            self.node4 = children[0]
        else:
            self.node4 = children[1]

        # Find the child with ID 5
        children = self.node3.get_children()
        if children[0].state == '5':
            self.node5 = children[0]
        else:
            self.node5 = children[1]



    def test_init(self):

        # Verify root
        self.assertEqual(self.root.state, "root")
        self.assertEqual(len(self.root.children), 1)

        # Verify node with state 3
        node3 = self.root.get_children()[0]
        self.assertEqual(node3.state, '3')
        self.assertEqual(len(node3.children), 2)

        # Verify node with state 4
        node4 = node3.get_children()[0]
        self.assertEqual(node4.state, '4')
        self.assertEqual(len(node4.children), 2)
        self.assertEqual(node4.get_children()[0].state, '2')
        self.assertEqual(node4.get_children()[1].state, '1')


    def test_get_nodes(self):

        nodes = self.root.get_nodes()
        self.assertEqual(nodes[0].state, "root")
        self.assertEqual(nodes[1].state, '3')
        self.assertEqual(nodes[2].state, '4')
        self.assertEqual(nodes[3].state, '2')
        self.assertEqual(nodes[4].state, '1')
        self.assertEqual(nodes[5].state, '5')


    def test_get_tree_position(self):

        self.assertEqual(self.root.get_tree_position(), 0)
        self.assertEqual(self.node3.get_tree_position(), 1)
        self.assertEqual(self.node4.get_tree_position(), 2)
        self.assertEqual(self.node5.get_tree_position(), 5)


    def test_get_right_most_leaf(self):

        self.assertEqual(self.root.get_right_most_leaf().state, '5')
        self.assertEqual(self.node3.get_right_most_leaf().state, '5')
        self.assertEqual(self.node4.get_right_most_leaf().state, '1')


    def test_structural_equality(self):

        tree_string = "3 4 2 -1 1 -1 -1 5 -1 -1"

        r1 = tree.OrderedTreeNode("root")
        r2 = tree.OrderedTreeNode("root")
        self.assertTrue(r1.structural_equality(r2))

        r1.build_tree_from_string(tree_string)
        r2.build_tree_from_string(tree_string)
        self.assertTrue(r1.structural_equality(r2))


    def test_build_string_from_tree(self):

        build_string = "root 3 4 2 -1 1 -1 -1 5 -1 -1 -1"
        self.assertEqual(self.root.build_string_from_tree(), build_string)


    def test_unrooted_build_tree_from_string(self):

        tree_string = "3 4 2 -1 1 -1 -1 5 -1 -1"
        local_root = tree.OrderedTreeNode.unrooted_build_tree_from_string(tree_string)
        num_children = local_root.get_num_children()
        self.assertEqual(num_children, 2)
        num_nodes = local_root.get_num_nodes()
        self.assertEqual(num_nodes, 5)

        tree_string = "3 -1 -1"
        self.assertRaises(AssertionError, tree.OrderedTreeNode.unrooted_build_tree_from_string,
                tree_string)


if __name__ == '__main__':
    unittest.main()
