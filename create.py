from time import sleep
import os
import logging
import yaml
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def api_request(prompt, num_tokens):
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=int(num_tokens),
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        best_of=1
    )
    output = response['choices'][0]['text']
    if '-=======-' in output:
        output = output[:output.find('-=======-')]
    sleep(20)
    return output


def create(input='test.yaml', directory='/Users/eric/pyspedas-add-project/'):
    with open(input, 'r') as f:
        project = yaml.safe_load(f)

    mission = str(project['Mission'])
    if '(' in mission:
        mission_abbr = mission.split('(')[1].strip()[:-1]
    else:
        mission_abbr = mission.strip()
    instruments = project['Instruments'].keys()
    default_trange = str(project['Default trange'])

    out_dir = os.path.join(directory, mission_abbr.lower())
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    test_dir = os.path.join(out_dir, 'tests')
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    docs_dir = os.path.join(out_dir, 'docs')
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # make the empty dunder inits first
    with open(os.path.join(test_dir, '__init__.py'), 'w') as f:
        f.write('')

    # create load.py
    logging.info('Creating load.py...')
    file = open('templates/load.py', 'r').read()

    num_tokens = 800

    prompt = """
    Mission: Colorado Student Space Weather Experiment (CSSWE)
    Instruments: Relativistic Electron and Proton Telescope integrated little experiment (REPTile)
    trange = ['2013-11-5', '2013-11-6']
    Python:
    """ + file + """
    -=======-
    Mission: """ + mission + """
    Instruments: """ + ', '.join(instruments) + """
    trange = """ + default_trange + """
    Python:
    """
    output = api_request(prompt, num_tokens)
    with open(os.path.join(out_dir, 'load.py'), 'w') as f:
        f.write(output)

    example_text = ''
    for instrument in instruments:
        if project['Instruments'][instrument].get('examples') is not None:
            example_text += instrument + ': ' + project['Instruments'][instrument]['examples'] + '\n'

    # create the README.md
    logging.info('Creating README.md...')
    file = open('templates/README.md', 'r').read()

    prompt = """
    Mission: Colorado Student Space Weather Experiment (CSSWE)
    Instruments: Relativistic Electron and Proton Telescope integrated little experiment (REPTile)
    trange = ['2013-11-5', '2013-11-6']
    Examples: 
        reptile: E1flux, P1flux
    Markdown:
    """ + file + """
    -=======-
    Mission: """ + mission + """
    Instruments: """ + ', '.join(instruments) + """
    trange = """ + default_trange + """
    Examples: 
    """ + example_text + """
    Markdown:
    """
    output = api_request(prompt, 800)
    with open(os.path.join(out_dir, 'README.md'), 'w') as f:
        f.write(output)

    # create config.py
    logging.info('Creating config.py...')
    file = open('templates/config.py', 'r').read()
    prompt = """
    Mission: Colorado Student Space Weather Experiment (CSSWE)
    Python:
    """ + file + """
    -=======-
    Mission: """ + mission + """
    Python:
    """
    output = api_request(prompt, 200)
    with open(os.path.join(out_dir, 'config.py'), 'w') as f:
        f.write(output)

    # create the tests
    logging.info('Creating tests.py...')
    file = open('templates/tests/tests.py', 'r').read()
    prompt = """
    Mission: Colorado Student Space Weather Experiment (CSSWE)
    Instruments: Relativistic Electron and Proton Telescope integrated little experiment (REPTile)
    trange = ['2013-11-5', '2013-11-6']
    Python:
    """ + file + """
    -=======-
    Mission: """ + mission + """
    Instruments: """ + ', '.join(instruments) + """
    trange = """ + default_trange + """
    Python:
    """
    output = api_request(prompt, 800)
    with open(os.path.join(test_dir, 'tests.py'), 'w') as f:
        f.write(output)

    # create the instrument load routines
    logging.info('Creating __init__.py...')
    file = open('templates/__init__.py', 'r').read()
    out = ''
    for instrument in instruments:
        prompt = """
        Mission: Colorado Student Space Weather Experiment (CSSWE)
        Instruments: Relativistic Electron and Proton Telescope integrated little experiment (REPTile)
        trange = ['2013-11-5', '2013-11-6']
        Python:
        """ + file + """
        -=======-
        Mission: """ + mission + """
        Instruments: """ + instrument + """
        trange = """ + default_trange + """
        
        """
        if project['Instruments'][instrument].get('datatypes') is not None:
            prompt += "datatypes: " + project['Instruments'][instrument]['datatypes'] + "\n"

        if project['Instruments'][instrument].get('levels') is not None:
            prompt += "levels: " + project['Instruments'][instrument]['levels'] + "\n"

        prompt += "Python:\n"
        output = api_request(prompt, 1000)
        out += output + '\n\n'

    with open(os.path.join(out_dir, '__init__.py'), 'w') as f:
        f.write(out)

    # create the docs
    logging.info('Creating API docs...')
    file = open('templates/docs/csswe.rst', 'r').read()

    prompt = """
    Mission: Colorado Student Space Weather Experiment (CSSWE)
    Instruments: Relativistic Electron and Proton Telescope integrated little experiment (REPTile)
    trange = ['2013-11-5', '2013-11-6']
    Examples: 
        reptile: E1flux, P1flux
    reStructuredText:
    """ + file + """
    -=======-
    Mission: """ + mission + """
    Instruments: """ + ', '.join(instruments) + """
    trange = """ + default_trange + """
    Examples: 
    """ + example_text + """
    reStructuredText:
    """
    output = api_request(prompt, 4000)
    with open(os.path.join(docs_dir, mission_abbr.lower() + '.rst'), 'w') as f:
        f.write(output)
