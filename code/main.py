import re
import sys

from project import Project
from open_path import open_path
from writers import write_all_projects, write_independent_projects, write_tree

all_projects: dict[str, Project] = {}

def parse_sln(fileSLN):
    try:
        with open(fileSLN, 'r') as file:
            file_content = file.read()

            regex_projects = re.findall(pattern=r'Project.*? = "(.*?)", "(.*?)", "({.*?})',
                                        string=file_content,
                                        flags=re.RegexFlag.M)

            for project_name, project_path, guid in regex_projects:
                if project_name == project_path:
                    continue
                all_projects[guid] = Project(name=project_name,
                                             guid=guid,
                                             path=project_path,
                                             framework='')

            regex_ProjectSections = re.findall(
                pattern=r', "(.{38})"\n\tProjectSection.*?\n\t\t(.*?)\n\tEndProjectSection$',
                string=file_content,
                flags=re.RegexFlag.M | re.RegexFlag.S)

            for project_dependences in range(len(regex_ProjectSections)):
                guid, childs = regex_ProjectSections[project_dependences]

                regex_Dependences = re.findall(pattern=r" = ({.*?})",
                                               string=childs,
                                               flags=re.RegexFlag.M | re.RegexFlag.S)
                if guid not in all_projects:
                    continue

                for mother_guid in regex_Dependences:
                    all_projects[guid].add_mother(all_projects[mother_guid])
                    all_projects[mother_guid].add_child(all_projects[guid])

    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(0)


def parse_projects(fileSLN):
    for guid, project in all_projects.items():
        path_to_sln = re.findall(pattern=r"(.*\\)",
                                 string=fileSLN,
                                 flags=re.RegexFlag.M)

        file_to_csproj = f"{path_to_sln[0]}\\{project.path}"

        if project.path.endswith(".csproj"):
            try:
                with open(file_to_csproj, 'r') as file:
                    open_path(file_to_csproj, project, all_projects)
                    file_content = file.read()

                    if file_to_csproj.endswith(".vcxproj"):
                        framework_version = re.search(
                            pattern=r"<TargetFrameworkVersion.*?>(.*?)<.*?/TargetFrameworkVersion>",
                            string=file_content,
                            flags=re.M | re.I).group(1)
                    else:
                        framework_version = re.search(
                            pattern=r"<TargetFramework.*?>(.*?)</TargetFramework.*?>",
                            string=file_content,
                            flags=re.M | re.I).group(1)

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


def main():
    while True:
        fileSLN = input("\nEnter path to .sln file:\n")
        if fileSLN.endswith('.sln'):
            break

    parse_sln(fileSLN)
    parse_projects(fileSLN)

    write_all_projects(all_projects)
    write_independent_projects(all_projects)
    write_tree(all_projects)


if __name__ == "__main__":
    main()
