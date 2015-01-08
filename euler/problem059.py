'''
============================================================
http://projecteuler.net/problem=59

Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value, taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random bytes. The user would keep the encrypted message and the encryption key in different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key. If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message. The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using cipher1.txt (right click and 'Save Link/Target As...'), a file containing the encrypted ASCII codes, and the knowledge that the plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the original text.
============================================================
'''

# a bar plot with errorbars
import numpy as np, operator, matplotlib.pyplot as plt

def frequency_dict(items):
    d = {}
    for x in items:
        d.setdefault(x, 0)
        d[x] += 1
    return d 
        
def freq_analysis(b, key_rank=0):
    k, v = zip(*sorted(frequency_dict(b).iteritems(), key=operator.itemgetter(1), reverse=True))
    k, v = np.array(k), np.array(v, dtype=np.float) / sum(v)
    print '#values', len(k), 'min', min(k), 'max', max(k), 'mode', k[0], 'freq', v[0]
    
    pos = np.arange(len(k))
    width = 1.0  # gives histogram aspect to the bar diagram
    
    # plt.clf()
    plt.figure()
    plt.bar(pos, v, width, color='b')
    
    ax = plt.axes()

    # Add labels
    ax.set_ylabel('Frequency')
    ax.set_title('Encrypted ASCII Code Frequency')
    ax.set_xlabel('Encrypted ASCII Code')
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(map(str, k))

    plt.show()
    return k[key_rank] ^ ord('e')

decyrpt = lambda cyphertext, password: ''.join(map(chr, cyphertext ^ np.tile(password, (np.ceil((1.0 * len(cyphertext)) / password_len),))[:len(cyphertext)]))
 
if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    cyphertext = np.array(map(int, open('problem059.dat', 'rb').readlines()[0].rstrip('\n').split(',')))
    
    plt.close('all')
    password_len = 3
    password = [freq_analysis(cyphertext[i::password_len], 1) for i in xrange(password_len)]
    print 'password', password, ''.join(map(chr, password))

    password = map(ord, 'god')
    print 'password', password, ''.join(map(chr, password))
    decrypted = decyrpt(cyphertext, password)
    print decrypted
    print sum(map(ord, decrypted))
