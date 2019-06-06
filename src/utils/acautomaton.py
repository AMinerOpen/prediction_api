'''
Introduction:
The Aho-Corasick automaton is a data structure that can quickly do a multiple-keyword search across text. It’s described in the classic paper ‘Efficient string matching: an aid to bibliographic search’: http://portal.acm.org/citation.cfm?id=360855&dl=ACM&coll=GUIDE. 
'''

import queue


class node:
    def __init__(self, ch):
        self.ch = ch
        self.fail = None
        self.tail = -1
        self.len = 0
        self.children = {}


class ACAutomaton:

    def __init__(self, patterns=[]):
        self.root = node('')
        self.count = 0
        self.patterns = patterns
        if patterns:
            for pattern in patterns:
                self.insert(pattern)
            self.getfail()

    def insert(self, pattern):
        # Insert a new pattern to the trie.
        p = self.root
        for i in pattern:
            if i not in p.children.keys():
                child = node(i)
                p.children[i] = child
                p = child
            else:
                p = p.children[i]
        p.tail = self.count
        p.len = len(pattern)
        self.count += 1
        return self.count

    def getfail(self):
        # Use BFS algorithm to initialize 'fail' points.
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            top = q.get()
            for i in top.children.values():
                if top == self.root:
                    i.fail = self.root
                else:
                    p = top.fail
                    while p:
                        if i.ch in p.children.keys():
                            i.fail = p.children[i.ch]
                            break
                        p = p.fail
                    if not p:
                        i.fail = self.root
                q.put(i)

    def search(self, text):
        # Do a multiple-keyword search across text
        p = self.root
        ret = []
        for i, ch in enumerate(text):
            while ch not in p.children.keys() and p is not self.root:
                p = p.fail
            if ch in p.children.keys():
                p = p.children[ch]
            else:
                p = self.root
            tmp = p
            while tmp is not self.root:
                if tmp.tail >= 0:
                    ret.append((i-tmp.len+1, -tmp.len))
                    break
                else:
                    tmp = tmp.fail
        '''
        In this project, we need to extract some patterns from the given text and these patterns should not intersect with each other.
        For example, 'ac' and 'a' are both substrings of 'acb'. In this case, we just need 'ac'.
        Here we use greedy algorithm to maximize the keywords' length.
        '''
        ret.sort()
        ans = set()
        end = -1
        for pos, l in ret:
            length = -l
            if pos > end:
                ans.add(text[pos: pos + length])
                end = pos + length - 1
        return list(ans)
