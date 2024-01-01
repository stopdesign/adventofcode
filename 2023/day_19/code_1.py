from dataclasses import dataclass

data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_conf(cls, conf):
        pairs = conf.strip("{").strip("}").split(",")
        init_values = {}
        for pair in pairs:
            k, v = pair.split("=")
            init_values[k] = int(v)
        return cls(**init_values)

    @property
    def sum(self):
        return self.x + self.m + self.a + self.s


@dataclass
class Rule:
    condition: str
    dest: str

    @classmethod
    def from_conf(cls, conf):
        if ":" in conf:
            condition, dest = conf.split(":")
        else:
            condition = ""
            dest = conf
        return cls(condition, dest)

    def apply(self, part):
        # return destination
        if not self.condition:
            return self.dest

        param_name = self.condition[0]
        comp = self.condition[1]
        value = int(self.condition[2:])

        if comp == "<":
            if getattr(part, param_name) < value:
                return self.dest

        if comp == ">":
            if getattr(part, param_name) > value:
                return self.dest

        # no rules applied
        return ""


@dataclass
class Workflow:
    name: str
    rules: list

    @classmethod
    def from_conf(cls, conf):
        name, rules_conf = conf.strip("}").split("{")
        rules_raw = rules_conf.split(",")
        rules = [Rule.from_conf(r) for r in rules_raw]
        return cls(name, rules)

    def test_part(self, part):
        for rule in self.rules:
            if res := rule.apply(part):
                return res


def main(data):
    workflows_raw, parts_raw = data.split("\n\n")

    parts = [Part.from_conf(conf) for conf in parts_raw.splitlines()]

    workflows = {}
    for conf in workflows_raw.splitlines():
        wf = Workflow.from_conf(conf)
        workflows[wf.name] = wf

    total_sum = 0

    for part in parts:
        print(part, end=": ")

        next_wf_key = "in"

        while wf := workflows.get(next_wf_key):
            next_wf_key = wf.test_part(part)
            if next_wf_key in ["A", "R"]:
                break

        # part is accepted
        if next_wf_key == "A":
            total_sum += part.sum

        print(next_wf_key)

    print()
    print(total_sum)


if __name__ == "__main__":
    # data = open("day_19/input").read()
    main(data.strip())
#
