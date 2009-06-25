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

import tree
import copy
import sets

def get_c1(root, minsup):
    """Find the right most leaf of occurrences of minsup frequent 1-itemsets."""

    num_nodes = root.get_num_nodes()

    # Track the number of times each size one subtree appears as the
    # state of a node within the tree rooted at root.
    rmo = {}
    for node in root.get_nodes():
        subtree = tree.OrderedTreeNode(node.state)
        subtree_string = subtree.build_string_from_tree()
        rmo[subtree_string] = rmo.setdefault(subtree_string, []) + [node]

    # Only keep track of the tokens that occur with frequency greater
    # than minsup.
    minsup_frequent = {}
    for (sts, rmos) in rmo.items():
        if len(rmos) > minsup * num_nodes:
            minsup_frequent[sts] = rmos
    return minsup_frequent


def pl_expand(t, p, l):
    """PL expand a tree.

    Expand tree t by adding node with label l to the p-th parent of the
    right most leaf."""

    expanded = copy.deepcopy(t)
    rml = expanded.get_right_most_leaf()
    pth_parent = rml.get_pth_parent(p)
    pth_parent.append_child(l)
    return expanded


def update_rmo(t, rmos, p, l):
    """Update the RMO information for a tree."""

    # Get nodes that will be tested for expansion
    children = []
    for rmo in rmos:
        pth_parent = rmo.get_pth_parent(p)
        if pth_parent == rmo:
            # Try expanding directly below the rmo.
            children += pth_parent.get_children()
        else:
            # Try expanding children that are:
            # - below the pth parent of rmo
            # - after this branch
            p_less_one_parent = rmo.get_pth_parent(p-1)
            index = pth_parent.get_children().index(p_less_one_parent)
            children += pth_parent.get_children()[index+1:]

    # Unique-ify the children to prevent duplicate checks
    children = list(sets.Set(children))

    # Try l-expanding each node
    rmo_new = [child for child in children if child.state == l]

    return rmo_new


def expand_trees(t, candidates, minsup, token_space):
    """Expand candidates on data tree.

    Examine the subtrees within candidates.  Expand each subtree using
    each token from token_space.  For each such expanded subtree, see if
    it appears with frequency greater than minsup within the data tree
    t.
    """

    c_new = {}

    # For each subtree
    for (subtree_string, rmos) in candidates.items():

        # Construct subtree, locate right most leaf, and its depth
        subtree = tree.OrderedTreeNode.unrooted_build_tree_from_string(subtree_string)
        right_most_leaf = subtree.get_right_most_leaf()
        rml_depth = right_most_leaf.get_depth()

        # For each parent_distance (distance from rml) and token combination
        for parent_distance in range(rml_depth + 1):
            for token in token_space:

                # Create a larger candidate subtree and locate its rmos
                # within the tree t.
                candidate = pl_expand(subtree, parent_distance, token)
                candidate_string = candidate.build_string_from_tree()
                assert candidate_string not in c_new
                c_new[candidate_string] = update_rmo(t, rmos, parent_distance, token)

    # Only keep track of the tokens that occur with frequency greater
    # than minsup.
    num_nodes = t.get_num_nodes()
    minsup_frequent = {}
    for (cs, rmos) in c_new.items():
        if len(rmos) > minsup * num_nodes:
            minsup_frequent[cs] = rmos
    return minsup_frequent
