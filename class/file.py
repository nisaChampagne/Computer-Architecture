import sys
print(sys.argv)

#open the file
if len(sys.argv) != 2:
    print("Error: must have file name")
    sys.exit(1)

try: 
    with open(sys.argv[1]) as f:
    #read all the lines
        for line in f:
            # parse out comments
            # print(line)
            comment_split = line.strip().split('#')
            # ignore blank lines

            #cast numbers from strings to ints
            value = comment_split[0].strip()
            if value == "":
                continue
            print(value)
            num = int(value)
            memory[mem_pointer] = num
            print(f"{num:08b}: {num}")
except:
    print('File not found')
    sys.exit(2)


#cast the numbers from strings to ints

#populate a memory array