from recipes.almahelpers import fixsyscaltimes # SACM/JAO - Fixes
__rethrow_casa_exceptions = True
h_init()
try:
    hifa_restoredata (vis=['uid___A002_Xcc8b19_X3341', 'uid___A002_Xcc8b19_X394f'], session=['session_1', 'session_2'], ocorr_mode='ca')
finally:
    h_save()
