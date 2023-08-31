
if __name__ == '__main__':
    with open('white_23q1.txt', mode='r') as f:
        lines = f.readlines()

    code_list = []
    for line in lines:
        code_str = line.strip()
        if len(code_str):
            if code_str[0] == '6':
                code_str += '.SHA'
            if code_str[0] == '0' or code_str[0] == '3':
                code_str += '.SZA'
            code_list.append(code_str)

    with open('white_23q1.txt', mode='w') as f:
        all_str = '\n'.join(code_list)
        f.write(all_str)
