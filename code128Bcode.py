
def string2barcode(text, codeType='B', fontShift='common'):
    """Generates a Code 128 barcode from given text string. For Libre 128 barcode font
    Args:
        text (str): The text to be encoded into a barcode
        codeType (str, optional): Version of the barcode. Defaults to 'B'.
        fontShift (str, optional): Character set used in the text string. Defaults to 'common'.

    Returns:
        str: character string presentation of the barcode
    """
    startCodeList = {'A' : 103, 'B' : 104, 'C' : 105} # Value of the start symbol in different variations
    fontPositionList = {'common' : 100, 'uncommon' : 105, 'barcodesoft' : 145} # Systems for presentingstart and stop symbols
    addValue = fontPositionList.get(fontShift) # Get a value to shift symbols in the font
    startSymbolValue = startCodeList.get(codeType) # Choose start symbol value according to code type A, B or C
    stopSymbolValue = 106 # Allways 106
    stringToCode = text # A srting to be encoded into barcode
    cntr = 0 # Se counter to 0
    weightedSum = startSymbolValue # Add the value of the start symbol to weighted value

    # Handle all characters in the string
    for character in stringToCode:
        cntr += 1

        # Check if character more or less than or equal to 126
        if ord(character) < 127:            
            bCValue = ord(character) -32 # < 127 Original 7 bit ASCII allways subtract 32
        else:
            bCValue = ord(character) - addValue # 8 bit charater subtract according to font shifting table

        weightedSum += bCValue * cntr # Calculate the position weighted sum

    chksum = weightedSum % 103 # Calculate modulo 103 checksum

    # Build barcode 
    startSymbol = chr(startSymbolValue + addValue) # Create a start symbol accordint ot the type
    stopSymbol = chr(stopSymbolValue + addValue) # Create a stop symbol 

    # Create the checksum symbol
    if chksum < 95:
        chkSymbol = chr(chksum + 32) # Add 32 if value < 95
    else:
        chkSymbol = chr(chksum + addValue) # Add shift according to the character set used
    
    # Build and return the final barcode string
    barCode = startSymbol + stringToCode + chkSymbol + stopSymbol
    return barCode
    

if __name__ == '__main__':
    bc = string2barcode('Kotu-12345', 'B', 'common')
    print('Viivakoodi on', bc)
