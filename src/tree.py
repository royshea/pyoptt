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
        """Create a new node with optional state."""
        self.parent = parent
        self.children = []
        if state:
            self.state = str(state)
        else:
            self.state = None
        self.id = TreeNode.node_counter
        TreeNode.node_counter += 1

        # Nodes contain tree level state.  This state is only valid when
        # the entire tree is in a locked state, indicating that no
        # changes can be made to the tree and thus the tree levele data
        # in each node is valid.
        self.locked = False
        self.depth = None
        self.num_successors = None

        return


    def _store_child(self, child):
        """Insert child under self."""
        self.children.append(child)
        return


    def _set_depth(self, depth):
        """Set depths of nodes."""
        self.depth = depth
        for child in self.get_children():
            child._set_depth(depth+1)
        return


    def _set_num_successors(self):
        """Set the number of successors to a given node."""
        child_successors = [child._set_num_successors() for child in self.get_children()]
        self.num_successors = sum(child_successors) + 1
        return self.num_successors


    def _lock(self):
        """Lock a node and its children."""
        self.locked = True
        for child in self.get_children():
            child._lock()


    def lock_tree(self):
        """Lock the tree.

        Calculate state for each node that is non-local (ie. number of
        nodes rooted from current location) and prevent future changes
        to the tree.  Any future changes will first require unlocking
        the tree, which invaladets non-local data.
        """
        root = self.get_root()
        root._set_depth(0)
        root._set_num_successors()
        root._lock()
        return


    def _unlock(self):
        """Unlock a node and its children."""
        self.locked = False
        self.depth = None
        self.successors = None
        for child in self.get_children():
            child._unlock()


    def unlock_tree(self):
        """Unlock the tree.

        Enable extending or modifying the tree.  This invalidates all
        non-local node data.
        """
        root = self.get_root()
        root._unlock()
        return


    def append_child(self, state=None):
        """Create a new child node of self with optional state."""
        assert self.locked == False, "Must first unlock tree.\n"
        child = TreeNode(state, self)
        self._store_child(child)
        return child


    def get_num_children(self):
        """Return the number of children of a node."""
        return len(self.get_children())


    def get_children(self):
        """Return the children of a node."""
        return self.children


    def get_parent(self):
        """Return the parent of a node."""
        return self.parent


    def get_pth_parent(self, p):
        """Return the pth parent of self.

        The 0th parent of a node is itself.  It is considered an error
        if p is greater than depth of self, since this would pass the
        root of the tree.
        """

        assert self.locked == True, "Must first lock tree.\n"
        assert p <= self.get_depth()
        if p == 0:
            return self
        else:
            return self.parent.get_pth_parent(p-1)


    def get_depth(self):
        """Return the depth of the current node.

        The root node is defined to have depth 0.
        """
        assert self.locked == True, "Must first lock tree.\n"
        return self.depth


    def get_root(self):
        """Return the root of the tree.

        The root is assumed to be the only node in the tree that has no
        parent.
        """
        if self.parent == None:
            return self
        else:
            return self.parent.get_root()


    def get_num_nodes(self, depth=0):
        """Return the number of nodes rooted under self."""
        assert self.locked == True, "Must first lock tree.\n"
        return self.num_successors


    def get_nodes(self):
        """Return the list of nodes in the tree rooted under self."""
        nodes = []
        for child in self.get_children():
            nodes += child.get_nodes()
        nodes.append(self)
        return nodes


    def build_tree_from_string(self, tree_string):
        """Build a tree rooted from self using tree_string.

        The string is a space separated serries of tokens, the string
        "-1" (negative one), or -2 (negative two).  Tokens describe the
        value of a child node.  Children are inserted using a depth
        traversal.  Negative one signals a return to a parent node.
        Negative two signals a return to the root."""

        assert self.locked == False, "Must first unlock tree.\n"
        root = self
        current_node = root

        # Build the tree
        for state in tree_string.split():

            if state == '-1':
                # Move up a level in the tree
                current_node = current_node.parent
            elif state == '-2':
                # Reset to root node
                current_node = root
            else:
                # Initialize a child using state and descend into the child
                current_node = current_node.append_child(state)

        # Require well formed build string that returns to start node
        assert current_node == root

        return root


    def print_tree(self):
        """Print the rooted tree."""
        work_list = [self]
        out_string = ""
        while work_list:
            node = work_list.pop()
            out_string += str(node)
            work_list += node.get_children()
        return out_string


    @classmethod
    def unrooted_build_tree_from_string(self, tree_string):
        """Similar to build_tree_from_string but also creates the root."""

        state = tree_string.split()
        root = TreeNode(state[0])
        return root.build_tree_from_string(" ".join(state[1:-1]))


    def __str__(self):
        """Write node child relations."""
        out_string = ""
        out_string += "node_%d_%s [label=%s]\n" % (self.id, str(self.state),
                str(self.state))
        return out_string


