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

class TreeNode():
    """Node in a tree data structure.

    Each node keeps track of a local node state, a parent node, and zero
    or more children nodes.  The parent and child relationships between
    a set of nodes define a tree structure.
    """

    node_counter = 0

    def __init__(self, state=None, parent=None):
        """Create a new node with optinal state."""
        self.parent = parent
        self.children = []
        self.state = state
        self.id = TreeNode.node_counter
        TreeNode.node_counter += 1
        return


    def _store_child(self, child):
        """Insert child under self."""
        self.children.append(child)
        return


    def append_child(self, state=None):
        """Create a new child node of self with optional state."""
        child = TreeNode(state, self)
        self._store_child(child)
        return child


    def get_num_children(self):
        """Return the number of children of a node."""
        return len(self.children)


    def get_children(self):
        """Return the children of a node."""
        return self.children


    def get_parent(self):
        """Return the parent of a node."""
        return self.parent


    def get_depth(self):
        """Return the depth of the current node.

        The root node is defined to have depth 0.
        """
        if self.parent == None:
            return 0
        else:
            return self.parent.get_depth() + 1


    def get_root(self):
        """Return the root of the tree.

        The root is assumed to be the only node in the tree that has no
        parent.
        """
        if self.parent == None:
            return self
        else:
            return self.parent.get_root()


    def __str__(self):
        """Write node child relations."""
        out_string = ""
        out_string += "node_%d_%s [label=%s]\n" % (self.id, str(self.state),
                str(self.state))
        for child in self.children:
            out_string += str(child)
            out_string += "node_%d_%s -> node_%d_%s\n" % (self.id, self.state,
                    child.id, child.state)
        return out_string


    def build_tree_from_string(self, tree_string):
        """Build a tree rooted from self using tree_string.

        The string is a space separeted serries of positive integers or
        negative one.  Tokens with positive integer values describe the
        value of a child node.  Children are inserted using a depth
        traversal, with negative one signalling a return to a parent
        node.
        """

        root = self
        current_node = root

        # Parse the token stream
        states = [int(token) for token in tree_string.split()]

        # Build the tree
        for state in states:
            assert state >= -1

            if state != -1:
                # Initialize a child using state and descend into the child
                current_node = current_node.append_child(state)

            else:
                # Move up a level in the tree
                assert current_node != root
                current_node = current_node.parent

        return root


class OrderedTreeNode(TreeNode):
    """Node within an ordered tree.

    An ordered tree defines an ordering over each child of a node.
    """


    def _store_child(self, child, index):
        """Insert child as the index-th child under self.

        The child is inserted before index.  This insertion has the same
        semantics as list.insert.
        """

        self.children.insert(index, child)
        return


    def append_child(self, state=None):
        """Create a new child node of self with optional state and
        insert it after all other children."""
        child = OrderedTreeNode(state, self)
        self._store_child(child, len(self.children))
        return child

