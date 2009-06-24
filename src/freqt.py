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

def get_c1(root, minsup):
    """Find the right most occurance of minsup frequent 1-itemsets."""

    num_nodes = root.get_num_nodes()

    # Track the number of times each token appears as the state of a
    # node within the tree rooted at root.
    occurrences = {}
    rmo = {}
    for node in root.get_nodes():
        token = node.state
        occurrences[token] = occurrences.get(token, 0) + 1
        rmo[token] = node.get_tree_position()

    # Only keep track of the tokens that occure with frequency greater
    # than minsup
    minsup_frequent = {}
    for (token, value) in occurrences.items():
        if value > minsup * num_nodes:
            minsup_frequent[token] = rmo[token]

    return minsup_frequent
