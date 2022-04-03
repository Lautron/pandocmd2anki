import mistletoe, json
from mistletoe.ast_renderer import ASTRenderer

def open_file(filename):
    with open(filename, 'r') as md_file:
        return md_file.read()

def get_data_dict(filename):
    md = open_file(filename)
    res = mistletoe.markdown(md, ASTRenderer)
    return json.loads(res)['children']

def split_by_heading(data, level):
    parts = []
    prev_ind = None
    for ind, val in enumerate(data):
        cond1 = val.get('type') == 'Heading'
        cond2 = val.get('level') == level
        if cond1 and cond2 or ind == len(data)-1:
            if not prev_ind:
                prev_ind = ind
                continue
            if ind == len(data)-1:
                res = data[prev_ind:ind+1]
            else: 
                res = data[prev_ind:ind]
            
            parts.append(res)
            prev_ind = ind
    return parts

def parse_file(filename: str):
    data = get_data_dict(filename)
    prev_level = 1
    result = []
    chapters = split_by_heading(data, 1)

    for chapter in chapters: 
        name = chapter[0]['children'][0]['content']
        for val in chapter[1:]:
            if val.get('type') == 'Heading':
                level = val.get('level')
                if result and level > prev_level:
                    result[-1]['headings'].append(val['children'][0]['content'])

                elif result and level == prev_level:
                    result.append({
                        'headings': [*result[-1]['headings'][:-1], val['children'][0]['content']],
                                'content': ''
                        })
                else:
                    result.append({
                                'headings': [name, val['children'][0]['content']],
                                'content': ''
                        })
                prev_level = level


            else:
                for content in val['children']:
                    content_type = content.get('type')
                    if content_type == 'LineBreak':
                        continue
                    elif content_type == 'EscapeSequence':
                        result[-1]['content'] += "\\" + content['children'][0]['content']
                    elif content_type == 'ListItem':
                        result[-1]['content'] += f"{content['leader']} {content['children'][0]['children'][0]['content']}\n"
                    else:
                        result[-1]['content'] += content['content'] + "\n"
    return result
if __name__ == "__main__":
    print(get_data_dict('AYED2.pmd'))


