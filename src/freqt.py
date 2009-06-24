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
    """Find the right most leaf of occurances of minsup frequent 1-itemsets."""

    num_nodes = root.get_num_nodes()

    # Track the number of times each token appears as the state of a
    # node within the tree rooted at root.
    rmo = {}
    for node in root.get_nodes():
        token = node.state
        rmo[token] = rmo.setdefault(token, []) + [node]

    # Only keep track of the tokens that occure with frequency greater
    # than minsup.
    minsup_frequent = {}
    for (token, rmos) in rmo.items():
        if len(rmos) > minsup * num_nodes:
            minsup_frequent[token] = rmos
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

    # Get nodes that will be tested for exansion
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

    # Uniquify the children to prevent duplicate checks
    children = list(sets.Set(children))

    # Try l-expanding each node
    rmo_new = [child for child in children if child.state == l]

    return rmo_new
