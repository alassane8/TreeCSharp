def tree(file, project, space):
    if project.isRoot():
        if project.framework == '':
            file.write("\t\t" * space + project.name + ": Could not retrieve framework\n")
        else:
            file.write("\t\t" * space + project.name + ": " + project.framework + "\n")
    else:
        for i in range(space):
            file.write("\t\t" * 2 + "|") * i
        if project.framework == '':
            file.write("------- " + project.name + ": Could not retrieve framework\n")
        else:
            file.write("------- " + project.name + ": " + project.framework + "\n")
    for child in project.child:
        tree(file, child, space + 1)
