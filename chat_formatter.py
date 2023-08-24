import pyparsing as pp

user_start = pp.Literal('{{#user}}')
user_end = pp.Literal('{{/user}}')
assistant_start = pp.Literal('{{#assistant}}')
assistant_end = pp.Literal('{{/assistant}}')
gen_statement = pp.Combine('{{gen' + pp.Word(pp.printables) + '}}')

template_element = gen_statement | pp.CharsNotIn('{}')


template = pp.ZeroOrMore(
    user_start + pp.ZeroOrMore(template_element) + user_end |
    assistant_start + pp.ZeroOrMore(template_element) + assistant_end |
    template_element
)


def wrap_user(text):
    return f"{{{{#user}}}}{text}{{{{/user}}}}"


def wrap_assistant(text):
    return f"{{{{#assistant}}}}{text}{{{{/assistant}}}}"


def format_template(input_text):
    parsed = template.parseString(input_text)
    formatted_text = ""

    for segment in parsed:
        if segment.startswith('{{gen'):
            formatted_text += wrap_assistant(segment)
        else:
            formatted_text += wrap_user(segment)

    if not formatted_text.endswith("{{{{#assistant}}}}{{{{gen 'write'}}}}{{{{/assistant}}}}"):
        formatted_text += wrap_assistant("{{gen 'write'}}")

    return formatted_text


# Testing the code
input_text1 = "how are things going, tell me about New York"
output1 = format_template(input_text1)
print(output1)

input_text2 = "Tweak this proverb to apply to model instructions instead. Where there is no guidance{{gen 'rewrite'}}"
output2 = format_template(input_text2)
print(output2)
