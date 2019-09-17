import json
import numpy as np
import pandas as pd
import re
from dateutil.parser import parse

from pandas_datareader.base import _BaseReader
from pandas_datareader.compat import string_types


class GoogleQuotesReader(_BaseReader):

    """Get current google quote
       WARNING: OFFLINE AS OF OCT 1, 2017
    """

    @property
    def url(self):
        return 'https://finance.google.com/finance/info'

    @property
    def params(self):
        """Parameters to use in API calls"""
        if isinstance(self.symbols, string_types):
            sym_list = self.symbols
        else:
            sym_list = ','.join(self.symbols)
        params = {'q': sym_list}
        return params

    def _read_lines(self, out):
        buffer = out.read()
        m = re.search('// ', buffer)
        result = json.loads(buffer[m.start() + len('// '):])
        return pd.DataFrame([[float(x['cp']), float(x['l'].replace(',', '')),
                              np.datetime64(parse(x['lt']).isoformat())]
                             for x in result], columns=['change_pct',
                                                        'last', 'time'],
                            index=[x['t'] for x in result])
