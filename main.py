import argparse
from constants import *

class mylist(list):
    # list subclass that uses lower() when testing for 'in'
    def __contains__(self, other):
        return super(mylist,self).__contains__(other.upper())

parser = argparse.ArgumentParser()
parser.add_argument('key', choices = mylist(MUSIC_KEYS), nargs=1)
parser.add_argument('--chord_type', choices = CHORD_TYPE, default='triad', nargs=1)
parser.add_argument('--mode', choices= MODES, default='ionian')
args = parser.parse_args(('f --chord_type=triad').split()) # ToDo: remove argument when ready
print('key: %s'%(args.key[0]))

def sharp_or_flat(input_key):
    '''
    Returns True if the input key contains sharps, and False
    if the input key contains flats.

    :param input_key:
    :return: bool whether key is sharp or flat
    '''
    matches_sharp = set(input_key).intersection(set(MAJOR_SHARP_KEYS))
    print("sharp match: {}".format(matches_sharp))
    matches_flat = set(input_key).intersection(set(MAJOR_FLAT_KEYS))
    print("flat match: {}".format(matches_flat))
    matches_sharp_m = set(input_key).intersection(set(MINOR_SHARP_KEYS))
    print("sharp match minor: {}".format(matches_sharp_m))
    matches_flat_m = set(input_key).intersection(set(MINOR_FLAT_KEYS))
    print("flat match minor: {}".format(matches_flat_m))
    matches_flat_m.empty()

    if input_key in MAJOR_SHARP_KEYS or MINOR_SHARP_KEYS:
        print("Sharp key.")
        return True

    elif input_key in MAJOR_FLAT_KEYS or MINOR_FLAT_KEYS:
        print ("Flat key.")

        return False

    else:
        print("Unknown key.")
        
        return None

    ## check if flat or sharp key
    #if len(input_key) == 2:
    #    if 'b' in input_key[1]:
    #        print("Flat key.")
    #        return False
    #    elif '#' in input_key[1]:
    #        print("Sharp key.")   # this block is obsolete since all keys are defined in choices
    #        return True
    #    else:
    #        print("Unknown character.")   # this block is obsolete since all keys are defined in choices
    #        return None
    #elif len(input_key) == 1:
    #    if 'F' in input_key[0]:
    #        print("Flat key.")
    #    else:
    #        print("Sharp key.")
    #        return True
    #else:
    #    print("Wrong key input.")


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

def add_sharps_or_flats(input_key, input_notes, major_key):
    '''
        The function adds sharps or flat notes to the ordered key notes.
    :param input_key:
    :param input_notes:
    :return: key_notes
    '''

    # if the key contains sharps
    if sharp_or_flat(input_key):
        print("Contains sharp notes.")
        root = input_key
        if major_key:
            amount_sharps = MAJOR_SHARP_KEYS.index(root)
            print("Amount sharps: {}".format(amount_sharps))
            if amount_sharps == 0:
                print("Does not contain any sharps.")
                return input_notes
            sharp_notes = list((KEY_SHARPS[:(amount_sharps)]))
            print("Sharps are: {}".format(sharp_notes))
            print("Regular tones are: {}".format(KEY_SHARPS[amount_sharps:]))
            for sharp in sharp_notes:
                index = input_notes.index(sharp)
                input_notes[index] = sharp + '#'
                output_notes = input_notes
        else:
            amount_sharps = MINOR_SHARP_KEYS.index(root)
            print("Amount sharps: {}".format(amount_sharps))
            if amount_sharps == 0:
                print("Does not contain any sharps.")
                return input_notes
            sharp_notes = list((KEY_SHARPS[:(amount_sharps)]))
            print("Sharps are: {}".format(sharp_notes))
            print("Regular tones are: {}".format(KEY_SHARPS[amount_sharps:]))
            for sharp in sharp_notes:
                index = input_notes.index(sharp)
                input_notes[index] = sharp + '#'
                output_notes = input_notes

    # if the key contains flats
    else:
        print("Contains flats.")
        if major_key:
            root = input_notes[0]
            amount_flats = MAJOR_FLAT_KEYS.index(root)
            print("Amount flats: {}".format(amount_flats))
            if amount_flats == 0:
                print("Does not contain any flats.")
                return input_notes
            flat_notes = list(KEY_FLATS[:(amount_flats)])
            print("Flats are: {}".format(flat_notes))
            print("Regular tones are: {}".format(KEY_FLATS[amount_flats:]))
            for flat in flat_notes:
                index = input_notes.index(flat)
                input_notes[index] = flat + 'b'
                output_notes = input_notes
        else: # if minor
            root = input_notes[0]
            amount_flats = MINOR_FLAT_KEYS.index(root)
            print("Amount flats: {}".format(amount_flats))
            if amount_flats == 0:
                print("Does not contain any flats.")
                return input_notes
            flat_notes = list(KEY_FLATS[:(amount_flats)])
            print("Flats are: {}".format(flat_notes))
            print("Regular tones are: {}".format(KEY_FLATS[amount_flats:]))
            for flat in flat_notes:
                index = input_notes.index(flat)
                input_notes[index] = flat + 'b'
                output_notes = input_notes

    return output_notes



def main():
    # read console input
    chord_type = args.chord_type[0]
    key = args.key[0]
    # check if major or minor key
    if key[0].isupper():
        print('Major Scale')
        major = True
        if chord_type == 'seventh':
            chords_dict = {'Imaj7': '', 'ii7': '', 'iii7': '', 'IVmaj7': '', 'V7': '', 'vi7': '', 'vii7b5°': ''}
        else:
            chords_dict = {'I': '', 'ii': '', 'iii': '', 'IV': '', 'V': '', 'vi': '', 'vii°': ''}

    else:
        print('Minor Scale')
        major = False
        # check if triads or seventh chords notation
        if chord_type == 'seventh':
            chords_dict = {'i7': '', 'ii7b5': '', 'bIIImaj7': '', 'iv7': '', 'v7': '', 'bVImaj7': '', 'bVII7': ''}
        else:
            chords_dict = {'I': '', 'ii°': '', 'biii': '', 'iv': '', 'v': '', 'bVI': '', 'bVII': ''}

    # start from the root
    ordered_notes = reorder_notes(key.upper())
    # add the sharps or flats
    key_notes = add_sharps_or_flats(key, ordered_notes, major)
    # put the chords and their functions together
    chords_dict = dict(zip(chords_dict, key_notes))
    print(chords_dict)

    return 0


if __name__ == "__main__":
    # execute only if run as a script
    main()