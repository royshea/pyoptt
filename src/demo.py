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
import freqt
from optparse import OptionParser

if __name__ == '__main__':

    # Handle the command line
    usage = "usage: %prog [options] tree_file minsup"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Must specify tree_file and minsup")
    (tree_file, minsup_str) = args
    minsup = float(minsup_str)

    # Generate a tree
    f = open(tree_file)
    tree_string = f.readline()
    f.close()

    root = tree.OrderedTreeNode("root")
    root.build_tree_from_string(tree_string)

    # Discover subtrees that occur with frequency greater than 0.2 in subtree
    frequent_subtrees = freqt.freqt(root, minsup)

    print "# ==== Size: Original Tree ====\n"
    print "digraph {\n%s}\n\n" % root.print_tree()

    for key in sorted(frequent_subtrees.keys(), reverse=True):
        print "# ==== Size: %d ====\n" % key
        for subtree in frequent_subtrees[key]:
            print "digraph {\n%s}\n" % \
                    tree.OrderedTreeNode.unrooted_build_tree_from_string(subtree).print_tree()
