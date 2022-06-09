from prometheus_client import start_http_server, Gauge
import random
import time

class Project:
    def __init__(self, name, group, url):
        self.name = name
        self.group = group
        self.url = url
        
    def get_branches(self):
        return [f"{self.name}_teste-{n}" for n in random.sample(range(0, 10), 5)]
    
    def metadata(self):
        return [self.name, self.group, self.url]

class Branch:
    def __init__(self, project, branch_name):
        self.project = project
        self.branch_name = branch_name
    def get_age(self):
        return random.randint(0,10)
    def get_changed_files(self):
        return random.randint(0,10)
    def get_branch_contributors(self):
        return random.randint(0,10)

# Create a metric to track time spent and requests made.
git_project_branchs_files_changed = Gauge('git_project_branchs_files_changed', 'number of file changed in the branch', labelnames=["project_name", "project_group", "project_url", "branch_name"])
git_project_branch_age = Gauge('git_project_branch_age', 'age of the branch', labelnames=["project_name", "project_group", "project_url", "branch_name"])
git_project_branch_contributors_number = Gauge('git_project_branch_contributors_number', 'number of contributors in the branch', labelnames=["project_name", "project_group", "project_url", "branch_name"])
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    for n in range(5):
        p = Project(f"teste{n}", "loja", f"http://localhost{n}")
        for branch in p.get_branches():
            b = Branch(p, branch)
            git_project_branchs_files_changed.labels(*p.metadata(), branch).set(b.get_changed_files())
            git_project_branch_age.labels(*p.metadata(), branch).set(b.get_age())
            git_project_branch_contributors_number.labels(*p.metadata(), branch).set(b.get_branch_contributors())
    
    while True:
        time.sleep(100)
