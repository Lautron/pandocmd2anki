import mistletoe, json
from mistletoe.ast_renderer import ASTRenderer
from log import get_logger

logger, log = get_logger('debug', __name__)

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
    #__import__('pprint').pprint(data)
    prev_level = 1
    result = []
    chapters = split_by_heading(data, 1)
    def get_count(count, level): 
        res = count[level-2] 
        count[level-2] += 1
        return res

    for chap_ind, chapter in enumerate(chapters, start=1): 
        name = chapter[0]['children'][0]['content']
        count = [1, 1, 1]
        for val in chapter[1:]:
            if val.get('type') == 'Heading':
                level = val.get('level')
                if result and level > prev_level:
                    result[-1]['headings'].append((1, val['children'][0]['content']))
                    prev_level = level
                    continue

                elif result and level == prev_level:
                    headings = [*result[-1]['headings'][:-1], (get_count(count, level), val['children'][0]['content'])]

                elif result and level == prev_level-1 and level > 2:
                    headings = [*result[-1]['headings'][:-2], (get_count(count, level), val['children'][0]['content'])]

                else:
                    headings = [(chap_ind, name), (get_count(count, level), val['children'][0]['content'])]

                log('debug', level, headings)
                result.append({
                            'headings': headings,
                            'content': ''
                    })
                prev_level = level


            else:
                for content in val['children']:
                    content_type = content.get('type')
                    if content_type == 'LineBreak' or not result:
                        continue
                    elif content_type == 'EscapeSequence':
                        result[-1]['content'] += "\\" + content['children'][0]['content']
                    elif content_type == 'ListItem':
                        result[-1]['content'] += f"{content['leader']} {content['children'][0]['children'][0]['content']}\n"
                    elif content_type == 'Emphasis':
                        result[-1]['content'] += "*" + content['children'][0]['content'] + "*" + " "
                    elif content_type == 'InlineCode':
                        result[-1]['content'] += content['children'][0]['content'] + "\n"
                    elif content_type == 'Image':
                        result[-1]['content'] += content['src'] + "\n"
                    elif content_type == 'TableRow':
                        result[-1]['content'] += "TableRow" + "\n"
                    else:
                        result[-1]['content'] += content['content'] + "\n"
    return result
if __name__ == "__main__":
    parse_file('parcial1_AnNum.pmd')



