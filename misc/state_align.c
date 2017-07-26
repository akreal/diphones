// compile with: gcc -I /usr/local/include/pocketsphinx -I /usr/local/include/sphinxbase -I ~/src/ps/pocketsphinx/src/libpocketsphinx  -l pocketsphinx -l sphinxbase -o state_align state_align.c
#include <pocketsphinx.h>

#include "ps_alignment.h"
#include "state_align_search.h"
#include "pocketsphinx_internal.h"

static int
do_search(ps_search_t *search, acmod_t *acmod, const char *fname)
{
    FILE *rawfh;
    int16 buf[2048];
    size_t nread;
    int16 const *bptr;
    int nfr;

    rawfh = fopen(fname, "rb");
    acmod_start_utt(acmod);
    ps_search_start(search);
    while (!feof(rawfh)) {
        nread = fread(buf, sizeof(*buf), 2048, rawfh);
        bptr = buf;
        while ((nfr = acmod_process_raw(acmod, &bptr, &nread, FALSE)) > 0) {
            while (acmod->n_feat_frame > 0) {
                ps_search_step(search, acmod->output_frame);
                acmod_advance(acmod);
            }
        }
    }
    acmod_end_utt(acmod);
    fclose(rawfh);
    return ps_search_finish(search);
}


int
main(int argc, char *argv[])
{
    ps_decoder_t *ps;
    dict_t *dict;
    dict2pid_t *d2p;
    acmod_t *acmod;
    ps_alignment_t *al;
    ps_alignment_iter_t *itor;
    ps_search_t *search;
    cmd_ln_t *config;
    int i, wi;
    char phone_str[4], word[128];

    config = cmd_ln_init(NULL, ps_args(), FALSE,
                 "-hmm", "../../model/en-us/en-us",
                 "-dict", "../../model/en-us/cmudict-en-us.dict",
                 "-samprate", "16000", NULL);
    ps = ps_init(config);
    dict = ps->dict;
    d2p = ps->d2p;
    acmod = ps->acmod;

    al = ps_alignment_init(d2p);

    wi = 0;
    for (i = 0; argv[2][i] != '\0'; i++) {
        if (argv[2][i] == ' ') {
            word[wi] = '\0';
            ps_alignment_add_word(al, dict_wordid(dict, word), 0);
            wi = 0;
        }
        else {
            word[wi] = argv[2][i];
            wi++;
        }
    }

    word[wi] = '\0';
    ps_alignment_add_word(al, dict_wordid(dict, word), 0);

    ps_alignment_populate(al);

    search = state_align_search_init("state_align", config, acmod, al);

    do_search(search, acmod, argv[1]);

    itor = ps_alignment_phones(al);

    while (itor != NULL) {
        bin_mdef_phone_str(acmod->mdef, ps_alignment_iter_get(itor)->id.pid.cipid, phone_str);

        printf("%s\t%d\t%d\t%d\n", phone_str,
            ps_alignment_iter_get(itor)->start,
            ps_alignment_iter_get(itor)->start + ps_alignment_iter_get(itor)->duration,
            ps_alignment_iter_get(itor)->score);

        itor = ps_alignment_iter_next(itor);
    }

    ps_search_free(search);
    ps_alignment_free(al);

    ps_free(ps);
    cmd_ln_free_r(config);
    return 0;
}