class OrderedTreeNode(TreeNode):
    """Node within an ordered tree.

    An ordered tree defines an ordering over each child of a node.
    """

    def __init__(self, state=None, parent=None):
        TreeNode.__init__(self, state, parent)
        self.position = None


    def get_tree_position(self):
        """Return the position of the node in the tree.

        Positions are determined based on a depth first pre-ordering.
        """
        assert self.locked == True, "Must first lock tree.\n"
        return self.position


    def _store_child(self, child, index):
        """Insert child as the index-th child under self.

        The child is inserted before index.  This insertion has the same
        semantics as list.insert.
        """

        self.children.insert(index, child)
        return


    def _update_positions(self):
        """Update the position of each node in a tree.

        Positions are determined based on a depth first pre-ordering
        with the root node at position 0.
        """
        root = self.get_root()
        nodes = root.get_nodes()
        for (node, position) in zip(nodes, range(len(nodes))):
            node.position = position


    def _clear_positions(self):
        """Clear position information."""
        self.position = None
        for child in self.get_children():
            child._clear_positions()


    def unlock_tree(self):
        TreeNode.unlock_tree(self)
        root = self.get_root()
        root._clear_positions()


    def lock_tree(self):
        TreeNode.lock_tree(self)
        self._update_positions()


    def append_child(self, state=None):
        """Create a new child node of self with optional state and
        insert it after all other children."""
        assert self.locked == False, "Must first unlock tree.\n"
        child = OrderedTreeNode(state, self)
        self._store_child(child, len(self.get_children()))
        return child


    def get_nodes(self):
        """Return the list of nodes in the tree rooted under self.

        List is gaunted to be in depth first pre-order.
        """
        nodes = [self]
        for child in self.get_children():
            nodes += child.get_nodes()
        return nodes


    def get_right_most_leaf(self):
        """Return the right most leaf of the tree rooted at self."""
        if self.get_children() == []:
            return self
        else:
            return self.get_children()[-1].get_right_most_leaf()


    def structural_equality(self, other):
        """State and connectivity equality over the rooted subtree.

        Note that this is defined over OrderedTreeNode trees since it
        assumes a specific ordering of child nodes."""

        # Ensure that the current nodes are equal
        if self.state == other.state and \
                len(self.get_children()) == len(other.children):
            for (self_child, other_child) in zip(self.get_children(),
                    other.children):
                if self_child.structural_equality(other_child): continue
                else: return False
        else: return False

        return True


    def build_string_from_tree(self):
        """Generate a "build string" from rooted subtree.

        This function is the inverse of build_tree_from_string and
        generates a string description of the tree that can be used by
        build_tree_from_string to regenerate the tree.  This is NOT the
        default __str__ function used for pretty printing a tree.  Note
        that this is defined over OrderedTreeNode trees since it assumes
        a specific ordering of child nodes.
        """

        out_string = "%s" % self.state
        for child in self.get_children():
            out_string += " " + child.build_string_from_tree()
        out_string += " -1"
        return out_string


    @classmethod
    def unrooted_build_tree_from_string(self, tree_string):
        """OrderedTreeNode version of unrooted_build_tree_from_string."""

        state = tree_string.split()
        root = OrderedTreeNode(state[0])
        return root.build_tree_from_string(" ".join(state[1:-1]))
