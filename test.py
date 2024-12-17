import unittest
from unittest.mock import patch
from dependency_visualizer import DependencyVisualizer

class TestDependencyVisualizer(unittest.TestCase):

    @patch("subprocess.run")
    def test_clone_repository(self, mock_subprocess):
        visualizer = DependencyVisualizer("https://github.com/google/guava.git", "com.google.guava", 2, "/path/to/graphviz")
        temp_dir = visualizer.clone_repository()
        mock_subprocess.assert_called_with(["git", "clone", "https://github.com/google/guava.git", temp_dir], check=True)

    @patch("os.walk")
    @patch("builtins.open", create=True)
    def test_parse_dependencies(self, mock_open, mock_walk):
        mock_walk.return_value = [("/code", [], ["Test.java"])]
        mock_open.return_value.__enter__.return_value = iter(["import com.google.guava.dependency;"])

        visualizer = DependencyVisualizer("https://github.com/google/guava.git", "com.google.guava", 2, "/path/to/graphviz")
        visualizer.parse_dependencies("/code", "com.google.guava", 0)

        self.assertIn("com.google.guava", visualizer.dependencies)
        self.assertIn("com.google.guava.dependency", visualizer.dependencies["com.google.guava"])

    def test_generate_graph(self):
        visualizer = DependencyVisualizer("https://github.com/google/guava.git", "com.google.guava", 2, "/path/to/graphviz")
        visualizer.dependencies = {
            "com.google.guava": {"com.google.guava.dependency"},
            "com.google.guava.dependency": set()
        }
        graph = visualizer.generate_graph()

        # Проверка на наличие узла и рёбер в графе
        self.assertIn("com.google.guava", graph.source)
        self.assertIn('"com.google.guava" -> "com.google.guava.dependency"', graph.source)

if __name__ == "__main__":
    unittest.main()
