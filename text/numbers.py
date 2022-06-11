""" from https://github.com/keithito/tacotron """

import inflect
import re
import num2words


_inflect = inflect.engine()
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_pounds_re = re.compile(r'£([0-9\,]*[0-9]+)')
_dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_manats_re = re.compile(r'\₼([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)')
_ordinal_re_az = re.compile(r'[0-9]+(ıncı|inci|nci|üncü|uncu)')
_number_re = re.compile(r'[0-9]+')


def _remove_commas(m):
  return m.group(1).replace(',', '')


def _expand_decimal_point(m):
  return m.group(1).replace('.', ' point ')


def _expand_decimal_point_az(m):
  return m.group(1).replace('.', ' nöqtə ')


def _expand_dollars(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts) > 2:
    return match + ' dollars'  # Unexpected format
  dollars = int(parts[0]) if parts[0] else 0
  cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if dollars and cents:
    dollar_unit = 'dollar' if dollars == 1 else 'dollars'
    cent_unit = 'cent' if cents == 1 else 'cents'
    return '%s %s, %s %s' % (dollars, dollar_unit, cents, cent_unit)
  elif dollars:
    dollar_unit = 'dollar' if dollars == 1 else 'dollars'
    return '%s %s' % (dollars, dollar_unit)
  elif cents:
    cent_unit = 'cent' if cents == 1 else 'cents'
    return '%s %s' % (cents, cent_unit)
  else:
    return 'zero dollars'
  
  
def _expand_manat(m):
  match = m.group(1)
  parts = match.split('.')
  if len(parts) > 2:
    return match + ' manat'  # Unexpected format
  manats = int(parts[0]) if parts[0] else 0
  qepik = int(parts[1]) if len(parts) > 1 and parts[1] else 0
  if manat and qepik:
    manats_unit = 'manat' if manats == 1 else 'manat'
    qepik_unit = 'qəpik' if qepik == 1 else 'qəpik'
    return '%s %s, %s %s' % (manats, manats_unit, qepik, qepik_unit)
  elif manats:
    manats_unit = 'manat' if manats == 1 else 'manat'
    return '%s %s' % (manats, manats_unit)
  elif qepik:
    qepik_unit = 'qəpik' if qepik == 1 else 'qəpik'
    return '%s %s' % (qepik, qepik_unit)
  else:
    return 'sıfır manat'


def _expand_ordinal(m):
  return _inflect.number_to_words(m.group(0))

def _expand_ordinal_az(m):
  return num2words.num2words(m, lang="az", to="ordinal")


def _expand_number(m):
  num = int(m.group(0))
  if num > 1000 and num < 3000:
    if num == 2000:
      return 'two thousand'
    elif num > 2000 and num < 2010:
      return 'two thousand ' + _inflect.number_to_words(num % 100)
    elif num % 100 == 0:
      return _inflect.number_to_words(num // 100) + ' hundred'
    else:
      return _inflect.number_to_words(num, andword='', zero='oh', group=2).replace(', ', ' ')
  else:
    return _inflect.number_to_words(num, andword='')
  
  
def expand_numbers_az(m):
  num = int(m.group(0))
  if num != 0:
    return num2words.num2words(num, lang='az')
  else:
    return 'sıfır'


def normalize_numbers(text):
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_pounds_re, r'\1 pounds', text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point, text)
  text = re.sub(_ordinal_re, _expand_ordinal, text)
  text = re.sub(_number_re, _expand_number, text)
  return text

def normalize_numbers_az(text):
  text = re.sub(_comma_number_re, _remove_commas, text)
  text = re.sub(_pounds_re, r'\1 sterlin', text)
  text = re.sub(_dollars_re, _expand_dollars, text)
  text = re.sub(_manats_re, _expand_manat, text)
  text = re.sub(_decimal_number_re, _expand_decimal_point_az, text)
  text = re.sub(_ordinal_re_az, _expand_ordinal_az, text)
  text = re.sub(_number_re, expand_numbers_az, text)
  return text
