import gzip, re, argparse
import shutil
from subprocess import run
import pandas as pd


def clinvar_list_to_dict(l):
    """
    This is not a general list_to_dict function
    helper of clinvar_vcf_gz_to_csv only
    Convert list to dict.
    """
    return {k: v for k, v in (x.split('=') for x in l)}


def clinvar_vcf_gz_to_csv(fname_in, fname_out, vep=False):

    '''
    NOT A GENERAL FUNCTION: THIS FILTERS varinets that have more than one submission
    ALSO adds a CLASS to classify ambigous phenotypes
    CAUTION: this will take a couple of minutes depending on the input file size
    converts a clinvar.vcf.gz to regualr csv file
    fname_in: input filepath with .gz
    fname_out: output filepath ending with .csv
    vep: if set True, exports a vep annotated csv
    '''
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--vep', action='store_true',
    #                     help='export a vep annotated csv')
    # args = parser.parse_args()
    # vep = args.vep

    # store column info
    cv_columns = {}
    with gzip.open(fname_in, 'rt') as f:
        for metaline in f:
            if metaline.startswith('##INFO'):
                colname = re.search('ID=(\w+),',
                                    metaline.strip('#\n'))
                coldesc = re.search('.*Description=(.*)>',
                                    metaline.strip('#\n'))
                cv_columns[colname.group(1)] = coldesc.group(1).strip('"')

    # read clinvar vcf
    cv_df = pd.read_csv(fname_in, sep='\t', comment='#', header=None,
                        usecols=[0, 1, 2, 3, 4, 7], dtype={0: object})

    # convert dictionaries to columns
    cv_df = pd.concat([cv_df.drop([7], axis=1),
                       cv_df[7].str.split(';')
                            .apply(clinvar_list_to_dict)
                            .apply(pd.Series)], axis=1
                      )
    # rename columns
    cv_df.rename(columns={0: 'CHROM',
                          1: 'POS',
                          2: 'ID',
                          3: 'REF',
                          4: 'ALT'},
                 inplace=True)

    # assign classes
    cv_df['CLASS'] = 0
    cv_df.set_value(cv_df.CLNSIGCONF.notnull(), 'CLASS', 1)

    # convert NaN to 0 where allele frequencies are null
    cv_df[['AF_ESP', 'AF_EXAC', 'AF_TGP']] = \
        cv_df[['AF_ESP', 'AF_EXAC', 'AF_TGP']].fillna(0)

    # select variants that have beeen submitted by multiple organizations.
    cv_df = \
        cv_df.loc[cv_df['CLNREVSTAT']
                  .isin(['criteria_provided,_multiple_submitters,_no_conflicts',
                        'criteria_provided,_conflicting_interpretations'])]

    # Reduce the size of the dataset below
    cv_df.drop(columns=['ALLELEID', 'RS', 'DBVARID'], inplace=True)
    # drop columns that would reveal class
    cv_df.drop(columns=['CLNSIG', 'CLNSIGCONF', 'CLNREVSTAT'], inplace=True)
    # drop this redundant columns
    cv_df.drop(columns=['CLNVCSO'], inplace=True)

    if vep:
        print('processing vep annotations')
        # column names
        with gzip.open('vep/clinvar.annotated.vcf.gz', 'rt') as f:
            for line in f:
                if line.startswith('##INFO=<ID=CSQ'):
                    m = re.search(r'Format: (.*)\">', line)
                    cols = m.group(1).split('|')
                    break
        # gunzip the vcf
        with gzip.open('vep/clinvar.annotated.vcf.gz', 'rb') as f_in:
            with open('vep/clinvar.annotated.vcf', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        try:
            # make sure vawk is in your $PATH
            f = open("vep/clinvar.annotated.csq.vcf", "w")
            run(['vawk', '--header', '{ print $3, I$CSQ }',
                'vep/clinvar.annotated.vcf'], stdout=f)
        except FileNotFoundError:
            print('install vawk to use generate vep annotated .csv, see docs')

        # gzip the vcf
        with open('vep/clinvar.annotated.vcf', 'rb') as f_in:
            with gzip.open('vep/clinvar.annotated.vcf.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        csq_df = pd.read_csv('vep/clinvar.annotated.csq.vcf', sep='\t',
                             comment='#', header=None, names=['ID', 'CSQ'],
                             dtype={0: object})
        csq_df = csq_df.reindex(columns=['ID', 'CSQ'] + cols)
        csq_df[cols] = csq_df['CSQ'].str.split('|').apply(pd.Series)
        csq_df['ID'] = csq_df['ID'].astype(int)
        df = cv_df.merge(csq_df.drop(columns=['CSQ']), on='ID')

        # drop some vep columns that are all null
        # df = df.loc[:, ~df.isnull().all()] # this didn't work, so be explicit
        df = df.drop(columns=['HGVSc', 'HGVSp', 'Existing_variation',
                              'FLAGS', 'HGNC_ID', 'TSL',
                              'APPRIS', 'REFSEQ_MATCH', 'MPC'])
        # Use the SYMBOL field instead of parsing GENEINFO
        df = df.drop(columns=['Gene', 'GENEINFO', 'SYMBOL_SOURCE'])
        # finally drop extra REF info from vep
        df = df.drop(columns=['GIVEN_REF', 'USED_REF'])

        df.drop(columns=['ID']).to_csv(fname_out,
                                       index=False)

    else:
        cv_df.drop(columns=['ID']).to_csv(fname_out,
                                          index=False)


def clinvar_vcf_gz_to_df(fname_in):
    '''
    CAUTION: this will take a couple of minutes depending on the input file size
    converts a clinvar.vcf.gz to regualar pandas dataframe
    fname_in: input filepath with .gz
    '''

    # store column info
    cv_columns = {}
    with gzip.open(fname_in, 'rt') as f:
        for metaline in f:
            if metaline.startswith('##INFO'):
                colname = re.search('ID=(\w+),',
                                    metaline.strip('#\n'))
                coldesc = re.search('.*Description=(.*)>',
                                    metaline.strip('#\n'))
                cv_columns[colname.group(1)] = coldesc.group(1).strip('"')

    # read clinvar vcf
    cv_df = pd.read_csv(fname_in, sep='\t', comment='#', header=None,
                        usecols=[0, 1, 2, 3, 4, 7], dtype={0: object})

    # convert dictionaries to columns
    cv_df = pd.concat([cv_df.drop([7], axis=1),
                       cv_df[7].str.split(';')
                            .apply(clinvar_list_to_dict)
                            .apply(pd.Series)], axis=1
                      )
    # rename columns
    cv_df.rename(columns={0: 'CHROM',
                          1: 'POS',
                          2: 'ID',
                          3: 'REF',
                          4: 'ALT'},
                 inplace=True)
    return cv_df
