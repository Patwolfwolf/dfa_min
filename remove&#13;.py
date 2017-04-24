
f = file("gene_hunting2.jff")
chars = f.read()
chars.replace("&#13;", "")
g = file("gene3.jff", "w")
print >> g, chars
f.close()