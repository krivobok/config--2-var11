import subprocess
import os
import tempfile
from graphviz import Digraph

class DependencyVisualizer:
    def __init__(self, repo_url, package_name, max_depth, graphviz_path):
        self.repo_url = repo_url
        self.package_name = package_name
        self.max_depth = max_depth
        self.graphviz_path = graphviz_path
        self.dependencies = {}

    def clone_repository(self):
        temp_dir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", self.repo_url, temp_dir], check=True)
        return temp_dir

    def parse_dependencies(self, code_dir, package_name, current_depth):
        if current_depth > self.max_depth:
            return

        if package_name in self.dependencies:
            return

        self.dependencies[package_name] = set()

        for root, _, files in os.walk(code_dir):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        for line in f:
                            if line.strip().startswith("import") and package_name in line:
                                imported_package = line.split()[1].rstrip(";")
                                self.dependencies[package_name].add(imported_package)

        for dependency in self.dependencies[package_name]:
            self.parse_dependencies(code_dir, dependency, current_depth + 1)

    def generate_graph(self):
        dot = Digraph()
        for package, deps in self.dependencies.items():
            dot.node(package)
            for dep in deps:
                dot.edge(package, dep)
        return dot

    def visualize_graph(self):
        repo_path = self.clone_repository()
        try:
            self.parse_dependencies(repo_path, self.package_name, 0)
            graph = self.generate_graph()

            # Генерация и сохранение .png файла
            output_path = os.path.join(tempfile.mkdtemp(), "graph")
            graph.render(output_path, format="png", engine="dot")

            # Открытие изображения
            subprocess.run(["open", f"{output_path}.png"], check=True)
        finally:
            subprocess.run(["rm", "-rf", repo_path], check=True)
