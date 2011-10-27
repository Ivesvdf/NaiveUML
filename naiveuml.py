#!/usr/bin/env python

import sys

def debug(str):
	sys.stderr.write(str + "\n")

class AClass:
	def __init__(self,name):
		self.name = name
		self.privates = []
		self.publics = []
		self.parents = []
		self.assoc = []
		debug("Starting class " + name)

	def addPrivateFunction(self, str):
		debug ("Adding private " + str);
		self.privates.append(str)

	def addPublicFunction(self, str):
		debug ("Adding public " + str);
		self.publics.append(str)

	def setParents(self, parents):
		debug ("Setting parents to " + str(parents))
		self.parents = parents

	def setAssociations(self, assoc):
		debug ("Setting associations to " + str(assoc))
		self.assoc = assoc

classes = []

text = sys.stdin.read()

lines = [line.strip() for line in text.split("\n") ]

i = 0

while i < len(lines):
	line = lines[i]
	nextline = lines[i+1] if i+1 < len(lines) else ""

	if len(line) == 0 or line[0] == "#":
		i += 1
		continue

	lineparts = line.split(":")
	classname = lineparts[0]

	thisClass = AClass(classname)

	if len(lineparts) > 1:
		parents = [ x.strip() for x in lineparts[1].split(",") ]
		thisClass.setParents(parents)

	if len(lineparts) > 2:
		assocs = [ x.strip() for x in lineparts[2].split(",") ]
		thisClass.setAssociations(assocs)


	if nextline == "":
		i += 2
		classes.append(thisClass)
		continue

	# Skip the = line
	i += 2

	while lines[i][0] != "=":
		thisClass.addPrivateFunction(lines[i])
		i+=1

	i+=1

	while lines[i] != "" and lines[i][0] != "=":
		thisClass.addPublicFunction(lines[i])
		i+=1

	classes.append(thisClass)

	i += 1


debug(str(len(classes)) + " classes")

out = sys.stdout

line = lambda s: out.write(s + "\n")

out.write("""
digraph G {
		fontname = "Bitstream Vera Sans"
        fontsize = 8
		rankdir=BT
		margin = 0

        node [
                fontsize = 8
				margin = 0
                shape = "none"
        ]

        edge [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
        ]

""")

filter = lambda s : s.replace("<", "&lt;").replace(">", "&gt;")
className = lambda s: "Class" + s


for c in classes:
	line("        " + className(c.name) + "[")
#	line("                label  = \"{" + "<b>" + c.name + "</b>" + "|"
#			+ "".join([str("- " + filter(priv) + "\\l")
#				for priv in c.privates]) 
#			+ "|"
#			+ "".join([str("+ " + filter(pub) + "\\l")
#				for pub in c.publics])+ "}\"")

	newname = c.name if len(c.name) > 14 else c.name.center(16, " ")
	line("                label = ")
	line("                <<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" >")
	line("                        <tr><td><font face=\"Helvetica-Bold\">")
	line(newname)
	line("</font></td></tr>")
	line("                        <tr><td align=\"left\">")
	line("".join([str("- " + filter(priv) + "<br align=\"left\"/>\n")
				for priv in c.privates]).rstrip())
	line("</td></tr>")
	line("                        <tr><td align=\"left\">")
	line("".join([str("+ " + filter(pub) + "<br align=\"left\"/>\n")
				for pub in c.publics]))
	line("</td></tr>")
	line("                </TABLE>>")
	line("        ];")
	line("")

line("""
        edge [
                arrowhead = "empty"
        ]
""")

for c in classes:
	for parent in c.parents:
		line("       " + className(c.name) + " -> " + className(parent));

line("""
        edge [
                style = "dashed"
               	arrowhead = "none"
        ]
""")

for c in classes:
	for assoc in c.assoc:
		line("       " + className(c.name) + " -> " + className(assoc));

line("}")
