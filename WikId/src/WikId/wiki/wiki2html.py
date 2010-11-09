import re

__author__ = "Erik Smartt <erik at asciigamer dot com>"
__copyright__ = "Copyright 2003-2005, Erik Smartt"
__license__ = """This work is licensed under the Creative Commons Attribution-ShareAlike 2.0

Attribution-ShareAlike 2.0

You are free:

	* to copy, distribute, display, and perform the work
	* to make derivative works
	* to make commercial use of the work

Under the following conditions:

 - Attribution. You must give the original author credit.

 - Share Alike. If you alter, transform, or build upon this work, you may distribute
the resulting work only under a license identical to this one.

	* For any reuse or distribution, you must make clear to others the license terms of this work.
	* Any of these conditions can be waived if you get permission from the copyright holder.

Your fair use and other rights are in no way affected by the above.

http://creativecommons.org/licenses/by-sa/2.0/legalcode
"""
__doc__ = """A plain-text to html conversion utility.  There are
many like it, but this one is mine.
"""



## ---------------------
re_freelinkswithanchor = re.compile('(\[\[)(.*?)\#(.*?)(\]\])')
re_namedextlinks = re.compile("(\[)(http://.*?)([\|\ ])(.*?)(\])")
re_freelinks = re.compile('(\[\[)(.*?)(\]\])')
re_anchor = re.compile("(\[anchor::)(.*?)(\])")
re_img = re.compile("(\[img\ )(http://)(.*?)(\])")
re_extlinks = re.compile("(\ )+(http|https|ftp|mail|gopher)(://.*?)(\ )+")
re_bold = re.compile("(''')(.*?)(''')")
re_italic = re.compile("('')(.*?)('')")
re_h6 = re.compile("(\======)(.*?)(======)")
re_h5 = re.compile("(\=====)(.*?)(=====)")
re_h4 = re.compile("(\====)(.*?)(====)")
re_h3 = re.compile("(\===)(.*?)(===)")
re_h2 = re.compile("(\==)(.*?)(==)")
re_h1 = re.compile("(\=)(.*?)(=)")
re_ul = re.compile("(\*(.*?))(\s{3})", re.DOTALL)
re_ol = re.compile("(\#(.*?))(\s{3})", re.DOTALL)
re_li = re.compile("(\*|#)(.*?(\n|</ol>|</ul>))")
re_hr = re.compile("----")
re_href = re.compile('(\[\[)(.*?)(\]\])')
re_ehref = re.compile('(\[)(.*?)(\s)(.*?)(\])')

#re_newline = re.compile(r'\n', re.IGNORECASE)
#re_preOpen = re.compile("\[PRE\]")
#re_preClose = re.compile("\[\/PRE\]")
#re_codeOpen = re.compile("\[CODE\]")
#re_codeClose = re.compile("\[\/CODE\]")

BASE_URL = ""


## ---------------------
def cb_preformat(args):
	"""
	Implements a callback mechanism for PyBlosxom.
	
	@param args: a dict with 'parser' string and a list 'story'
	@type args: dict
	"""
	if args['parser'] == 'wiki2html':
		config = args['request'].getConfiguration()
		return parse(''.join(args['story']))

# --
def _format_freelink(mo):
	global BASE_URL

	key = mo.group(2).strip()
	repkey = key.replace(" ", "_")
	
	return "<a href='%s/index.cgi/%s'>%s</a>" % (BASE_URL, repkey, key)

# --
def _format_freelinkwithanchor(mo):
	global BASE_URL

	key = mo.group(2).strip()
	repkey = key.replace(" ", "_")
	anchor = mo.group(3).strip()
	
	return "<a href='%s/index.cgi/%s#%s'>%s</a>" % (BASE_URL, repkey, anchor, key)

