import requests
from bs4 import BeautifulSoup
import argparse

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def dfs(self, level=0, prefix="Root"):
        if self is None:
            return

        print(" " * level + prefix + ": " + self.data)
        if self.left:
            self.left.dfs(level + 1, "L")
        if self.right:
            self.right.dfs(level + 1, "R")

    @classmethod
    def build_tree(self, root_url, depth):
        root = Node(root_url)
        visited = set()  # Keep track of visited URLs
        self.build_tree_recursive(root, depth, visited)
        return root

    @staticmethod
    def build_tree_recursive(node, depth, visited):
        if depth == 0 or node.data in visited:
            return

        visited.add(node.data)

        try:
            queue = req(node.data)
    
            for url in queue:
                if url not in visited:
                    if node.left is None:
                        node.left = Node(url)
                        Node.build_tree_recursive(node.left, depth - 1, visited)
                    elif node.right is None:
                        # print(node.data, url, "RIGHT")
                        node.right = Node(url)
                        Node.build_tree_recursive(node.right, depth - 1, visited)
                    else:
                        return
        except Exception as e:
            print(f"Error fetching URLs for {node.data}: {e}")

def req(url):
    try:
        queue = []
        response = requests.get("https://" + url.strip())
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                raw = href.split('://')[1]
                queue.append(raw)
                with open(raw.split("/")[0] + ".txt", "a") as file:
                    file.write(href + "\n")


        print(queue[0], url)
        return queue
    except:
        print(url)
        return []

def main():
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument("--url", help="Root URL to start crawling from")
    args = parser.parse_args()
    
    root_url = args.url
    depth = 20
    root = Node.build_tree(root_url, depth)
    root.dfs()

main()