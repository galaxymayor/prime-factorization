#include"prime16.c"
#include<stdlib.h>
#include<string.h>

#define ull unsigned long long
#define MIN(a, b) ((a)<(b)?(a):(b))

typedef struct Pow{
    ull base;
    short exp;
} Pow;

typedef struct Factors{
    ull i;
    unsigned factors_count;
    Pow *factors;
} Factors;

Factors new(ull i, unsigned size, Pow * factors){
    Pow *ps = malloc(size*sizeof(Pow));
    memcpy(ps, factors, sizeof(Pow)*size);
    return (Factors){i, size, ps};
}

Factors copy(Factors f){
    Pow *ps = malloc(sizeof(Pow)*(f.factors_count));
    memcpy(ps, f.factors, sizeof(Pow)*(f.factors_count));
    return (Factors){f.i, f.factors_count, ps};
}

size_t as_ptr(Factors f){
    Factors *fs = malloc(sizeof(Factors));
    *fs = f;
    return fs;
}

Factors mul(Factors a, Factors b){
    Factors res = {a.i*b.i, 0, malloc(sizeof(Pow)*(a.factors_count+b.factors_count))};
    int i=0, j=0, size=0;
    while(i<a.factors_count && j<b.factors_count){
        if(b.factors[j].base==a.factors[i].base){
            res.factors[size].base = a.factors[i].base;
            res.factors[size].exp = a.factors[i].exp + b.factors[j].exp;
            ++size, ++i, ++j;
        }
        else{
            res.factors[size++] = a.factors[i].base>b.factors[j].base ? 
                b.factors[j++] :
                a.factors[i++] ;
        }
    }
    while(i<a.factors_count){
        res.factors[size++] = a.factors[i++];
    }
    while(j<b.factors_count){
        res.factors[size++] = b.factors[j++];
    }
    res.factors_count = size;
    return res;
}

Factors _pow(Factors f, unsigned exp){
    if(exp==0){
        return (Factors){1, 0, NULL};
    }
    Factors res = copy(f);
    ull tmp = f.i;
    for(unsigned i=exp; i; i>>=1){
        if(i & 1){
            res.i *= tmp;
        }
        tmp *= tmp;
    }
    for(int i=0; i<f.factors_count; ++i){
        res.factors[i].exp *= exp;
    }
    return res;
}

void _ipow(Factors *fp, unsigned exp){
    if(fp->i == 0){
        free(fp->factors);
        *fp = (Factors){1, 0, NULL};
        return;
    }
    ull tmp = fp->i;
    fp->i = 1;
    for(unsigned i=exp; i; i>>=1){
        if(i & 1){
            fp->i *= tmp;
        }
        tmp *= tmp;
    }
    for(int i=0; i<fp->factors_count; ++i){
        fp->factors[i].exp *= exp;
    }
}

Factors gcd(Factors a, Factors b){ // a, b != 0
    Factors res = {1, 0, malloc(sizeof(Pow)*MIN(a.factors_count, b.factors_count))};
    int i=0, j=0, size=0;
    while(i<a.factors_count && j<b.factors_count){
        if(b.factors[j].base==a.factors[i].base){
            res.factors[size].base = a.factors[i].base;
            res.factors[size].exp = MIN(a.factors[i].exp, b.factors[j].exp);
            ++size, ++i, ++j;
        }
        else{
            a.factors[i].base>b.factors[j].base ? ++j : ++i;
        }
    }
    res.factors_count = size;
    for(i=0; i<size; ++i){
        for(j=0; j<res.factors[i].exp; ++j){
            res.i *= res.factors[i].base;
        }
    }
    return res;
}


Factors decompose_u32(unsigned i){ //  i < 2^32
    Factors ans = {i, .factors=malloc(4*sizeof(Pow))};
    unsigned size=0;
    unsigned capacity = 4;

    unsigned p;
    for(int o=0; o<6542 && SQ_PRIME16[o]<=i; ++o){
        if(i % (p = PRIME16[o])){
            continue;
        }

        if(size == capacity){
            capacity += 3;
            ans.factors = realloc(ans.factors, capacity*sizeof(Pow));
        }
        ans.factors[size++] = (Pow){p, 0};

        do{
            i/=p;
            ans.factors[size-1].exp++;
        }while(!(i%p));
    }

    if(i==1){
        ans.factors_count = size;
        return ans;
    }

    if(size == capacity){
        ans.factors = realloc(ans.factors, (++capacity)*sizeof(Pow));
    }
    ans.factors[size++] = (Pow){i, 1};
    ans.factors_count = size;
    return ans;
}

Factors decompose(ull i){ //  i < 2^50
    Factors ans = {i, .factors=malloc(4*sizeof(Pow))};
    unsigned size=0;
    unsigned capacity = 4;

    ull p;
    for(int o=0; o<6542 && SQ_PRIME16[o]<=i; ++o){
        if(i % (p = PRIME16[o])){
            continue;
        }

        if(size == capacity){
            capacity += 3;
            ans.factors = realloc(ans.factors, capacity*sizeof(Pow));
        }
        ans.factors[size++] = (Pow){p, 0};

        do{
            i/=p;
            ans.factors[size-1].exp++;
        }while(!(i%p));
    }

    if(i==1){
        ans.factors_count = size;
        return ans;
    }

    if(i<0x100000000){
        if(size == capacity){
            ans.factors = realloc(ans.factors, (++capacity)*sizeof(Pow));
        }
        ans.factors[size++] = (Pow){i, 1};
        ans.factors_count = size;
        return ans;
    }

    ull test = 65537;

    do{
        if(!(i%test)){
            if(size == capacity){
                capacity += 2;
                ans.factors = realloc(ans.factors, capacity*sizeof(Pow));
            }
            ans.factors[size++] = (Pow){test, 0};
            do{
                i/=test;
                ans.factors[size-1].exp++;
            }while(!(i%test));
        }
        test+=2;
        if(!(i%test)){
            if(size == capacity){
                capacity += 2;
                ans.factors = realloc(ans.factors, capacity*sizeof(Pow));
            }
            ans.factors[size++] = (Pow){test, 0};
            do{
                i/=test;
                ans.factors[size-1].exp++;
            }while(!(i%test));
        }
        test+=4;
    }while(test<33554432&&test*test<=i); // 2^25

    if(i==1){
        ans.factors_count = size;
        return ans;
    }

    if(size == capacity){
        ans.factors = realloc(ans.factors, (++capacity)*sizeof(Pow));
    }
    ans.factors[size++] = (Pow){i, 1};
    ans.factors_count = size;
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

void free_ptr_size_t(size_t _Memory){
    free(_Memory);
}
//test 

// #include<stdio.h>
// int main(){
//     Factors f;
//     for(ull i=1; i<100; ++i){
//         f = decompose(i);
//         printf("decompose %llu: ", i);
//         for(int j=0; j<f.factors_count; ++j){
//             printf("(%llu, %llu)", f.factors[j].base, f.factors[j].exp);
//         }
//         puts("");
//         free(f.factors);
//     }
// }
