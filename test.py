class person():
    def __init__(self) -> None:
        self.buff = [{'fire':[10,5]},{'fire':[20,7]},{'gg':[30,9]}]
per = person()
if any('turtle' in b for b in per.buff):
    for buff_ in per.buff:
        try:
            buff_['turtle'][0]+=15
        except:
            pass
print(per.buff)