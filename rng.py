import json
import random


# global variables
file_name = "file1.txt"
parameter = {}
pas_id = 0
time = 0
floor_name = []
lift_id_pool = []
burst_id_pool = []


def __init__():
    global parameter, pas_id, time, lift_id_pool, floor_name, burst_id_pool
    parameter = json.load(open('config.json', 'r', encoding="utf-8"))
    pas_id = parameter['INIT_PAS_ID']
    time = parameter['TIME']
    lift_id_pool = parameter['LIFT_ID']
    floor_name = parameter['FLOOR_NAME']
    burst_id_pool = parameter['LIFT_ID']


def mono_gen(pri, from_floor, to_floor, lift_id):
    with open(file_name, 'a') as f:
        f.write(
            str("[" + str(round(time, 1)) + "]" + str(pas_id) + "-PRI-" + str(pri) + "-FROM-" +
                str(from_floor) + "-TO-" + str(to_floor) + "-BY-" + str(lift_id) + "\n")
        )


def chaos_gen():
    global pas_id, time, lift_id_pool
    s_len = parameter['STD_LEN']
    s_range = parameter['STD_RANGE']
    _len = random.randint(s_len - s_range, s_len + s_range)
    for i in range(_len):
        pri = random.randint(1, 100)
        lift_id = random.choice(lift_id_pool)
        from_floor = random.choice(floor_name)
        to_floor = random.choice(floor_name)
        while to_floor == from_floor:
            to_floor = random.choice(floor_name)
        mono_gen(pri, from_floor, to_floor, lift_id)
        pas_id += 1


def time_little_dif_gen():
    global pas_id, time, lift_id_pool
    s_len = parameter['STD_LEN']
    s_range = parameter['STD_RANGE']
    time_dif = parameter['TIME_DIF']
    _len = random.randint(s_len - s_range, s_len + s_range)

    for i in range(_len):
        pri = random.randint(1, 100)
        lift_id = random.choice(lift_id_pool)
        from_floor = random.choice(floor_name)
        to_floor = random.choice(floor_name)
        while to_floor == from_floor:
            to_floor = random.choice(floor_name)
        mono_gen(pri, from_floor, to_floor, lift_id)
        pas_id += 1
        time += random.choice(time_dif)


def time_large_dif_gen():
    global pas_id, time, lift_id_pool
    s_len = parameter['STD_LEN']
    s_range = parameter['STD_RANGE']
    time_dif = parameter['TIME_DIF']
    _len = random.randint(s_len - s_range, s_len + s_range)
    _times = parameter['TIME_TIMES']

    for i in range(_len):
        pri = random.randint(1, 100)
        lift_id = random.choice(lift_id_pool)
        from_floor = random.choice(floor_name)
        to_floor = random.choice(floor_name)
        while to_floor == from_floor:
            to_floor = random.choice(floor_name)
        mono_gen(pri, from_floor, to_floor, lift_id)
        pas_id += 1
        for j in range(_times):
            time += random.choice(time_dif)


def mono_lift_std_burst_gen():
    global pas_id, time, lift_id_pool
    s_len = parameter['BURST_LEN']
    s_range = parameter['BURST_RANGE']
    _len = random.randint(s_len - s_range, s_len + s_range)
    if len(burst_id_pool) > 0:
        lift_id = burst_id_pool.pop(0)
    else:
        return
    for i in range(_len):
        pri = random.randint(1, 100)
        from_floor = random.choice(floor_name)
        to_floor = random.choice(floor_name)
        while to_floor == from_floor:
            to_floor = random.choice(floor_name)
        mono_gen(pri, from_floor, to_floor, lift_id)
        pas_id += 1


def mono_lift_mono_from_burst_gen():
    global pas_id, time, lift_id_pool
    s_len = parameter['BURST_LEN']
    s_range = parameter['BURST_RANGE']
    _len = random.randint(s_len - s_range, s_len + s_range)
    if len(burst_id_pool) > 0:
        lift_id = burst_id_pool.pop(0)
    else:
        return
    from_floor = random.choice(floor_name)
    for i in range(_len):
        pri = random.randint(1, 100)
        to_floor = random.choice(floor_name)
        while to_floor == from_floor:
            to_floor = random.choice(floor_name)
        mono_gen(pri, from_floor, to_floor, lift_id)
        pas_id += 1


def mono_lift_mono_to_burst_gen():
    global pas_id, time, lift_id_pool
    s_len = parameter['BURST_LEN']
    s_range = parameter['BURST_RANGE']
    _len = random.randint(s_len - s_range, s_len + s_range)
    if len(burst_id_pool) > 0:
        lift_id = burst_id_pool.pop(0)
    else:
        return
    to_floor = random.choice(floor_name)
    for i in range(_len):
        pri = random.randint(1, 100)
        from_floor = random.choice(floor_name)
        while to_floor == from_floor:
            to_floor = random.choice(floor_name)
        mono_gen(pri, from_floor, to_floor, lift_id)
        pas_id += 1


def fin_gen(req):
    for i in req:
        if i == 0:
            chaos_gen()
        elif i == 1:
            time_little_dif_gen()
        elif i == 2:
            time_large_dif_gen()
        elif i == 3:
            mono_lift_std_burst_gen()
        elif i == 4:
            mono_lift_mono_from_burst_gen()
        elif i == 5:
            mono_lift_mono_to_burst_gen()

