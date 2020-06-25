import shutil

# Determines the space left on the drive for storage. [Storing Picture Factor.]
def storage_left():
    total, used, free = shutil.disk_usage("N:\\")
    perc_free = (int(free)/int(total)) *100
    kb = int(free)/1024
    mb = kb/1024
    gb = mb/1024
    tb = gb/1024
    print(f"Storage Left on drive :{gb} GB")
    print(f"Storage Left on drive :{tb} TB")
    print(f"Percentage of storage left: {perc_free}%")

    return gb, tb, perc_free

# gb, tb, perc_free = storage_left()