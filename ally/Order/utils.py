# MIT License
#
# Copyright (c) 2020 Brett Graves
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import xml.etree.cElementTree as ET


def shouldIgnore ( s ):
	"""Should we ignore the key s?
	(Right now, returns true if s takes the form
	"__xxxxx...", prepended by two '_' chars
	"""
	return len(s) > 1 and s[:2] == '__'




def woodChipper ( tree ):
	"""Given a tree structure,
	sort out the leaves from the subtrees (and also aggregate all the other junk)
	"""
	leaves	= []
	trees	= []

	for k,v in tree.items():

		if not shouldIgnore(k):

			# Pull out the subtrees
			if isinstance(v, dict):
				trees.append ( (k,v) )


			# Pull out the leaves
			else:
				leaves.append ( (k,str(v)) )


	return leaves, trees






def _transposeTreeHelper ( tree, name="unnamed_tree", work=None ):
	"""Recursive steps of vvvv
	"""

	# Sort all this stuff out
	leaves, trees = woodChipper ( tree )


	# Create this current object
	root = ET.SubElement(
		work,
		name,
		attrib = dict(leaves)
	)


	# Now add all of our branches
	for name, subtree in trees:

		# Now pass this root object off to the helper
		_transposeTreeHelper ( subtree, name=name, work=root )







def transposeTree ( tree, name="unnamed_tree", stringify=True, ):
	"""Give me a nested dictionary structure, where at each level:

		- Leaves should become XML attributes
		- Subtrees become subtags
	"""

	# Sort all this stuff out
	leaves, trees = woodChipper ( tree )


	# Create the root element, and add any needed leaves
	root = ET.Element(
		name,
		attrib = dict(leaves)
	)

	# Now add all of our branches
	for name, subtree in trees:

		# Now pass this root object off to the helper
		_transposeTreeHelper ( subtree, name=name, work=root )


	# And return the new tree
	if stringify:
		return ET.tostring(root)

	# Return raw tree
	else:
		return root







def fixTag ( tag ):
	return tag.split('}',1)[-1]



def parseTree ( tree ):

	if isinstance(tree, str):
		tree = ET.fromstring(tree)

	if tree is None:
		return {}
		
	x = tree.attrib

	for child in tree:
		x = { **x, **parseTree(child) }
	

	return  { fixTag(tree.tag) : x }
