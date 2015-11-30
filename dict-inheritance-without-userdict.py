import collections
import doctest

od = lambda d={}: collections.OrderedDict(sorted(d.items()))

class CardProcessingErrors(dict):
    """
    Dictionary with predefined key/value pairs and a message for missing pairs.
    Optionally, pass optional key/value pairs as arguments when instantiating:
        - as a dict (ignoring predefined mapping completely),
            i.e CardProcessingErrors({key=value, key2=value2})
        - as kwargs (adding to/substituting predefined pairs),
            i.e CardProcessingErrors(key=value, key2=value2)

    ######################################
    # doctests___________________________#
    ######################################
    >>> defaults = CardProcessingErrors()
    >>> # {
        'incorrect_number':     "The card number is incorrect.",
        'invalid_number':       "The card number is not a valid credit card number.",
        'invalid_expiry_month': "The card's expiration month is invalid.",
        'invalid_expiry_year':  "The card's expiration year is invalid.",
        'invalid_cvc':          "The card's security code is invalid.",
        'expired_card':         "The card has expired.",
        'incorrect_cvc':        "The card's security code is incorrect.",
        'card_declined':        "The card was declined.",
        'missing':              "There is no card on a customer that is being charged.",
        'processing_error':     "An error occurred while processing the card."}
    >>> defaults['NON_EXISTING_KEY']
    'A processing error has occurred.'
    >>> # dict must be ordered before ordering it: http://bugs.python.org/issue19026
    >>> od(defaults)
    OrderedDict([('card_declined', 'The card was declined.'), ('expired_card', 'The card has expired.'), ('incorrect_cvc', "The card's security code is incorrect."), ('incorrect_number', 'The card number is incorrect.'), ('invalid_cvc', "The card's security code is invalid."), ('invalid_expiry_month', "The card's expiration month is invalid."), ('invalid_expiry_year', "The card's expiration year is invalid."), ('invalid_number', 'The card number is not a valid credit card number.'), ('missing', 'There is no card on a customer that is being charged.'), ('processing_error', 'An error occurred while processing the card.')])

    >>> #####################################
    >>> # replacement of a key (or many)    #
    >>> #####################################
    >>> single_key_replacement = CardProcessingErrors(expired_card='-'*16)
    >>> # {
        'incorrect_number':     "The card number is incorrect.",
        'invalid_number':       "The card number is not a valid credit card number.",
        'invalid_expiry_month': "The card's expiration month is invalid.",
        'invalid_expiry_year':  "The card's expiration year is invalid.",
        'invalid_cvc':          "The card's security code is invalid.",
        'expired_card':         "----------------",
        'incorrect_cvc':        "The card's security code is incorrect.",
        'card_declined':        "The card was declined.",
        'missing':              "There is no card on a customer that is being charged.",
        'processing_error':     "An error occurred while processing the card."}
    >>> od(single_key_replacement)
    OrderedDict([('card_declined', 'The card was declined.'), ('expired_card', '----------------'), ('incorrect_cvc', "The card's security code is incorrect."), ('incorrect_number', 'The card number is incorrect.'), ('invalid_cvc', "The card's security code is invalid."), ('invalid_expiry_month', "The card's expiration month is invalid."), ('invalid_expiry_year', "The card's expiration year is invalid."), ('invalid_number', 'The card number is not a valid credit card number.'), ('missing', 'There is no card on a customer that is being charged.'), ('processing_error', 'An error occurred while processing the card.')])

    >>> #####################################
    >>> # addition of key (or many)         #
    >>> #####################################
    >>> mixin_many_keys = CardProcessingErrors(new_key='*'*16, even_newer_key='#'*16)
    >>> # {
        'incorrect_number':     "The card number is incorrect.",
        'invalid_number':       "The card number is not a valid credit card number.",
        'invalid_expiry_month': "The card's expiration month is invalid.",
        'invalid_expiry_year':  "The card's expiration year is invalid.",
        'invalid_cvc':          "The card's security code is invalid.",
        'expired_card':         "The card has expired.",
        'incorrect_cvc':        "The card's security code is incorrect.",
        'card_declined':        "The card was declined.",
        'missing':              "There is no card on a customer that is being charged.",
        'processing_error':     "An error occurred while processing the card.",
        'new_key':              "****************",
        'even_newer_key':       "################"}
    >>> od(mixin_many_keys)
    OrderedDict([('card_declined', 'The card was declined.'), ('even_newer_key', '################'), ('expired_card', 'The card has expired.'), ('incorrect_cvc', "The card's security code is incorrect."), ('incorrect_number', 'The card number is incorrect.'), ('invalid_cvc', "The card's security code is invalid."), ('invalid_expiry_month', "The card's expiration month is invalid."), ('invalid_expiry_year', "The card's expiration year is invalid."), ('invalid_number', 'The card number is not a valid credit card number.'), ('missing', 'There is no card on a customer that is being charged.'), ('new_key', '****************'), ('processing_error', 'An error occurred while processing the card.')])

    >>> #####################################
    >>> # replacement of complete dict      #
    >>> #####################################
    >>> replacement_dict = CardProcessingErrors({
    ...    'custom_declined': "Declined.",
    ...    'custom_invalid':  "Invalid.",
    ...    'custom_expired':  "Expired."})
    >>> # {
        'custom_declined': "Declined.",
        'custom_invalid':  "Invalid.",
        'custom_expired':  "Expired."}
    >>> od(replacement_dict)
    OrderedDict([('custom_declined', 'Declined.'), ('custom_expired', 'Expired.'), ('custom_invalid', 'Invalid.')])

    >>> #################################################################################
    >>> # replacement of a whole dict with inline replacement for provided key/values.  #
    >>> #################################################################################
    >>> inline_replacement = CardProcessingErrors(custom_expired='-'*16, custom={
    ...     'custom_declined': "Declined",
    ...     'custom_invalid':  "Invalid",
    ...     'custom_expired':  "Expired"})
    >>> # {
        'custom_declined':      "Declined",
        'custom_invalid':       "Invalid",
        'custom_expired':       "----------------"}
    >>> od(inline_replacement)
    OrderedDict([('custom_declined', 'Declined'), ('custom_expired', '----------------'), ('custom_invalid', 'Invalid')])
    """

    __missing__ = lambda s, key: 'A processing error has occurred.'

    def __init__(self, custom=None, **kwargs):
        if custom:
            if not isinstance(custom, collections.Mapping):
                raise TypeError('must be dict or Mapping, not %s' % dict.__class__)
        else:
            custom = {
                'incorrect_number':     "The card number is incorrect.",
                'invalid_number':       "The card number is not a valid credit card number.",
                'invalid_expiry_month': "The card's expiration month is invalid.",
                'invalid_expiry_year':  "The card's expiration year is invalid.",
                'invalid_cvc':          "The card's security code is invalid.",
                'expired_card':         "The card has expired.",
                'incorrect_cvc':        "The card's security code is incorrect.",
                'card_declined':        "The card was declined.",
                'missing':              "There is no card on a customer that is being charged.",
                'processing_error':     "An error occurred while processing the card."}
        if kwargs:
            custom.update(kwargs)
        super(self.__class__, self).__init__(self, **custom)


if __name__ == "__main__":
    if __import__('sys').version_info.major < 3:
        print('Tested with Python 3.5')
    doctest.testmod()