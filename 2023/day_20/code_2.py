from time import monotonic, sleep

data = """
broadcaster -> kv
%kv -> xr, hr
%xr -> qq, hr
%qq -> dh
%dh -> hr, nm
%nm -> rb, hr
%rb -> xl, hr
%xl -> jd
%jd -> hr, bm
%bm -> hr, fj
%fj -> pt, hr
%pt -> lg, hr
%lg -> hr
&hr -> hh, kv, xl, qq
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

    def process_signal(self, source: str, signal: int) -> list:
        output = []

        # flip-flop
        if self.role == "%" and signal == 0:
            self.ff_state = 1 - self.ff_state
            for target in self.targets:
                output.append((self.name, target, self.ff_state))

        # conj
        elif self.role == "&":
            self.inputs[source] = signal

            msg = 1 - int(all(self.inputs.values()))

            for target in self.targets:
                output.append((self.name, target, msg))

        # broadcast
        elif self.role == "*":
            for target in self.targets:
                output.append((self.name, target, signal))

        return output


class Machine:
    def __init__(self, data):
        # parse all the relays
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

    def push_the_button(self, push_cnt):
        signals = [("button", "broadcaster", 0)]
        while signals:
            source, target_id, signal = signals.pop(0)
            if target_id in self.relays:
                target_relay = self.relays[target_id]
                signals += target_relay.process_signal(source, signal)
                # When the Ring node recieves a signal 0
                if target_relay.name in ["fh", "fn", "hh", "lk"] and signal == 0:
                    print(">>", source, signal, push_cnt)


def main(data):
    m = Machine(data)

    ring_periods = []

    for n in range(1, 5000):
        ring_periods.append(m.push_the_button(n))
    
    # print(ring_periods)


if __name__ == "__main__":
    data = open("day_20/input").read()
    main(data.strip())
#
