import re
import collections
from decimal import Decimal
from pdict import PreservingDict


def cfour_harvest(outtext):
    """
    Function to read CFOUR output file *outtext* and parse important quantum chemical information from it in
    """
    psivar = PreservingDict()

#    TODO: BCC
#          CI
#          QCISD(T)
#          other ROHF tests
#          vcc/ecc

    NUMBER = "((?:[-+]?\\d*\\.\\d+(?:[DdEe][-+]?\\d+)?)|(?:[-+]?\\d+\\.\\d*(?:[DdEe][-+]?\\d+)?))"

    # Process NRE
    mobj = re.search(r'^\s+' + r'(?:Nuclear repulsion energy :)' + r'\s+' + NUMBER + r'\s+a\.u\.\s*$',
        outtext, re.MULTILINE)

    if mobj:
        print('matched nre')
        psivar['NUCLEAR REPULSION ENERGY'] = mobj.group(1)

    # Process SCF
    mobj = re.search(
        r'^\s+' + r'(?:E\(SCF\))' + r'\s+=\s+' + NUMBER + r'\s+a\.u\.\s*$',
        outtext, re.MULTILINE)
    if mobj:
        print('matched scf1')
        psivar['SCF TOTAL ENERGY'] = mobj.group(1)

    mobj = re.search(
        r'^\s+' + r'(?:E\(SCF\)=)' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE)
    if mobj:
        print('matched scf2')
        psivar['SCF TOTAL ENERGY'] = mobj.group(1)

    mobj = re.search(
        r'^\s+' + r'(?:SCF has converged.)' + r'\s*$' +
        r'(?:.*?)' +
        r'^\s+' + r'(?:\d+)' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched scf3')
        psivar['SCF TOTAL ENERGY'] = mobj.group(1)

    # Process MP2
    mobj = re.search(
        r'^\s+' + r'(?:E2\(AA\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(AB\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(TOT\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:Total MP2 energy)' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*$',
        outtext, re.MULTILINE)
    if mobj:
        print('matched mp2r')
        psivar['MP2 SAME-SPIN ENERGY'] = 2 * Decimal(mobj.group(1))
        psivar['MP2 OPPOSITE-SPIN ENERGY'] = mobj.group(2)
        psivar['MP2 CORRELATION ENERGY'] = 2 * Decimal(mobj.group(1)) + Decimal(mobj.group(2))
        psivar['MP2 TOTAL ENERGY'] = mobj.group(4)

    mobj = re.search(
        r'^\s+' + r'(?:E2\(AA\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(BB\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(AB\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(TOT\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:Total MP2 energy)' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*$',
        outtext, re.MULTILINE)
    if mobj:
        print('matched mp2u')
        psivar['MP2 SAME-SPIN ENERGY'] = Decimal(mobj.group(1)) + Decimal(mobj.group(2))
        psivar['MP2 OPPOSITE-SPIN ENERGY'] = mobj.group(3)
        psivar['MP2 CORRELATION ENERGY'] = Decimal(mobj.group(1)) + \
            Decimal(mobj.group(2)) + Decimal(mobj.group(3))
        psivar['MP2 TOTAL ENERGY'] = mobj.group(5)

    mobj = re.search(
        r'^\s+' + r'(?:E2\(AA\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(BB\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(AB\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(SINGLE\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:E2\(TOT\))' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'(?:Total MP2 energy)' + r'\s+=\s+' + NUMBER + r'\s+a.u.\s*$',
        outtext, re.MULTILINE)
    if mobj:
        print('matched mp2ro')
        psivar['MP2 SAME-SPIN ENERGY'] = Decimal(mobj.group(1)) + Decimal(mobj.group(2))
        psivar['MP2 OPPOSITE-SPIN ENERGY'] = mobj.group(3)
        psivar['MP2 SINGLES ENERGY'] = mobj.group(4)
        psivar['MP2 CORRELATION ENERGY'] = Decimal(mobj.group(1)) + \
            Decimal(mobj.group(2)) + Decimal(mobj.group(3)) + Decimal(mobj.group(4))
        psivar['MP2 TOTAL ENERGY'] = mobj.group(6)

    # Process MP3
    mobj = re.search(
        r'^\s+' + r'(?:D-MBPT\(2\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:D-MBPT\(3\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched mp3r')
        dmp2 = Decimal(mobj.group(1))
        dmp3 = Decimal(mobj.group(3))
        psivar['MP2 CORRELATION ENERGY'] = dmp2
        psivar['MP2 TOTAL ENERGY'] = mobj.group(2)
        psivar['MP3 CORRELATION ENERGY'] = dmp2 + dmp3
        psivar['MP3 TOTAL ENERGY'] = mobj.group(4)
        psivar['MP2.5 CORRELATION ENERGY'] = dmp2 + Decimal('0.500000000000') * dmp3
        psivar['MP2.5 TOTAL ENERGY'] = psivar['MP2.5 CORRELATION ENERGY'] + psivar['SCF TOTAL ENERGY']

    mobj = re.search(
        r'^\s+' + r'(?:S-MBPT\(2\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:D-MBPT\(2\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:S-MBPT\(3\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:D-MBPT\(3\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched mp3ro')
        dmp2 = Decimal(mobj.group(1)) + Decimal(mobj.group(3))
        dmp3 = Decimal(mobj.group(5)) + Decimal(mobj.group(7))
        psivar['MP3 CORRELATION ENERGY'] = dmp2 + dmp3
        psivar['MP3 TOTAL ENERGY'] = mobj.group(8)
        psivar['MP2.5 CORRELATION ENERGY'] = dmp2 + Decimal('0.500000000000') * dmp3
        psivar['MP2.5 TOTAL ENERGY'] = psivar['MP2.5 CORRELATION ENERGY'] + psivar['SCF TOTAL ENERGY']

    # Process MP4
    mobj = re.search(
        r'^\s+' + r'(?:D-MBPT\(2\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:D-MBPT\(3\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:D-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:Q-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:S-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched mp4r')
        dmp2 = Decimal(mobj.group(1))
        dmp3 = Decimal(mobj.group(3))
        dmp4sdq = Decimal(mobj.group(5)) + Decimal(mobj.group(7)) + Decimal(mobj.group(9))
        psivar['MP2 CORRELATION ENERGY'] = dmp2
        psivar['MP2 TOTAL ENERGY'] = mobj.group(2)
        psivar['MP3 CORRELATION ENERGY'] = dmp2 + dmp3
        psivar['MP3 TOTAL ENERGY'] = mobj.group(4)
        psivar['MP2.5 CORRELATION ENERGY'] = dmp2 + Decimal('0.500000000000') * dmp3
        psivar['MP2.5 TOTAL ENERGY'] = psivar['MP2.5 CORRELATION ENERGY'] + psivar['SCF TOTAL ENERGY']
        psivar['MP4(SDQ) CORRELATION ENERGY'] = dmp2 + dmp3 + dmp4sdq
        psivar['MP4(SDQ) TOTAL ENERGY'] = mobj.group(10)

    mobj = re.search(
        r'^\s+' + r'(?:S-MBPT\(2\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:D-MBPT\(2\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:S-MBPT\(3\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:D-MBPT\(3\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:L-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:NL-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched mp4ro')
        dmp2 = Decimal(mobj.group(1)) + Decimal(mobj.group(3))
        dmp3 = Decimal(mobj.group(5)) + Decimal(mobj.group(7))
        dmp4sdq = Decimal(mobj.group(9)) + Decimal(mobj.group(11))
        psivar['MP2 CORRELATION ENERGY'] = dmp2
        psivar['MP2 TOTAL ENERGY'] = mobj.group(4)
        psivar['MP3 CORRELATION ENERGY'] = dmp2 + dmp3
        psivar['MP3 TOTAL ENERGY'] = mobj.group(8)
        psivar['MP2.5 CORRELATION ENERGY'] = dmp2 + Decimal('0.500000000000') * dmp3
        psivar['MP2.5 TOTAL ENERGY'] = psivar['MP2.5 CORRELATION ENERGY'] + psivar['SCF TOTAL ENERGY']
        psivar['MP4(SDQ) CORRELATION ENERGY'] = dmp2 + dmp3 + dmp4sdq
        psivar['MP4(SDQ) TOTAL ENERGY'] = mobj.group(12)

    mobj = re.search(
        r'^\s+' + r'(?:D-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:Q-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:S-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:T-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched mp4tr')
        dmp4sdq = Decimal(mobj.group(1)) + Decimal(mobj.group(3)) + Decimal(mobj.group(5))
        dmp4t = Decimal(mobj.group(7))
        psivar['MP4(SDQ) CORRELATION ENERGY'] = psivar['MP3 CORRELATION ENERGY'] + dmp4sdq
        psivar['MP4(SDQ) TOTAL ENERGY'] = mobj.group(6)
        psivar['MP4(T) CORRECTION ENERGY'] = dmp4t
        psivar['MP4(SDTQ) CORRELATION ENERGY'] = psivar['MP3 CORRELATION ENERGY'] + dmp4sdq + dmp4t
        psivar['MP4(SDTQ) TOTAL ENERGY'] = mobj.group(8)
        psivar['MP4 CORRELATION ENERGY'] = psivar['MP4(SDTQ) CORRELATION ENERGY']
        psivar['MP4 TOTAL ENERGY'] = psivar['MP4(SDTQ) TOTAL ENERGY']

    mobj = re.search(
        r'^\s+' + r'(?:L-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:NL-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:WT12-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*' +
        r'^\s+' + r'(?:T-MBPT\(4\))' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched mp4tro')
        dmp4sdq = Decimal(mobj.group(1)) + Decimal(mobj.group(3))
        dmp4t = Decimal(mobj.group(5)) + Decimal(mobj.group(7))  # TODO: WT12 with T, not SDQ?
        psivar['MP4(SDQ) CORRELATION ENERGY'] = psivar['MP3 CORRELATION ENERGY'] + dmp4sdq
        psivar['MP4(SDQ) TOTAL ENERGY'] = mobj.group(4)
        psivar['MP4(T) CORRECTION ENERGY'] = dmp4t
        psivar['MP4(SDTQ) CORRELATION ENERGY'] = psivar['MP3 CORRELATION ENERGY'] + dmp4sdq + dmp4t
        psivar['MP4(SDTQ) TOTAL ENERGY'] = mobj.group(8)
        psivar['MP4 CORRELATION ENERGY'] = psivar['MP4(SDTQ) CORRELATION ENERGY']
        psivar['MP4 TOTAL ENERGY'] = psivar['MP4(SDTQ) TOTAL ENERGY']

    # Process CC Iterations
    mobj = re.search(
        r'^\s+' + r'(?P<fullCC>(?P<iterCC>CC(?:\w+))(?:\(T\))?)' + r'\s+(?:energy will be calculated.)\s*' +
        r'(?:.*?)' +
        r'^\s+' + r'(?:\d+)' + r'\s+' + NUMBER + r'\s+' + NUMBER + r'\s+DIIS\s*' +
        r'^\s*(?:-+)\s*' +
        r'^\s*(?:A miracle (?:has come|come) to pass. The CC iterations have converged.)\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched cc with full %s iterating %s' % (mobj.group('fullCC'), mobj.group('iterCC')))
        print('matched cc')
        print mobj.group(1), mobj.group(2), mobj.group(3), mobj.group(4)
        psivar['%s CORRELATION ENERGY' % (mobj.group('iterCC'))] = mobj.group(3)
        psivar['%s TOTAL ENERGY' % (mobj.group('iterCC'))] = mobj.group(4)

    # Process CC(T)
    mobj = re.search(
        r'^\s+' + r'(?:E\(SCF\))' + r'\s+=\s+' + NUMBER + r'\s+a\.u\.\s*' +
        r'(?:.*?)' +
        r'^\s+' + r'(?:E\(CCSD\))' + r'\s+=\s+' + NUMBER + r'\s*' +
        r'(?:.*?)' +
        r'^\s+' + r'(?:E\(CCSD\(T\)\))' + r'\s+=\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched ccsd(t) vcc')
        psivar['SCF TOTAL ENERGY'] = mobj.group(1)
        psivar['CCSD TOTAL ENERGY'] = mobj.group(2)
        psivar['(T) CORRECTION ENERGY'] = Decimal(mobj.group(3)) - Decimal(mobj.group(2))
        psivar['CCSD(T) CORRELATION ENERGY'] = Decimal(mobj.group(3)) - Decimal(mobj.group(1))
        psivar['CCSD(T) TOTAL ENERGY'] = mobj.group(3)

    mobj = re.search(
        r'^\s+' + r'(?:E\(SCF\))' + r'\s+=\s+' + NUMBER + r'\s+a\.u\.\s*' +
        r'(?:.*?)' +
        r'^\s+' + r'(?:CCSD energy)' + r'\s+' + NUMBER + r'\s*' +
        r'(?:.*?)' +
        r'^\s+' + r'(?:Total perturbative triples energy:)' + r'\s+' + NUMBER + r'\s*' +
        r'^\s*(?:-+)\s*' +
        r'^\s+' + r'(?:CCSD\(T\) energy)' + r'\s+' + NUMBER + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:
        print('matched ccsd(t) ecc')
        psivar['SCF TOTAL ENERGY'] = mobj.group(1)
        psivar['CCSD TOTAL ENERGY'] = mobj.group(2)
        psivar['(T) CORRECTION ENERGY'] = mobj.group(3)
        psivar['CCSD(T) CORRELATION ENERGY'] = Decimal(mobj.group(4)) - Decimal(mobj.group(2))
        psivar['CCSD(T) TOTAL ENERGY'] = mobj.group(4)

    # Process SCS-CC
    mobj = re.search(
        r'^\s+' + r'(?P<fullCC>(?P<iterCC>CC(?:\w+))(?:\(T\))?)' + r'\s+(?:energy will be calculated.)\s*' +
        r'(?:.*?)' +
        r'^\s*' + r'(?:@CCENRG-I, Correlation energies.)' + r'\s+(?:ECCAA)\s+' + NUMBER + r'\s*' +
        r'^\s+(?:ECCBB)\s+' + NUMBER + '\s*' +
        r'^\s+(?:ECCAB)\s+' + NUMBER + '\s*' +
        r'^\s+(?:Total)\s+' + NUMBER + '\s*',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:  # PRINT=2 to get SCS-CC components
        print('matched scscc')
        print mobj.groups()
        psivar['%s SAME-SPIN ENERGY' % (mobj.group('iterCC'))] = Decimal(mobj.group(3)) + Decimal(mobj.group(4))
        psivar['%s OPPOSITE-SPIN ENERGY' % (mobj.group('iterCC'))] = mobj.group(5)
        psivar['%s CORRELATION ENERGY' % (mobj.group('iterCC'))] = mobj.group(6)

    mobj = re.search(
        r'^\s+' + r'(?P<fullCC>(?P<iterCC>CC(?:\w+))(?:\(T\))?)' + r'\s+(?:energy will be calculated.)\s*' +
        r'(?:.*?)' +
        r'^\s+' + r'Amplitude equations converged in' + r'\s*\d+\s*' + r'iterations.\s*' +
        r'^\s+' + r'The AA contribution to the correlation energy is:\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'The BB contribution to the correlation energy is:\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'The AB contribution to the correlation energy is:\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'The total correlation energy is\s+' + NUMBER + r'\s+a.u.\s*' +
        r'^\s+' + r'The CC iterations have converged.' + r'\s*$',
        outtext, re.MULTILINE | re.DOTALL)
    if mobj:  # PRINT=2 to get SCS components
        print('matched scscc2')
        print mobj.groups()
        psivar['%s SAME-SPIN ENERGY' % (mobj.group('iterCC'))] = Decimal(mobj.group(3)) + Decimal(mobj.group(4))
        psivar['%s OPPOSITE-SPIN ENERGY' % (mobj.group('iterCC'))] = mobj.group(5)
        psivar['%s CORRELATION ENERGY' % (mobj.group('iterCC'))] = mobj.group(6)

    # Process CURRENT energies (needs better way)
    if 'SCF TOTAL ENERGY' in psivar:
        psivar['CURRENT REFERENCE ENERGY'] = psivar['SCF TOTAL ENERGY']
        psivar['CURRENT ENERGY'] = psivar['SCF TOTAL ENERGY']

    if 'MP2 TOTAL ENERGY' in psivar and 'MP2 CORRELATION ENERGY' in psivar:
        psivar['CURRENT CORRELATION ENERGY'] = psivar['MP2 CORRELATION ENERGY']
        psivar['CURRENT ENERGY'] = psivar['MP2 TOTAL ENERGY']

    if 'MP3 TOTAL ENERGY' in psivar and 'MP3 CORRELATION ENERGY' in psivar:
        psivar['CURRENT CORRELATION ENERGY'] = psivar['MP3 CORRELATION ENERGY']
        psivar['CURRENT ENERGY'] = psivar['MP3 TOTAL ENERGY']

    if 'MP4 TOTAL ENERGY' in psivar and 'MP4 CORRELATION ENERGY' in psivar:
        psivar['CURRENT CORRELATION ENERGY'] = psivar['MP4 CORRELATION ENERGY']
        psivar['CURRENT ENERGY'] = psivar['MP4 TOTAL ENERGY']

#    if ('%s TOTAL ENERGY' % (mobj.group('fullCC')) in psivar) and \
#       ('%s CORRELATION ENERGY' % (mobj.group('fullCC')) in psivar):
#        psivar['CURRENT CORRELATION ENERGY'] = psivar['%s CORRELATION ENERGY' % (mobj.group('fullCC')]
#        psivar['CURRENT ENERGY'] = psivar['%s TOTAL ENERGY' % (mobj.group('fullCC')]

    if 'CCSD TOTAL ENERGY' in psivar and 'CCSD CORRELATION ENERGY' in psivar:
        psivar['CURRENT CORRELATION ENERGY'] = psivar['CCSD CORRELATION ENERGY']
        psivar['CURRENT ENERGY'] = psivar['CCSD TOTAL ENERGY']

    if 'CCSD(T) TOTAL ENERGY' in psivar and 'CCSD(T) CORRELATION ENERGY' in psivar:
        psivar['CURRENT CORRELATION ENERGY'] = psivar['CCSD(T) CORRELATION ENERGY']
        psivar['CURRENT ENERGY'] = psivar['CCSD(T) TOTAL ENERGY']

    if 'CC3 TOTAL ENERGY' in psivar and 'CC3 CORRELATION ENERGY' in psivar:
        psivar['CURRENT CORRELATION ENERGY'] = psivar['CC3 CORRELATION ENERGY']
        psivar['CURRENT ENERGY'] = psivar['CC3 TOTAL ENERGY']

    if 'CCSDT TOTAL ENERGY' in psivar and 'CCSDT CORRELATION ENERGY' in psivar:
        psivar['CURRENT CORRELATION ENERGY'] = psivar['CCSDT CORRELATION ENERGY']
        psivar['CURRENT ENERGY'] = psivar['CCSDT TOTAL ENERGY']

    return psivar


def cfour_memory(mem):
    """Transform input *mem* in MB into psi4-type options for cfour.

    """
    text = ''

    # prepare memory keywords to be set as c-side keywords
    options = collections.defaultdict(lambda: collections.defaultdict(dict))
    options['CFOUR']['CFOUR_MEMORY_SIZE']['value'] = int(mem)
    options['CFOUR']['CFOUR_MEM_UNIT']['value'] = 'MB'

    return text, options