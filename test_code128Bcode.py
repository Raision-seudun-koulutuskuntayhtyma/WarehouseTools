# Some tests for module code128Bcode.py

import code128Bcode

def test_string2Bcode():
    # Numbers, capital letters and special characters and all arguments
    assert code128Bcode.string2barcode('A-0040-Z', 'B', 'common') == 'ÌA-0040-ZÇÎ'

    # Numbers, capital letters and special characters and default arguments
    assert code128Bcode.string2barcode('A-0040-Z') == 'ÌA-0040-ZÇÎ'

    # Only numbers (student id) and default parameters
    assert code128Bcode.string2barcode('33666') == 'Ì33666-Î'
    assert code128Bcode.string2barcode('50000') == 'Ì50000HÎ' 

    # Capital, small letters and numbers
    assert code128Bcode.string2barcode('Kotu-12345') == 'ÌKotu-12345tÎ'

    