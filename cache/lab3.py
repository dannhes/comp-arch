MEM_SIZE = 2**16
ADDR_LEN = 20-4
CACHE_WAY = 4
CACHE_TAG_LEN = 10-4
CACHE_IDX_LEN = 4+1
CACHE_OFFSET_LEN = 6-1
CACHE_SIZE =64*64
CACHE_LINE_SIZE = 64/2
CACHE_LINE_COUNT =64*2
CACHE_SETS_COUNT = 16*2
ADDR1_BUS_LEN = ADDR_LEN
ADDR2_BUS_LEN = ADDR_LEN-CACHE_OFFSET_LEN
DATA1_BUS_LEN = 16
DATA2_BUS_LEN = 16*2
CTR1_BUS_LEN = 3
CTR2_BUS_LEN = 2
cache = [[[0, 0, 0] for r in range(CACHE_WAY)] for r2 in range(CACHE_SETS_COUNT)] # [tag,flag,cur_tacts]
LRU_tacts = 0
PLRU_tacts = 0
RR_tacts = 0
cache_in_rr = 0
cache_out_rr=0
cache_in_plru = 0
cache_out_plru =0
M = 64
N = 60
K = 32
a = [[0]*32]*64
b = [[0]*60]*32
c = [[0]*60]*64
cache_in = 0
cache_out = 0

def check_in_cache(adres,size):
    global cache,cache_in,LRU_tacts,cache_out
    ofset = int(adres[-CACHE_OFFSET_LEN:],2)
    idx = int(adres[-(CACHE_IDX_LEN+CACHE_OFFSET_LEN):-CACHE_OFFSET_LEN],2)
    tag = int(adres[:-(CACHE_IDX_LEN+CACHE_OFFSET_LEN)],2)
    for i in range(4):
        if(cache[idx][i][0]==tag):
            max1 = 0
            for j in range(4):
                max1 = max(max1,cache[idx][j][2])
            cache[idx][i][2]=max1+1
            cache_in+=1
            cache[idx][i][1]=1
            LRU_tacts += 6 + size//ADDR1_BUS_LEN
            break
    else:
        cache_out+=1
        LRU_tacts+=4
        LRU_tacts+=100
        LRU_tacts+=1+ size//ADDR1_BUS_LEN # write from mem & data
        max_age = cache[idx][0][2]
        min_age = cache[idx][0][2]
        ind = 0
        for j in range(1,4):
            if cache[idx][j][2]<min_age:
                min_age = cache[idx][j][2]
                ind = j
            max_age = max(max_age,cache[idx][j][2])
        if cache[idx][ind][1]==1:
            LRU_tacts+=16+1
        cache[idx][ind][0] = tag
        cache[idx][ind][1] = 0
        cache[idx][ind][2] = max_age+1

LRU_tacts+=1
def nmul():
    global LRU_tacts,PLRU_tacts,a,b,c,M,N,K
    LRU_tacts+=1
    LRU_tacts+=2
    for y in range(64):
        LRU_tacts+=3
        for x in range(60):
            LRU_tacts+=2
            s = 0
            LRU_tacts+=2
            for k in range(32):
                s+=a[y][k]*b[k][x]
                check_in_cache(bin(int('400',16)+y * K + k)[2:], 16)
                LRU_tacts+=2
                check_in_cache(bin(K*M+int('400',16)+k*N*2+x*2)[2:], 32)
                LRU_tacts+=7
            c[y][x] = s
            check_in_cache(bin(x*4+N*y*4+int('400',16)+K*M+N*K*2)[2:], 64)
        LRU_tacts+=2
nmul()
LRU_tacts+=1

cache = [[[0, 0, 0] for r in range(CACHE_WAY)] for r2 in range(CACHE_SETS_COUNT)] # [tag,flag,cur_tacts]

def check_in_cache_plru(adres,size):
    global cache, cache_in_plru, PLRU_tacts, cache_out_plru
    ofset = int(adres[-CACHE_OFFSET_LEN:], 2)
    idx = int(adres[-(CACHE_IDX_LEN + CACHE_OFFSET_LEN):-CACHE_OFFSET_LEN], 2)
    tag = int(adres[:-(CACHE_IDX_LEN + CACHE_OFFSET_LEN)], 2)
    for i in range(4):
        if (cache[idx][i][0] == tag):
            PLRU_tacts += 6 + size//ADDR1_BUS_LEN
            cache[idx][i][2] = 1
            cache_in_plru += 1
            count_zer = 0
            for j in range(4):
                if cache[idx][j][2] == 0:
                    count_zer += 1
            if count_zer == 0:
                for j in range(4):
                    if j != i:
                        cache[idx][j][2] = 0
            cache[idx][i][1] = 1
            break
    else:
        cache_out_plru+=1
        PLRU_tacts += 4
        PLRU_tacts += 100
        PLRU_tacts += 1 + size//ADDR1_BUS_LEN # write from mem & data
        ind  = 0
        count_zer = 0
        for j  in range(4):
            if cache[idx][j][2]==0:
                count_zer+=1
                ind = j
        if count_zer==1:
            for j in range(4):
                if j!=ind:
                    cache[idx][j][2] = 0
        if cache[idx][ind][1] == 1:
            PLRU_tacts += 16+1
        cache[idx][ind][0] = tag
        cache[idx][ind][1] = 0
        cache[idx][ind][2] = 1
