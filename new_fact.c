#include"prime16.c"
#include<stdlib.h>
#include<string.h>

#define ull unsigned long long
#define MIN(a, b) ((a)<(b)?(a):(b))
#define NEW_FACT malloc(sizeof(Factors))


typedef struct Pow{
    ull base;
    short exp;
} Pow;

typedef struct Factors{
    ull i;
    unsigned factors_count;
    Pow *factors;
} Factors;

size_t new(ull i, unsigned size, size_t factors){
    Factors * restrict ans = NEW_FACT;
    Pow *ps = malloc(size*sizeof(Pow));
    memcpy(ps, factors, sizeof(Pow)*size);
    *ans = (Factors){i, size, ps};
    return ans;
}

size_t copy(size_t f){
    Factors * restrict ans = NEW_FACT;
    Pow *ps = malloc(sizeof(Pow)*(((Factors*)f)->factors_count));
    memcpy(ps, ((Factors*)f)->factors, sizeof(Pow)*(((Factors*)f)->factors_count));
    *ans = (Factors){((Factors*)f)->i, ((Factors*)f)->factors_count, ps};
    return ans;
}

size_t mul(size_t a, size_t b){
    Factors * restrict res = NEW_FACT;
    *res = (Factors){((Factors*)a)->i*((Factors*)b)->i, 0, malloc(sizeof(Pow)*(((Factors*)a)->factors_count+((Factors*)b)->factors_count))};
    unsigned i=0, j=0, size=0;
    while(i<((Factors*)a)->factors_count && j<((Factors*)b)->factors_count){
        if(((Factors*)b)->factors[j].base==((Factors*)a)->factors[i].base){
            res->factors[size].base = ((Factors*)a)->factors[i].base;
            res->factors[size].exp = ((Factors*)a)->factors[i].exp + ((Factors*)b)->factors[j].exp;
            ++size, ++i, ++j;
        }
        else{
            res->factors[size++] = ((Factors*)a)->factors[i].base>((Factors*)b)->factors[j].base ? 
                ((Factors*)b)->factors[j++] :
                ((Factors*)a)->factors[i++] ;
        }
    }
    while(i<((Factors*)a)->factors_count){
        res->factors[size++] = ((Factors*)a)->factors[i++];
    }
    while(j<((Factors*)b)->factors_count){
        res->factors[size++] = ((Factors*)b)->factors[j++];
    }
    res->factors_count = size;
    return res;
}

size_t _pow(size_t f, unsigned exp){
    Factors * restrict res;
    if(exp==0){
        res = NEW_FACT;
        *res = (Factors){1, 0, NULL};
        return res;
    }
    res = copy(f);
    ull tmp = ((Factors*)f)->i;
    for(unsigned i=exp; i; i>>=1){
        if(i & 1){
            res->i *= tmp;
        }
        tmp *= tmp;
    }
    for(unsigned i=0; i<((Factors*)f)->factors_count; ++i){
        res->factors[i].exp *= exp;
    }
    return res;
}

void _ipow(size_t fp, unsigned exp){
    if(((Factors*)fp)->i == 0){
        free(((Factors*)fp)->factors);
        *(Factors*)fp = (Factors){1, 0, NULL};
        return;
    }
    ull tmp = ((Factors*)fp)->i;
    ((Factors*)fp)->i = 1;
    for(unsigned i=exp; i; i>>=1){
        if(i & 1){
            ((Factors*)fp)->i *= tmp;
        }
        tmp *= tmp;
    }
    for(unsigned i=0; i<((Factors*)fp)->factors_count; ++i){
        ((Factors*)fp)->factors[i].exp *= exp;
    }
}

