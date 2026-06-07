import re
from pathlib import Path

def open_path(file_to_csproj, project, all_projects):
    with open(file_to_csproj, 'r') as file:
        file_content = file.read()

        path_to_missed_ref = re.findall(pattern=r'<ProjectReference Include="(.*?)".*?>',
                                        string=file_content,
                                        flags=re.M | re.S)
        for references_path in path_to_missed_ref:
            p1 = Path(references_path)
            project_found = next((p for p in all_projects.values() if p.name == p1.stem), None)
            if project_found is None:
                continue

            project.add_mother(project_found)
            project_found.add_child(project)
