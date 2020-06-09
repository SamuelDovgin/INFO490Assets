'''
https://colab.research.google.com/drive/1Np-Si3PLn32v48QreAVEDVPX1S4MH81u#offline=false&sandboxMode=tru


import IPython, requests
LESSON_URL = 'https://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src/dmap/lessons/tfidf'
res = requests.get('{:s}/part0.html'.format(LESSON_URL));
display(IPython.display.HTML(res.text))


lesson_map_URL = {
    'base': 'https://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src/dmap/lessons/',
    'DMP:TFIDF' : {
        'base': 'tfidf',
    }
}
class HtmlReader(object):
    def __init__(self, lesson_id):
        self.base = lesson_map.get('base') + lesson_map[lesson_id].get('base', 'na')
        try:
            from IPython.display import display, clear_output
            self.player = display
        except ImportError:
            self.player = None

    def _fetch(self, url):
        return requests.get(url).text

    def view(self, page):
        url = "{:s}/part{:d}.html".format(self.base, page)
        if self.player:
            import IPython
            from IPython.display import display, clear_output
            text = self._fetch(url)
            display(IPython.display.HTML(text))
        else:
            print('viewer not available')
        return ''
'''
