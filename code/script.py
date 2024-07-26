import re
from pathlib import Path

########################################################################################################################
def tree(file, project, s):
    if project.isRoot():
        if project.framework == '':
            file.write("\t\t" * s + project.name + ": Could not retrieve framework\n")
        else:
            file.write("\t\t" * s + project.name + ": " + project.framework + "\n")
    else:
        for i in range(s):
            file.write("\t\t" * 2 + "|") * i
        if project.framework == '':
            file.write("------- " + project.name + ": Could not retrieve framework\n")
        else:
            file.write("------- " + project.name + ": " + project.framework + "\n")
    for child in project.child:
        tree(file, child, s + 1)

#######################################################################################################################
def open_path(file_to_sln, file_to_csproj, project):
    with open(file_to_csproj, 'r') as file:
        file_content = file.read()
        path_to_missed_ref = re.findall(pattern=r'<ProjectReference Include="(.*?)".*?>',
                                        string=file_content,
                                        flags=re.M | re.S)
        for references_path in path_to_missed_ref:
            p1 = Path(references_path)
            print(f"Project Reference: {references_path}")
            project_found = next((p for p in all_projects.values() if p.name == p1.stem), None)
            if project_found is None:
                print("!!!!!!!!!!!!! Attention, nous n'avons pas le project !!!!!!!!!!!!!")
                continue
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

    def add_mother(self, mother):
        if any(m for m in self.mother if m.name == mother.name):
            print(f"[{self.name}] We are trying to add twice the same mother: {mother.name}")
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

    def add_child(self, child):
        if any(c for c in self.child if c.name == child.name):
            print(f"[{self.name}] We are trying to add twice the same child: {child.name}")
            return
        self.child.append(child)

    def __str__(self):
        return f"======== ({self.guid}) {self.name} - {self.path} - {self.framework}"

########################################################################################################################

all_projects: dict[str, Project] = {}
fileSLN = "C:\Workspace\SigarePlus\SIG-3884_f005094_Harmonisation\SigareCSharp\SigareCSharp.sln"

if fileSLN.endswith('.sln'):
    try:
        with open(fileSLN, 'r') as file:
            file_content = file.read()
            regex_projects = re.findall(pattern=r'Project.*? = "(.*?)", "(.*?)", "({.*?})',
                                        string=file_content,
                                        flags=re.RegexFlag.M)
            regex_path = re.findall(pattern=r', ["](.*?)["],',
                                    string=file_content,
                                    flags=re.RegexFlag.M | re.RegexFlag.S)
            for project_name, project_path, guid in regex_projects:
                if project_name == project_path:
                    continue
                all_projects[guid] = Project(name=project_name,
                                             guid=guid,
                                             path=project_path,
                                             framework='')
            dep_projects = re.findall(pattern=r'Project.*? = "(.*?)", (.*?), (.{40})\n\tProjectSection',
                                      string=file_content,
                                      flags=re.RegexFlag.M)
            for i in dep_projects:
                print(i)
            regex_ProjectSections = re.findall(
                pattern=r', "(.{38})"\n\tProjectSection.*?\n\t\t(.*?)\n\tEndProjectSection$',
                string=file_content,
                flags=re.RegexFlag.M | re.RegexFlag.S)

            for i in range(len(regex_ProjectSections)):
                guid, childs = regex_ProjectSections[i]
                regex_Dependences = re.findall(pattern=r" = ({.*?})",
                                               string=childs,
                                               flags=re.RegexFlag.M | re.RegexFlag.S)
                if guid not in all_projects:
                    continue
                for mother_guid in regex_Dependences:
                    all_projects[guid].add_mother(all_projects[mother_guid])
                    all_projects[mother_guid].add_child(all_projects[guid])
    except FileNotFoundError:
        print("\nFileNotFoundError")

########################################################################################################################
for guid, project in all_projects.items():
    file_to_sln = "C:\Workspace\SigarePlus\SIG-3884_f005094_Harmonisation\SigareCSharp\\"
    file_to_csproj = f"C:\Workspace\SigarePlus\SIG-3884_f005094_Harmonisation\SigareCSharp\{project.path}"
    try:
        with open(file_to_csproj, 'r') as file:
            if project.path.endswith(".csproj"):
                print(f"\nProject Name: {project.name} {project.path}")
                open_path(file_to_sln, file_to_csproj, project)
    except FileNotFoundError:
        print(FileNotFoundError)
    except AttributeError:
       print(project.path)
#######################################################################################################################
for guid, project in all_projects.items():
    file_to_csproj = f"C:\Workspace\SigarePlus\SIG-3884_f005094_Harmonisation\SigareCSharp\{project.path}"
    try:
        with open(file_to_csproj, 'r') as file:
            file_content = file.read()
            if file_to_csproj.endswith(".csproj"):
                framework_version = re.search(pattern=r"<TargetFramework.*?>(.*?)</TargetFramework.*?>",
                                              string=file_content,
                                              flags=re.M | re.I).group(1)
                project.framework = framework_version

            if file_to_csproj.endswith(".vcxproj"):
                framework_version = re.search(pattern=r"<TargetFrameworkVersion.*?>(.*?)<.*?/TargetFrameworkVersion>",
                                              string=file_content,
                                              flags=re.M | re.I).group(1)
                project.framework = framework_version
    except FileNotFoundError:
        print("\nFileNotFoundError")
        print(file_to_csproj)
    except PermissionError:
        print("\nPermissionError: [Errno 13] Permission denied")
        print(file_to_csproj)
    except AttributeError:
        project.framework = ''
########################################################################################################################

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
        file.close()

except FileNotFoundError:
    print("\nFileNotFoundError")
except PermissionError:
    print("\nPermissionError: [Errno 13] Permission denied")
########################################################################################################################

try:
    with open("Independent_Projects.txt", "w") as file:
        Independent_Projects = 0
        for guid, project in all_projects.items():
            if project.isRoot() and project.noChild():
                Independent_Projects += 1
                file.write(f"{project.name} {project.guid} => Framework: {project.framework}\n")
                file.write(f"Path : {project.path}\n\n")
        file.write(f"\nNumber Project: {Independent_Projects}")
        file.close()

except FileNotFoundError:
    print("\nFileNotFoundError")
except PermissionError:
    print("\nPermissionError: [Errno 13] Permission denied")
########################################################################################################################

s = 0
try:
    with open("Tree.txt", "w") as file:
        for guid, project in all_projects.items():
            if project.isRoot():
                tree(file, project, s)
except FileNotFoundError:
    print("\nFileNotFoundError")
except PermissionError:
    print("\nPermissionError: [Errno 13] Permission denied")
########################################################################################################################