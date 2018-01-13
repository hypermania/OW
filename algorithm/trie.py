class Node():
    def __init__(self):
        self.children = {} 
        self.value = None

class Trie():
    def __init__(self):
        self.root = Node()
        
        
    def find(self, string):
        node = self.root
        for char in string:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.value


    def insert(self, string):
        node = self.root
        i = 0
        while i < len(string):
            if string[i] in node.children:
                node = node.children[string[i]]
                i += 1
            else:
                break

        while i < len(string):
            node.children[string[i]] = Node()
            node = node.children[string[i]]
            i += 1
        
        node.value = string

    def match_prefix(self, string):
        matches = []
        node = self.root
        for char in string:
            if char in node.children:
                node = node.children[char]
                if node.value is not None:
                    matches.append(node.value)
            else:
                break
            
        return matches

    def match_all(self, string):
        matches = []
        prefixes = self.match_prefix(string)
        for prefix in prefixes:
            if len(prefix) == len(string):
                matches.append([string])
                continue
            suffix = string[len(prefix):]
            suffix_matches = self.match_all(suffix)
            for suffix_match in suffix_matches:
                match = [prefix]
                match.extend(suffix_match)
                matches.append(match)
        return matches
        
