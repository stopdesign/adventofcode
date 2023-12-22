data = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""


class Relay:
    def __init__(self, conf):
        # adjust the config format
        conf = conf.replace("broadcaster ", "*broadcaster ")
        role_name, targets = conf.split(" -> ")
        self.role, self.name = role_name[0], role_name[1:]

        self.inputs = {}
        self.targets = targets.split(", ")

        self.ff_state = 0

    def __repr__(self):
        return f"{self.role} {self.name} -> {self.targets}"

    def process(self, source: str, signal: int) -> list:
        output = []

        # broadcast
        if self.role == "*":
            for target in self.targets:
                output.append((self.name, target, signal))

        # flip-flop
        if self.role == "%":
            if signal == 0:
                self.ff_state = 1 - self.ff_state
                for target in self.targets:
                    output.append((self.name, target, self.ff_state))

        # conj
        if self.role == "&":
            self.inputs[source] = signal

            msg = 1 - int(all(self.inputs.values()))

            for target in self.targets:
                output.append((self.name, target, msg))

        return output


class Machine:
    def __init__(self, data):
        # parse all the relays
        self.signals_processed = {
            0: 0,
            1: 0,
        }
        self.relays = {}
        for relay_conf in data.splitlines():
            relay = Relay(relay_conf)
            self.relays[relay.name] = relay

        # init conjunction inputs
        for relay in self.relays.values():
            for target_id in relay.targets:
                target = self.relays.get(target_id)
                if target and target.role == "&":
                    target.inputs[relay.name] = 0

    def push_the_button(self):
        signals = [("button", "broadcaster", 0)]
        while signals:
            source, target, signal = signals.pop(0)
            self.signals_processed[signal] += 1
            # print()
            # print(source, target, signal)
            relay = self.relays.get(target)
            if relay:
                output = relay.process(source, signal)
                signals += output
                # print(output)
            else:
                if signal == 0:
                    print("target relay not found", target, signal)
                    break


def main(data):
    m = Machine(data)

    for n in range(1000):
        m.push_the_button()

    res = 1
    for cnt in m.signals_processed.values():
        res *= cnt

    print(f"\nres: {res}")


if __name__ == "__main__":
    data = open("day_20/input").read()
    main(data.strip())
#
