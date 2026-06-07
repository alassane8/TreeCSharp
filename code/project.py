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
