import re
import sys
from pathlib import Path

########################################################################################################################

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

########################################################################################################################

def open_path(file_to_csproj, project):
    with open(file_to_csproj, 'r') as file:
        file_content = file.read()

        # Looking for missed ref in .csproj that are not in .sln
        path_to_missed_ref = re.findall(pattern=r'<ProjectReference Include="(.*?)".*?>',
                                        string=file_content,
                                        flags=re.M | re.S)
        for references_path in path_to_missed_ref:
            p1 = Path(references_path)
            project_found = next((p for p in all_projects.values() if p.name == p1.stem), None)
            if project_found is None:
                continue

            # Add missed project to dependences
            project.add_mother(project_found)
            project_found.add_child(project)

########################################################################################################################

class Project:
    def __init__(self, guid: str, name: str, path: str, framework: str):
        self.guid: str = guid
        self.name: str = name
        self.path: str = path
        self.framework: str = framework
        self.mother: list[Project] = []
        self.child: list[Project] = []

    def add_child(self, child):
        if any(c for c in self.child if c.name == child.name):
            return
        self.child.append(child)

    def add_mother(self, mother):
        if any(m for m in self.mother if m.name == mother.name):
            return
        self.mother.append(mother)

    def isRoot(self):
        if len(self.mother) == 0:
            return True

    def noChild(self):
        if len(self.child) == 0:
            return True

    def RootandNoChild(self):
        if len(self.child) == 0 and len(self.mother) == 0:
            return True

    def __str__(self):
        return f"======== ({self.guid}) {self.name} - {self.path} - {self.framework}"

########################################################################################################################

all_projects: dict[str, Project] = {}

while True:
    # User input path to .sln file
    fileSLN = input("\nEnter path to .sln file:\n")

    if (fileSLN.endswith('.sln')):
        break

# Path has been checked
if fileSLN.endswith('.sln'):
    try:
        with open(fileSLN, 'r') as file:
            file_content = file.read()

            # Get project's informations => 1.name 2.path in the solution 3.GUID
            regex_projects = re.findall(pattern=r'Project.*? = "(.*?)", "(.*?)", "({.*?})',
                                        string=file_content,
                                        flags=re.RegexFlag.M)

            # Isolate path to solution
            regex_path = re.findall(pattern=r', ["](.*?)["],',
                                    string=file_content,
                                    flags=re.RegexFlag.M | re.RegexFlag.S)

            # Some projects in .sln are just folders => we don't count them as real projects
            for project_name, project_path, guid in regex_projects:
                if project_name == project_path:
                    continue

                # else we add project and it's info in dictionnary
                all_projects[guid] = Project(name=project_name,
                                             guid=guid,
                                             path=project_path,
                                             framework='')

            # Looking for projects that have dependences
            dep_projects = re.findall(pattern=r'Project.*? = "(.*?)", (.*?), (.{40})\n\tProjectSection',
                                      string=file_content,
                                      flags=re.RegexFlag.M)

            # Links projects GUID and it's dependences GUID
            regex_ProjectSections = re.findall(
                pattern=r', "(.{38})"\n\tProjectSection.*?\n\t\t(.*?)\n\tEndProjectSection$',
                string=file_content,
                flags=re.RegexFlag.M | re.RegexFlag.S)


            for project_dependences in range(len(regex_ProjectSections)):
                guid, childs = regex_ProjectSections[project_dependences]

                # Isolate dependeces GUID
                regex_Dependences = re.findall(pattern=r" = ({.*?})",
                                               string=childs,
                                              flags=re.RegexFlag.M | re.RegexFlag.S)
                if guid not in all_projects:
                    continue

                # Add project and dependences to the dictionnary
                for mother_guid in regex_Dependences:
                    all_projects[guid].add_mother(all_projects[mother_guid])
                    all_projects[mother_guid].add_child(all_projects[guid])

    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(0)

########################################################################################################################

# Parse dictionnary using GUID as key
for guid, project in all_projects.items():

    # Select folder where .sln file is
    path_to_sln = re.findall(pattern=r"(.*\\)",
                             string=fileSLN,
                             flags=re.RegexFlag.M)

    # Create path to projetc .csproj or .vcxproj
    file_to_csproj = f"{path_to_sln[0]}\\{project.path}"

    if project.path.endswith(".csproj"):
        try:
            # Open path if it's .csproj
            with open(file_to_csproj, 'r') as file:

                # Call open_path() function
                open_path(file_to_csproj, project)
                file_content = file.read()

                # For .vcxproj we only look for framework => no missed refs
                if file_to_csproj.endswith(".vcxproj"):
                    framework_version = re.search(pattern=r"<TargetFrameworkVersion.*?>(.*?)<.*?/TargetFrameworkVersion>",
                                                  string=file_content,
                                                  flags=re.M | re.I).group(1)
                    # Add project framework to class
                    project.framework = framework_version
                else:
                    framework_version = re.search(pattern=r"<TargetFramework.*?>(.*?)</TargetFramework.*?>",
                                                    string=file_content,
                                                    flags=re.M | re.I).group(1)
                    # Add project framework to class
                    project.framework = framework_version

        except FileNotFoundError:
            print(FileNotFoundError)
            print(file_to_csproj)
            sys.exit(0)
        except PermissionError:
            print(PermissionError)
            print(file_to_csproj)
            sys.exit(0)
        except AttributeError:
            project.framework = ''

########################################################################################################################

# Display of the All_Projects. txt file
try:
    with open("All_Projects.txt", "w") as file:
        allProjects = 0
        count = 0
        for guid, project in all_projects.items():
            if not project.isRoot() or not project.noChild():
                allProjects += 1
                # For .vcxproj projects
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
                # For .csproj projects
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
        file.close()

except FileNotFoundError:
    print(FileNotFoundError)
    sys.exit(0)
except PermissionError:
    print(PermissionError)
    sys.exit(0)

########################################################################################################################

# Display of the Independent_Projects.txt file
try:
    with open("Independent_Projects.txt", "w") as file:
        Independent_Projects = 0
        for guid, project in all_projects.items():
            # Looking for projects that don't have mothers nor child in solution
            if project.isRoot() and project.noChild():
                Independent_Projects += 1
                file.write(f"{project.name} {project.guid} => Framework: {project.framework}\n")
                file.write(f"Path : {project.path}\n\n")
        file.write(f"\nNumber Project: {Independent_Projects}")
        file.close()

except FileNotFoundError:
    print(FileNotFoundError)
    sys.exit(0)
except PermissionError:
    print(PermissionError)
    sys.exit(0)

########################################################################################################################

# Display of the Tree.txt file
space = 0
try:
    with open("Tree.txt", "w") as file:
        for guid, project in all_projects.items():
            # Looking for a isRoot() project to build the tree from it
            if project.isRoot():
                tree(file, project, space)
        print("Build successful: \n=> Check for .txt files updates in this script's folder.")
except FileNotFoundError:
    print(FileNotFoundError)
    sys.exit(0)
except PermissionError:
    print(PermissionError)
    sys.exit(0)

########################################################################################################################