# https://adventofcode.com/2024/day/4
# %% IMPORT
from typing import Union
from pathlib import Path
from common import INPUT_DIR, check_test
from graphlib import TopologicalSorter
import numpy as np

# %%


class Day5Quiz:
    def __init__(self, quiz_fn):
        assert quiz_fn.exists(), f"{quiz_fn} does not exist"
        self.quiz_fn = quiz_fn
        self.rules = None
        self.updates = None
        self.graph={}
        self.correct_updates = None

    def parse(self, text):
        # parse from text to rules and updates
        rules_str, updates_str = text.split("\n\n")
        rules=[]
        for line in rules_str.split("\n"):
            rules.append([int(v) for v in line.split("|")])
        updates=[]
        for line in updates_str.split("\n"):
            updates.append([int(v) for v in line.split(",")])
        return rules, updates
        
    def refine_data(self, rules, updates):
        rules_hash = {}
        self.graph={} # this shouldn't be an object, but let's make it so
        for vl, vr in rules:
            rule_l = rules_hash.get(vl, {"before":[], "after":[]})
            rule_l["after"].append(vr) # all numbers that must be after the number vl
            rule_r = rules_hash.get(vr, {"before":[], "after":[]})
            rule_r["before"].append(vl) # all numbers that must be before the number vr
            rules_hash.update({vl:rule_l, vr:rule_r})
            edges = self.graph.get(vl, set())
            edges.add(vr)
            self.graph[vl]=edges
            
        return rules_hash, updates
    def filter_updates(self, rules, updates):
        
        filtered_updates=[]
        wrong_updates=[]
        for update in updates:
            rule_broken=False
            for i, num_i in enumerate(update[:-1]):
                rule_i = rules[num_i]
                for j, num_j in enumerate(update[i+1:]):
                    rule_j = rules[num_j]                    
                    if num_j in rule_i["before"] or num_i in rule_j["after"]:
                        rule_broken=True
                        break
                if rule_broken:
                    break
            if rule_broken:
                wrong_updates.append(update)
                continue
            filtered_updates.append(update)
                
        return filtered_updates, wrong_updates
    
    def fix_updates(self, wrong_updates):
        fixed_updates=[]
        for update in wrong_updates:
            subgraph={v:self.graph.get(v, set()).intersection(set(update)) for v in update}
            ts= TopologicalSorter(subgraph)
            fixed_updates.append(list(ts.static_order()))

           
        return fixed_updates    

    def sum_middle_number(self, updates):
        num=0
        for update in updates:
            num+=update[len(update)//2]
        return num



    def get_data(self, test_data):
        if test_data is not None:
            return self.parse(test_data)
        if self.rules is None:
            with open(self.quiz_fn, "r") as fp:
                self.rules, self.updates = self.parse(fp.read())
        return self.rules, self.updates

    def solve_quiz1(self, test_data=None):
        rules, updates = self.get_data(test_data)
        rules, updates = self.refine_data(rules, updates)
        updates, _ = self.filter_updates(rules, updates)

        return self.sum_middle_number(updates)

    def solve_quiz2(self, test_data=None):
        rules, updates = self.get_data(test_data)
        rules, updates = self.refine_data(rules, updates)
        _, wrong_updates = self.filter_updates(rules, updates)
        fixed_updates = self.fix_updates(rules, wrong_updates)
        return self.sum_middle_number(fixed_updates)


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day5.txt"
    d5q = Day5Quiz(quiz_fn)

    test_data="""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    
    
    result_test1=d5q.solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=143)
    print("Quiz1 result is", d5q.solve_quiz1())
    result_test2=d5q.solve_quiz2(test_data=test_data) 
    check_test(2, result_test2, true_result=123)    
    print("Quiz2 result is", d5q.solve_quiz2())

# %%