# --
def parse(s, baseurl=None):
	result = s

	# Step 1, change < >'s to encoded chars.  `cgi.escape()` should do the same thing
	#result = result.replace('<', '&lt;')
	#result = result.replace('>', '&gt;')
	result = result.replace(' & ', ' &amp; ')

	# For an example of other wiki markup, take a look at:
	#   http://ciaweb.net/free/textwiki.php?page=SamplePage
	# and:
	#   http://www.usemod.com/cgi-bin/mb.pl?WikiMarkupStandard

	result = result.replace("[CODE]", "<code>")
	result = result.replace("[/CODE]", "</code>")
	result = result.replace("[PRE]", "<pre>")
	result = result.replace("[/PRE]", "</pre>")
	#result = re_preClose.sub("</pre>", result)
	#result = re_preClose.sub("</pre>", result)

	# Handle code
	#result = re_codeOpen.sub("<span class='code'>", result)
	#result = re_codeClose.sub("</span>", result)
	 
	# Handle free-links with anchors
	result = re_freelinkswithanchor.sub(_format_freelinkwithanchor, result)

	# Handle named external-links
	result = re_namedextlinks.sub(lambda mo:"<a href='%s'>%s</a>" % (mo.group(2), mo.group(4)), result)

	# Handle free-links
	result = re_freelinks.sub(_format_freelink, result)

	# Handle named anchors
	result = re_anchor.sub(lambda mo:"<a name='%s'></a>" % (mo.group(2)), result)

	# Handle linked media
	result = re_img.sub(lambda mo:"<img src='%s%s' hspace='0' vspace='0' border='0' />" % (mo.group(2), mo.group(3)), result)

	# Handle external-links
	result = re_extlinks.sub(lambda mo:" <span class='link_bracket'>&lt;</span><a href='%s%s'>%s%s</a><span class='link_bracket'>&gt;</span> " % (mo.group(2), mo.group(3), mo.group(2), mo.group(3)), result)

	# Handle bold (emphasis)
	result = re_bold.sub(lambda mo:"<strong>%s</strong>" % (mo.group(2)), result)

	# Handle italics (emphasis)
	result = re_italic.sub(lambda mo:"<em>%s</em>" % (mo.group(2)), result)

	# Handle h6
	result = re_h6.sub(lambda mo:"<h6>%s</h6>" % (mo.group(2)), result)

	# Handle h5
	result = re_h5.sub(lambda mo:"<h5>%s</h5>" % (mo.group(2)), result)

	# Handle h4
	result = re_h4.sub(lambda mo:"<h4>%s</h4>" % (mo.group(2)), result)

	# Handle h3
	result = re_h3.sub(lambda mo:"<h3>%s</h3>" % (mo.group(2)), result)

	# Handle h2
	result = re_h2.sub(lambda mo:"<h2>%s</h2>" % (mo.group(2)), result)

	# Handle h1
	result = re_h1.sub(lambda mo:"<h1>%s</h1>" % (mo.group(2)), result)
	
	result = re_ul.sub(lambda mo:"<ul>%s</ul>" % (mo.group(1)), result)
	
	result = re_ol.sub(lambda mo:"<ol>%s</ol>" % (mo.group(1)), result)
	
	result = re_li.sub(lambda mo:"<li>%s</li>" % (mo.group(2)), result)
	# Handle hr
	result = re_hr.sub("<hr />", result)
	result = re_href.sub(lambda mo:"<a href='/wiki/article/%s/'>%s</a>" % (mo.group(2), mo.group(2)), result )
	result = re_ehref.sub(lambda mo:"<a href='http://%s'>%s</a>" % (mo.group(2), mo.group(4)), result )

	# Change line breaks: replace '\n' with <br />'s
	#result = re_newline.sub('<br />', result)
	result = result.replace('\n', '<br />')

	# Now that we've done all the regex stuff, go through line-by-line
	# for additional tweaks.
	#lines = result.split()
	#for line in lines:
		#pass

	return result



## ---------------------
if __name__ == "__main__":
	import unittest
	
	## ---------------------
	class ModTest(unittest.TestCase):
		def testAnchor(self):
			self.assertEqual(parse("[anchor::foo]"), "<a name='foo'></a>")
	
		def testBold(self):
			self.assertEqual(parse("'''bold'''"), "<b>bold</b>")
	
		def testCodeOpen(self):
			self.assertEqual(parse("[PRE]"), "<pre>")
	
		def testCodeClose(self):
			self.assertEqual(parse("[/PRE]"), "</pre>")
	
		def testExternalLink(self):
			self.assertEqual(parse(" http://foo.com/ "), " <span class='link_bracket'>&lt;</span><a href='http://foo.com/'>http://foo.com/</a><span class='link_bracket'>&gt;</span> ")
	
		def testFreeLink(self):
			self.assertEqual(parse("[[foo]]"), "<a href='/index.cgi/foo'>foo</a>")
			self.assertEqual(parse("[[foo bar]]"), "<a href='/index.cgi/foo_bar'>foo bar</a>")
	
		def testFreeLinkwithAnchor(self):
			self.assertEqual(parse("[[foo#manchoo]]"), "<a href='/index.cgi/foo#manchoo'>foo</a>")
			self.assertEqual(parse("[[foo bar#manchoo]]"), "<a href='/index.cgi/foo_bar#manchoo'>foo bar</a>")
		
		def testH1(self):
			self.assertEqual(parse(" =header="), "<span class='header1'>header</span>")
	
		def testH2(self):
			self.assertEqual(parse(" ==header=="), "<span class='header2'>header</span>")
	
		def testH3(self):
			self.assertEqual(parse(" ===header==="), "<span class='header3'>header</span>")
	
		def testH4(self):
			self.assertEqual(parse(" ====header===="), "<span class='header4'>header</span>")
	
		def testH5(self):
			self.assertEqual(parse(" =====header====="), "<span class='header5'>header</span>")
	
		def testH6(self):
			self.assertEqual(parse(" ======header======"), "<span class='header6'>header</span>")
	
		def testHR(self):
			self.assertEqual(parse("----"), "<hr />")
	
		def testItalic(self):
			self.assertEqual(parse("''italics''"), "<i>italics</i>")
	
		def testLT(self):
			self.assertEqual(parse("<"), "&lt;")
	
		def testNamedLink(self):
			self.assertEqual(parse("[http://foo.com|foo]"), "<a href='http://foo.com'>foo</a>")
			self.assertEqual(parse("[http://foo.com foo]"), "<a href='http://foo.com'>foo</a>")
	
		def testNewline(self):
			self.assertEqual(parse("\n"), "<br />")
	
		def testRT(self):
			self.assertEqual(parse(">"), "&gt;")
	
		def testAmp(self):
			self.assertEqual(parse("one & two &copy; "), "one &amp; two &copy; ")

	unittest.main()
