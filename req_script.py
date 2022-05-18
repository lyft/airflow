with open('replace_reqs.txt') as f, open('install_reqs.txt') as f2:
    lines = f.readlines()
    f2lines = f2.readlines()
    f2lines = [l.strip() for l in f2lines if '#' not in l]
    s = ''.join(f2lines)
    for line in lines:
        name, version = line.strip().split('==')
        print(name,version, f2lines)
        if name in s:
            print(name)

# with open('install_reqs.txt') as f1:
#     lines = f1.readlines()

#     with open('new_reqs.txt', 'w') as new_reqs:
#         for install_reqs_line in lines:
#             if '#' in install_reqs_line:
#                 continue
#             with open('replace_reqs.txt') as f:
#                     req_lines = f.readlines()

#                     for req_line in req_lines:
#                         name, version = req_line.split('==')
#                         if name in install_reqs_line and req_line not in open('new_reqs.txt').read():
#                             new_reqs.write(req_line + '\n')
#                         elif name not in install_reqs_line and req_line not in open('new_reqs.txt').read():
#                             new_reqs.write(install_reqs_line + '\n')
# with open('install_reqs.txt') as f:
#     setup_lines = f.readlines()

#     for setup_line in setup_lines:
#         # print(setup_line.strip())
#         with open('replace_reqs.txt') as f2:
#             req_lines = f2.readlines()

#             for req_line in req_lines:
#                 name, version = req_line.split('==')
#                 if '#' not in setup_line.strip() and name in setup_line.strip():
#                     print(f'its a candidate, reqline: {req_line}, setup line: {setup_line}')