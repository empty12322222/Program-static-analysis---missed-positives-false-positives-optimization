#初步过筛判断是不是一直指向一个空间，指向一个的话，过滤掉

def Preliminary_sifting(dictionary):
    global_arrival = {key: value for key, value in dictionary.items() if len(value) > 1}
    return global_arrival