PLRU_tacts+=1
def nmul():
    global LRU_tacts,PLRU_tacts,a,b,c,M,N,K,cache
    cache = [[[0, 0, 0] for r in range(CACHE_WAY)] for r2 in range(CACHE_SETS_COUNT)]  # [tag,flag,cur_tacts]
    PLRU_tacts+=1
    PLRU_tacts+=2
    for y in range(64):
        PLRU_tacts+=3
        for x in range(60):
            PLRU_tacts+=4
            s = 0
            for k in range(32):
                s+=a[y][k]*b[k][x]
                check_in_cache_plru(bin(int('400',16)+y * K + k)[2:], 16)
                PLRU_tacts+=2
                check_in_cache_plru(bin(K*M+int('400',16)+k*N*2+x*2)[2:], 32)
                PLRU_tacts+=7
            c[y][x] = s
            check_in_cache_plru(bin(x*4+N*y*4+int('400',16)+K*M+N*K*2)[2:], 64)
        PLRU_tacts+=2
nmul()
PLRU_tacts+=1
def check_in_cache_rr(adres,size):
    global cache, cache_in_rr, RR_tacts, cache_out_rr
    ofset = int(adres[-CACHE_OFFSET_LEN:], 2)
    idx = int(adres[-(CACHE_IDX_LEN + CACHE_OFFSET_LEN):-CACHE_OFFSET_LEN], 2)
    tag = int(adres[:-(CACHE_IDX_LEN + CACHE_OFFSET_LEN)], 2)
    for i in range(4):
        if (cache[idx][i][0] == tag):
            cache_in_rr += 1
            RR_tacts += 6 + size // ADDR1_BUS_LEN
            cache[idx][i][1] = 1
            break
    else:
        cache_out_rr += 1
        RR_tacts += 4
        RR_tacts += 100
        RR_tacts += 1 + size // ADDR1_BUS_LEN  # write from mem & data
        ind = 0
        count_zer = 0
        for j in range(4):
            if cache[idx][j][2] == 0:
                ind = j
        if cache[idx][ind][1] == 1:
            RR_tacts += 17
        cache[idx][ind][0] = tag
        cache[idx][ind][1] = 0
        cache[idx][ind][2] = 1
        for j in range(4):
            if cache[idx][j][2] == 0:
                count_zer += 1
        if count_zer == 0:
            for j in range(4):
                cache[idx][j][2] = 0
def nmul():
    global RR_tacts, RR_tacts, a, b, c, M, N, K,cache
    cache = [[[0, 0, 0] for r in range(CACHE_WAY)] for r2 in range(CACHE_SETS_COUNT)]
    RR_tacts += 1
    RR_tacts += 2
    for y in range(64):
        RR_tacts += 3
        for x in range(60):
            s = 0
            RR_tacts += 4
            for k in range(32):
                s += a[y][k] * b[k][x]
                check_in_cache_rr(bin(int('400', 16) + y * K + k)[2:], 16)
                RR_tacts += 2
                check_in_cache_rr(bin(K * M + int('400', 16) + k * N * 2 + x * 2)[2:], 32)
                RR_tacts += 7
            c[y][x] = s
            check_in_cache_rr(bin(x * 4 + N * y * 4 + int('400', 16) + K * M + N * K * 2)[2:], 64)
        RR_tacts += 2
nmul()
RR_tacts+=1
print("LRU:\thit perc. {:.4f}%\ttime: {time1}\npLRU:\thit perc. {:.4f}%\ttime: {time2}\nRR:\t    hit perc. {:.4f}%\ttime: {time3}\n".format(cache_in / (cache_out+cache_in) * 100, cache_in_plru / (cache_out_plru+cache_in_plru) * 100,(cache_in_rr/(cache_out_rr+cache_in_rr))*100, time1 = LRU_tacts, time2 = PLRU_tacts,time3=RR_tacts))















































































































