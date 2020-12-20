import argparse
from constants import *

class mylist(list):
    # list subclass that uses lower() when testing for 'in'
    def __contains__(self, other):
        return super(mylist,self).__contains__(other.upper())

parser = argparse.ArgumentParser()
parser.add_argument('key', choices = MUSIC_KEYS, nargs=1)
parser.add_argument('--chord_type', choices = CHORD_TYPE, default='triad', nargs=1)
parser.add_argument('--mode', choices= MODES, default='ionian')
args = parser.parse_args(('Gb --chord_type=triad').split()) # ToDo: remove argument when ready
print('key: %s'%(args.key[0]))

def sharp_or_flat(input_key):
    '''
    Returns True if the input key contains sharps, and False
    if the input key contains flats.

    :param input_key:
    :return: bool whether key is sharp or flat
    '''
    # check if flat or sharp key
    if len(input_key) == 2:
        if 'b' in input_key[1]:
            print("Flat key")
            return False
        else:
            print("Unknown character.")   # this block is obsolete since all keys are defined in choices ToDo: remove
            return None
    else:
        print("Sharp key.")
        return True


def reorder_notes(input_key):
    '''
    Reorders the notes according to the chosen tonic.

    :param input_key: the input key
    :return: list of the notes belonging to this key
    '''
    # make uppercase
    input_key[0].upper()
    # find the index of the chosen key
    start_index = MUSIC_NOTES.index(input_key[0])
    # find the length (should be always 7)
    length = len(MUSIC_NOTES)
    print(start_index, length)
    # extract the notes for the key in the right order
    key_notes = (list(MUSIC_NOTES[start_index:(length)]))
    key_notes.extend(MUSIC_NOTES[0:start_index])

    return key_notes

def add_sharps_or_flats(input_key, input_notes):
    '''
        The function adds sharps or flat notes to the ordered key notes.
    :param input_key:
    :param input_notes:
    :return: key_notes
    '''

    # if the key contains sharps
    if sharp_or_flat(input_key):
        print("Contains sharp")
        root = input_notes[0]
        amount_sharps = MAJOR_SHARP_KEYS.index(root)
        print("Amount sharps: {}".format(amount_sharps))
        if amount_sharps == 0:
            print("Does not contain any sharps.")
            return input_notes
        sharp_notes = list((MAJOR_KEYS_SHARPS[:(amount_sharps)]))
        print("Sharps are: {}".format(sharp_notes))
        print("Regular tones are: {}".format(MAJOR_KEYS_SHARPS[amount_sharps:]))
        for sharp in sharp_notes:
            index = input_notes.index(sharp)
            input_notes[index] = sharp + '#'
            output_notes = input_notes

    # if the key contains flats
    else:
        print("Contains flats.")
        root = input_notes[0]
        amount_flats = MAJOR_FLAT_KEYS.index(root)
        print("Amount flats: {}".format(amount_flats))
        if amount_flats == 0:
            print("Does not contain any flats.")
            return input_notes
        flat_notes = list(MAJOR_KEYS_FLATS[:(amount_flats)])
        print(flat_notes)
        output_notes = 0



    return output_notes





def main():
    chord_type = args.chord_type[0]
    key = args.key[0]
    major_scale = False
    # check if major or minor key
    if key[0].isupper():
        print('Major Scale')
        major_scale = True
        if chord_type == 'seventh':
            chords_dict = {'Imaj7': '', 'ii7': '', 'iii7': '', 'IVmaj7': '', 'V7': '', 'vi7': '', 'vii7b5°': ''}
        else:
            chords_dict = {'I': '', 'ii': '', 'iii': '', 'IV': '', 'V': '', 'vi': '', 'vii°': ''}

    else:
        print('minor Scale')
        # check if triads or seventh chords notation
        if chord_type == 'seventh':
            chords_dict = {'i7': '', 'ii7b5': '', 'bIIImaj7': '', 'iv7': '', 'v7': '', 'bVImaj7': '', 'bVII7': ''}
        else:
            chords_dict = {'I': '', 'ii°': '', 'biii': '', 'iv': '', 'v': '', 'bVI': '', 'bVII': ''}

    # estimate the right note order for this key
    ordered_notes = reorder_notes(key.upper())
    key_notes = add_sharps_or_flats(key, ordered_notes)
    chords_dict = dict(zip(chords_dict, key_notes))
    print(chords_dict)

    return 1



if __name__ == "__main__":
    # execute only if run as a script
    main()