size_t gcd(size_t a, size_t b){ // a, b != 0
    Factors * restrict res = NEW_FACT;
    *res = (Factors){1, 0, malloc(sizeof(Pow)*MIN(((Factors*)a)->factors_count, ((Factors*)b)->factors_count))};
    unsigned i=0, j=0, size=0;
    while(i<((Factors*)a)->factors_count && j<((Factors*)b)->factors_count){
        if(((Factors*)b)->factors[j].base==((Factors*)a)->factors[i].base){
            res->factors[size].base = ((Factors*)a)->factors[i].base;
            res->factors[size].exp = MIN(((Factors*)a)->factors[i].exp, ((Factors*)b)->factors[j].exp);
            ++size, ++i, ++j;
        }
        else{
            ((Factors*)a)->factors[i].base>((Factors*)b)->factors[j].base ? ++j : ++i;
        }
    }
    res->factors_count = size;
    for(i=0; i<size; ++i){
        for(j=0; j<res->factors[i].exp; ++j){
            res->i *= res->factors[i].base;
        }
    }
    return res;
}

size_t decompose_u32(unsigned i){ //  i < 2^32
    Factors * restrict ans = NEW_FACT;
    *ans = (Factors){i, .factors=malloc(4*sizeof(Pow))};
    unsigned size=0;
    unsigned capacity = 4;

    unsigned p;
    for(int o=0; o<6542 && SQ_PRIME16[o]<=i; ++o){
        if(i % (p = PRIME16[o])){
            continue;
        }

        if(size == capacity){
            capacity += 3;
            ans->factors = realloc(ans->factors, capacity*sizeof(Pow));
        }
        ans->factors[size++] = (Pow){p, 0};

        do{
            i/=p;
            ans->factors[size-1].exp++;
        }while(!(i%p));
    }

    if(i==1){
        ans->factors_count = size;
        return ans;
    }

    if(size == capacity){
        ans->factors = realloc(ans->factors, (++capacity)*sizeof(Pow));
    }
    ans->factors[size++] = (Pow){i, 1};
    ans->factors_count = size;
    return ans;
}

size_t decompose(ull i){ //  i < 2^52
    Factors * restrict ans = NEW_FACT;
    *ans = (Factors){i, .factors=malloc(4*sizeof(Pow))};
    unsigned size=0;
    unsigned capacity = 4;

    ull p;
    for(int o=0; o<6542 && SQ_PRIME16[o]<=i; ++o){
        if(i % (p = PRIME16[o])){
            continue;
        }

        if(size == capacity){
            capacity += 3;
            ans->factors = realloc(ans->factors, capacity*sizeof(Pow));
        }
        ans->factors[size++] = (Pow){p, 0};

        do{
            i/=p;
            ans->factors[size-1].exp++;
        }while(!(i%p));
    }

    if(i==1){
        ans->factors_count = size;
        return ans;
    }

    if(i<0x100000000){
        if(size == capacity){
            ans->factors = realloc(ans->factors, (++capacity)*sizeof(Pow));
        }
        ans->factors[size++] = (Pow){i, 1};
        ans->factors_count = size;
        return ans;
    }

    ull test = 65537;

    do{
        if(!(i%test)){
            if(size == capacity){
                capacity += 2;
                ans->factors = realloc(ans->factors, capacity*sizeof(Pow));
            }
            ans->factors[size++] = (Pow){test, 0};
            do{
                i/=test;
                ans->factors[size-1].exp++;
            }while(!(i%test));
        }
        test+=2;
        if(!(i%test)){
            if(size == capacity){
                capacity += 2;
                ans->factors = realloc(ans->factors, capacity*sizeof(Pow));
            }
            ans->factors[size++] = (Pow){test, 0};
            do{
                i/=test;
                ans->factors[size-1].exp++;
            }while(!(i%test));
        }
        test+=4;
    }while(test<4294967296 && test*test<=i); // 2^32 to ignore overflow

    if(i==1){
        ans->factors_count = size;
        return ans;
    }

    if(size == capacity){
        ans->factors = realloc(ans->factors, (++capacity)*sizeof(Pow));
    }
    ans->factors[size++] = (Pow){i, 1};
    ans->factors_count = size;
    return ans;
}

unsigned short int* get_prime16_p(){
    return PRIME16;
}

unsigned int* get_sq_prime16_p(){
    return SQ_PRIME16;
}

void free_ptr(void *_Memory){
    free(_Memory);
}

void free_address(size_t _Memory){
    free(_Memory);
}

void free_facted(size_t fp){
    free(((Factors*)fp)->factors);
    free((Factors*)fp);
}
