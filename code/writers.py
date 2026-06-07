import sys
from tree import tree


def write_all_projects(all_projects):
    try:
        with open("All_Projects.txt", "w") as file:
            allProjects = 0
            count = 0
            for guid, project in all_projects.items():
                if not project.isRoot() or not project.noChild():
                    allProjects += 1
                    if project.path.endswith(".vcxproj"):
                        file.write(f"{project.name}: {project.guid} => Project ToolsVersion: {project.framework}\n")
                        file.write(f"   .vcxproj: {project.path}\n")
                        for child in project.child:
                            count += 1
                            file.write(f"   Child  {count}: {child.name} => Framework: {child.framework}\n")
                        count = 0
                        for mother in project.mother:
                            count += 1
                            file.write(f"   Mother {count}: {mother.name} => Framework: {mother.framework}\n")
                        count = 0
                        file.write(f"\n\n")
                    if project.path.endswith(".csproj"):
                        file.write(f"{project.name}: {project.guid} => Framework: {project.framework}\n")
                        file.write(f"   .csproj : {project.path}\n")
                        for child in project.child:
                            count += 1
                            file.write(f"   Child  {count}: {child.name} => Framework: {child.framework}\n")
                        count = 0
                        for mother in project.mother:
                            count += 1
                            file.write(f"   Mother {count}: {mother.name} => Framework: {mother.framework}\n")
                        count = 0
                        file.write(f"\n\n")
            file.write(f"\nNumber Project: {allProjects}")
    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(0)
    except PermissionError:
        print(PermissionError)
        sys.exit(0)


def write_independent_projects(all_projects):
    try:
        with open("Independent_Projects.txt", "w") as file:
            Independent_Projects = 0
            for guid, project in all_projects.items():
                if project.isRoot() and project.noChild():
                    Independent_Projects += 1
                    file.write(f"{project.name} {project.guid} => Framework: {project.framework}\n")
                    file.write(f"Path : {project.path}\n\n")
            file.write(f"\nNumber Project: {Independent_Projects}")
    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(0)
    except PermissionError:
        print(PermissionError)
        sys.exit(0)


def write_tree(all_projects):
    try:
        with open("Tree.txt", "w") as file:
            for guid, project in all_projects.items():
                if project.isRoot():
                    tree(file, project, 0)
        print("Build successful: \n=> Check for .txt files updates in this script's folder.")
    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(0)
    except PermissionError:
        print(PermissionError)
        sys.exit(0)
