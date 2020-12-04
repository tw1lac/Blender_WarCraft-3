import re


class Reader:
    def __init__(self, file):
        print("reading")
        self.file = file
        print("got file")
        self.chunks = chunkifier(file)
        print("split file into chunks")

    def parse(self, context):
        pass

    def read(self, bracket_count):
        line = self.file.readline().replace(",", "").strip()
        bracket_count = count_brackets(bracket_count, line)
        return line, bracket_count


def chunkifier(chunk_to_split):
    chunks = []
    last_bracket = chunk_to_split.rfind('}')
    split_start = 0

    while split_start < last_bracket:
        end_bracket_index = chunk_to_split.index("}", split_start)
        bracket_count = count_brackets(0, chunk_to_split[split_start:end_bracket_index+1])
        while bracket_count > 0:
            end_bracket_index = chunk_to_split.index("}", end_bracket_index+1)
            bracket_count = count_brackets(0, chunk_to_split[split_start:end_bracket_index+1])
        chunks.append(chunk_to_split[split_start:end_bracket_index+1].strip('\n\t\r ,'))
        split_start = end_bracket_index+1

    return chunks


def extract_bracket_content(stuff):
    # print("extract_bracket_content")
    split_start = stuff.find("{")+1
    # bracket_count = 1
    end_bracket_index = stuff.find("}")
    bracket_count = count_brackets(0, stuff[0:end_bracket_index + 1])
    # print(stuff[split_start:end_bracket_index + 1])
    # print(end_bracket_index)
    while bracket_count > 0:
        # print(bracket_count)
        end_bracket_index = stuff.find("}", end_bracket_index + 1)
        bracket_count = count_brackets(0, stuff[0:end_bracket_index+1])
    # print("found stuff!")
    # print(stuff[split_start:end_bracket_index].strip())
    return stuff[split_start:end_bracket_index].strip()


def count_brackets2(line):
    start_brackets = line.count('{')
    end_brackets = line.count('}')
    return start_brackets - end_brackets


def count_brackets(bracket_count, line):
    start_brackets = line.count('{')
    end_brackets = line.count('}')
    bracket_count += start_brackets
    bracket_count -= end_brackets
    return bracket_count


def get_between(line, start, end):
    start_point = line.find(start)
    # print(start_point)
    end_point = line.find(end, start_point)
    # print(end_point)
    if end_point == -1:
        end_point = len(line)
    thing = line[start_point:end_point].replace(start, "").strip()
    # print(thing)
    return thing


def extract_float_values(line):
    no_bracket_line = extract_bracket_content(line).strip(',')
    if no_bracket_line == '':
        no_bracket_line = line.strip(',')
    line_value_strings = re.split(', *', no_bracket_line)
    line_values = []
    # if re.match('\\s*\\d+.*\\d*\\s*', no_bracket_line):
    if re.match('[\\s\\S]*\\d+[\\s\\S]*', no_bracket_line):
        for v_string in line_value_strings:
            line_values.append(float(v_string))
    return line_values


def extract_int_values(line):
    no_bracket_line = extract_bracket_content(line).strip(',')
    if no_bracket_line == '':
        no_bracket_line = line.strip(',')
    # print(no_bracket_line)
    line_value_strings = re.split(', *', no_bracket_line)
    # print(line_value_strings)
    line_values = []
    # if re.match('\\s*\\d+\\s*', no_bracket_line):
    if re.match('[\\s\\S]*\\d+[\\s\\S]*', no_bracket_line):
        for v_string in line_value_strings:
            # print(v_string.strip('\n\t '))
            line_values.append(int(v_string.strip('\n\t ')))
    return line_values
