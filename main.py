import argparse
from dependency_visualizer import DependencyVisualizer

def main():
    parser = argparse.ArgumentParser(description="График зависимостей")
    parser.add_argument("--graphviz-path", required=True, help="Путь к программе просмотра Graphviz.")
    parser.add_argument("--package-name", required=True, help="Название пакета для анализа.")
    parser.add_argument("--max-depth", type=int, required=True, help="Максимальная глубина зависимостей.")
    parser.add_argument("--repo-url", required=True, help="URL-адрес репозитория.")
    args = parser.parse_args()

    visualizer = DependencyVisualizer(
        repo_url=args.repo_url,
        package_name=args.package_name,
        max_depth=args.max_depth,
        graphviz_path=args.graphviz_path,
    )

    visualizer.visualize_graph()

if __name__ == "__main__":
    main()
