# def tokenize(line: str):
#     tokens = []
#     current = ""

#     for ch in line:
#         if ch in [' ', '=', '\n']:
#             if current:
#                 tokens.append(current)
#                 current = ""
#             if ch == '=':
#                 tokens.append('=')
#         else:
#             current += ch

#     if current:
#         tokens.append(current)

#     return tokens